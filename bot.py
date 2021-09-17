#!/usr/bin/env python
# coding: utf-8


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import pymorphy2
from random import sample
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from database import *
from pony.orm import *
from datetime import datetime
from config import TOKEN
import logging


# Connect logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Define command handlers
@db_session
def start(update: Update, context: CallbackContext) -> None:
    """Authorize a new user and send a welcome message
    after the command /start."""
    add_users({update.message.chat_id})
    update.message.reply_text('Привет!')


@db_session
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a list of available commands (or a description of a specific command)
    or a message stating that there is no such command
    after the command /help <command_name> <other_command_names>."""
    requested_command_names = context.args
    status = get(user.admin for user in User if user.chat_id == update.message.chat_id)

    # Send command list
    if not requested_command_names:
        names = list(select(command.name for command in Command if not command.admin or status))

        text = 'Введите "/help <название_команды> <ещё_названия команд>", ' \
               'чтобы получить более подробное описание определенных команд.\n' \
               'Список команд:\n/' + '\n/'.join(names)

        update.message.reply_text(text)

    # Send a description of a specific program
    else:
        existing_commands = set(select(command.name for command in Command))

        for name in requested_command_names:
            if name.lower() in existing_commands:
                text = get(command.help for command in Command if command.name == name)
            else:
                text = f'Нет команды "{name}"'

            update.message.reply_text(text)


@db_session
def meme(update: Update, context: CallbackContext) -> None:
    """Send a meme or message that there is no such meme
    after the command /meme <topic> <other_topics>"""
    requested_topics = context.args

    existing_topics = set(select(meme.topic for meme in Meme))

    # No topics
    if not search(morphological_analysis(update.message.text), existing_topics) \
            and (not requested_topics or not len(requested_topics)):
        links = set(select(meme.link for meme in Meme))
        context.bot.send_photo(update.message.chat_id, *sample(links, 1))

    # There is at least one topic
    else:
        if not requested_topics:
            requested_topics = set(morphological_analysis(update.message.text))
            command_flag = False
        else:
            requested_topics = set(requested_topics)
            command_flag = True

        for topic in requested_topics:
            topic = topic.lower()

            if topic in existing_topics:
                links = set(select(meme.link for meme in Meme if meme.topic == topic))
                context.bot.send_photo(update.message.chat_id, *sample(links, 1))

            elif command_flag:
                update.message.reply_text(f'Мемов на тему "{topic}" у меня нет')


@db_session
def music(update: Update, context: CallbackContext) -> None:
    """Send a song or a message that there is no such singer
    after the command /music <singer> <other_singers>."""
    requested_singers = context.args

    existing_singers = set(select(music.singer for music in Music))

    # No singer
    if not search(morphological_analysis(update.message.text), existing_singers) \
            and (not requested_singers or not len(requested_singers)):
        links = set(select(music.link for music in Music))
        update.message.reply_text(*sample(links, 1))

    # There is at least one singer
    else:
        if not requested_singers:
            requested_singers = set(morphological_analysis(update.message.text))
            command_flag = False
        else:
            requested_singers = set(requested_singers)
            command_flag = True

        for singer in requested_singers:
            singer = singer.lower()

            if singer in existing_singers:
                links = set(select(music.link for music in Music if music.singer == singer))
                update.message.reply_text(*sample(links, 1))

            elif command_flag:
                update.message.reply_text(f'Музыки исполнителя "{singer}" у меня нет')


@db_session
def delete_commands(update: Update, context: CallbackContext) -> None:
    """Delete commands from the database and send a message with the result
    after the command /delete_commands <command_name> <other_command_names>.
    This action is available only to senders with the admin status."""
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        requested_command_names = context.args

        names = set(select(command.name for command in Command))

        for name in requested_command_names:
            if name in names:
                delete(command for command in Command if command.name == name)

                update.message.reply_text(f'Команда "{name}" удалена из базы данных.')

            else:
                update.message.reply_text(f'Команды "{name}" нет.')


@db_session
def add_command(update: Update, context: CallbackContext) -> None:
    """Add a command to the database and send a message with the result
    after the command /add_command <command_name> <command description>.
    This action is available only to senders with the admin status."""
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        command_name, command_help = context.args[0], ' '.join(context.args[1:])
        add_commands({command_name: command_help})
        update.message.reply_text(f'Команда "{command_name}" добавлена в базу данных.')


@db_session
def change_permissions(update: Update, context: CallbackContext) -> None:
    """Change the access level for the command:
    admin to user, user to admin after the command /change_permissions <command_name> <other_command_names>.
    This action is available only to senders with the admin status."""
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        requested_command_names = context.args

        existing_command_names = set(select(command.name for command in Command))

        for command_name in requested_command_names:
            if command_name in existing_command_names:
                key = get(command.id for command in Command if command.name == command_name)
                Command[key].admin = not Command[key].admin
                Command[key].date = datetime.now().strftime(date_format)

                if Command[key].admin:
                    text = f'Команда "{command_name}" теперь доступна только админам.'
                else:
                    text = f'Команда "{command_name}" теперь доступна всем пользователям.'

                update.message.reply_text(text)

            else:
                update.message.reply_text(f'Команды "{command_name}" нет.')


@db_session
def movies(update: Update, context: CallbackContext) -> None:
    """Send a link to the site to watch the movie
    after the command /movie <film_name> <other_film_names>.
    Temporarily send a message that the command is in development."""
    update.message.reply_text('Работа в процессе. Вы можете поддержать проект: ')
    context.bot.send_contact(
        phone_number='phone number',
        first_name='Name',
        last_name='Firname',
        chat_id=update.message.chat_id
    )


@db_session
def start_game(update: Update, context: CallbackContext) -> None:
    """If possible, delete the old inline_markup,
    send a message asking you to start, continue or end the game,
    and write new message ID with inline_markup to the database
    after the command /start_game."""
    key = get(user.id for user in User if update.message.chat_id == user.chat_id)

    try:
        context.bot.editMessageReplyMarkup(User[key].chat_id, User[key].play_message_id, reply_markup=None)
    except:
        pass

    if not User[key].play:
        keyboard = [
            [InlineKeyboardButton(text='Начать', callback_data='-2')],
            [InlineKeyboardButton(text='Выход', callback_data='-1')]
        ]
        text = 'Запускаю игру.'

    else:
        keyboard = [
            [
                InlineKeyboardButton(text='Начать заново', callback_data='-2'),
                InlineKeyboardButton(text='Продолжить', callback_data='-3')
            ],
            [InlineKeyboardButton(text='Выход', callback_data='-1')]
        ]
        text = 'Вы не завершили игру в прошлый раз. Желаете продолжить или начать заново?'

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = update.message.reply_text(text, reply_markup=reply_markup)
    User[key].play_message_id = message.message_id


@db_session
def button(update: Update, context: CallbackContext) -> None:
    """Handle clicks on inline_markup while playing."""
    query = update.callback_query
    query.answer()
    reply_markup = None
    query.edit_message_reply_markup(reply_markup=reply_markup)

    current_stage = query.data

    key = get(user.id for user in User if query.message.chat_id == user.chat_id)

    # Finish the game
    if current_stage == '-1':
        text = 'Игра завершена.'
        current_stage = '0'
        User[key].play = False

    else:
        # Start the game
        if current_stage == '-2':
            current_stage = '1'

        # Continue the game
        elif current_stage == '-3':
            current_stage = get(user.play_plot for user in User if query.message.chat_id == user.chat_id)

        text = play_plot[current_stage]['text']

        keyboard = []
        steps = play_plot[current_stage]['steps']
        for callback_data, next_text in steps:
            keyboard.append([InlineKeyboardButton(text=next_text, callback_data=callback_data)])
        keyboard.append([InlineKeyboardButton(text='Выход', callback_data='-1')])

        reply_markup = InlineKeyboardMarkup(keyboard)

        User[key].play = True

    new_message = context.bot.send_message(query.message.chat_id, text, reply_markup=reply_markup)
    User[key].play_message_id = new_message.message_id

    User[key].play_plot = current_stage
    commit()


@db_session
def add_admins(update: Update, contex: CallbackContext) -> None:
    """Add admins and send a message with the result for each requested admin
    after the command /add_admins <adminChatID> <otherAdminChatIDs>.
    This action is available only to senders with the admin status."""
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        requested_admins = {int(person) for person in contex.args}

        existing_users = set(select(user.chat_id for user in User))

        for requested_admin in requested_admins:
            if requested_admin in existing_users:
                key = get(user.id for user in User if requested_admin == user.chat_id)
                User[key].admin = True

                text = f'Пользователь "{requested_admin}" назначен админом.'

            else:
                text = f'Пользователь "{requested_admin}" не активизировал бота. Его невозможно назначить админом.'

            update.message.reply_text(text)


@db_session
def delete_admins(update: Update, contex: CallbackContext) -> None:
    """Delete admins and send a message with the result for each requested admin
    after the command /delete_admins <adminChatID> <otherAdminChatIDs>.
    This action is available only to senders with the admin status."""
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        requested_admins = {int(person) for person in contex.args}

        existing_admins = set(select(user.chat_id for user in User if user.admin))

        for requested_admin in requested_admins:
            if requested_admin in existing_admins:
                key = get(user.id for user in User if user.chat_id == requested_admin)
                User[key].admin = False

                text = f'С пользователя "{requested_admin}" сняты права админа.'

            else:
                text = f'Пользователь {requested_admin} не являлся админом.'

            update.message.reply_text(text)


@db_session
def Add_music(update: Update, contex: CallbackContext) -> None:
    """Add links to singer songs and send a message with the result
    after the command /add_music <singer> <song_link> <other_song_links>.
    This action is available only to senders with the admin status."""
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        singer, links = contex.args[0], contex.args[1:]
        add_music({singer: links})

        update.message.reply_text('Запрос выполнен.')


@db_session
def Delete_music(update: Update, contex: CallbackContext) -> None:
    """Delete song links and send a message with the result
    after the command /delete_music <song_link> <other_song_links>.
    This action is available only to senders with the admin status."""
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        links = set(contex.args)
        delete_music(links)

        update.message.reply_text('Запрос выполнен.')


@db_session
def Add_memes(update: Update, contex: CallbackContext) -> None:
    """"Add links to topic memes and send a message with the result
    after the command /add_memes <topic> <meme_link> <other_meme_links>.
    This action is available only to senders with the admin status."""
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        topic, links = contex.args[0], contex.args[1:]
        add_memes({topic: links})

        update.message.reply_text('Запрос выполнен.')


@db_session
def Delete_memes(update: Update, contex: CallbackContext) -> None:
    """Delete meme links and send a message with the result
    after the command /delete_memes <meme_link> <other_meme_links>.
    This action is available only to senders with the admin status."""
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        links = set(contex.args)
        delete_memes(links)

        update.message.reply_text('Запрос выполнен.')


def bochka(update: Update, context: CallbackContext) -> None:
    """Send a special message."""
    update.message.reply_text('...Басс колбасит соло Колбасёр по пояс голый...')


def search(a, b) -> int:
    """Determine the number of identical elements for two iterables
    and return that number."""
    c = []
    for i in a:
        for j in b:
            if i == j:
                c.append(i)
                break

    return len(c)


@db_session
def topics(update: Update, context: CallbackContext) -> None:
    """Send a message with all the meme topics in the database."""
    existing_topics = set(select(meme.topic for meme in Meme))
    text = 'Список имеющихся тем мемов:\n- ' + '\n- '.join(existing_topics)

    update.message.reply_text(text)


@db_session
def singers(update: Update, context: CallbackContext) -> None:
    """Send a message with all the singers of the songs in the database."""
    existing_singers = set(select(music.singer for music in Music))
    text = 'Список имеющихся исполнителей песен:\n- ' + '\n- '.join(existing_singers)

    update.message.reply_text(text)


def morphological_analysis(text):
    """Take a string and
    return a list of all words in normal form."""
    text = list(map(str, text.split()))

    for i in range(len(text)):
        morph = pymorphy2.MorphAnalyzer()
        text[i] = morph.parse(text[i])[0].normal_form

    return text


@db_session
def echo(update: Update, context: CallbackContext) -> None:
    """Process text messages and,
    if there are certain words, execute the appropriate commands."""
    text = morphological_analysis(update.message.text)

    text = set(text)

    flag = False

    if search(text, {'мем', 'мемасик', 'рофл'}):
        meme(update, context)
        flag = True
    if search(text, {'музыка', 'музло', 'песня', 'трек', 'песенка'}):
        music(update, context)
        flag = True
    if search(text, {'фильм', 'фильмец'}):
        movies(update, context)
        flag = True
    if search(text, {'игра', 'играть', 'сыграть'}):
        start_game(update, context)
        flag = True
    if search(text, {'бочка'}):
        bochka(update, context)
        flag = True

    if not flag:
        update.message.reply_text('Я не понимаю о чём ты говоришь...')


def main() -> None:
    """Create and run a bot."""
    # Create a bot
    updater = Updater(TOKEN, use_context=True)

    # Customize the handling of commands and buttons
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("meme", meme))
    dispatcher.add_handler(CommandHandler("music", music))
    dispatcher.add_handler(CommandHandler("movie", movies))
    dispatcher.add_handler(CommandHandler("bochka", bochka))
    dispatcher.add_handler(CommandHandler("add_command", add_command))
    dispatcher.add_handler(CommandHandler("delete_commands", delete_commands))
    dispatcher.add_handler(CommandHandler("change_permissions", change_permissions))
    dispatcher.add_handler(CommandHandler("start_game", start_game))
    dispatcher.add_handler(CommandHandler("add_admins", add_admins))
    dispatcher.add_handler(CommandHandler("delete_admins", delete_admins))
    dispatcher.add_handler(CommandHandler("add_music", Add_music))
    dispatcher.add_handler(CommandHandler("delete_music", Delete_music))
    dispatcher.add_handler(CommandHandler("add_memes", Add_memes))
    dispatcher.add_handler(CommandHandler("delete_memes", Delete_memes))
    dispatcher.add_handler(CommandHandler("topics", topics))
    dispatcher.add_handler(CommandHandler("singers", singers))

    dispatcher.add_handler(CallbackQueryHandler(button))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Run a bot
    updater.start_polling()

    # Block stopping until the special keyboard shortcut Ctrl+C and stop the updater
    updater.idle()


if __name__ == '__main__':
    main()
