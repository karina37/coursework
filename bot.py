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


@db_session
def start(update: Update, context: CallbackContext) -> None:
    add_users({update.message.chat_id})
    update.message.reply_text('Привет!')


@db_session
def help_command(update: Update, context: CallbackContext) -> None:
    requested_command_names = context.args
    admin = get(user.admin for user in User if user.chat_id == update.message.chat_id)

    if not requested_command_names:
        names = list(select(command.name for command in Command if not command.admin or admin))

        text = 'Список команд:\n/' + '\n/'.join(names)
        update.message.reply_text(text)

    else:
        commands = set(select(command.name for command in Command))
        for name in requested_command_names:
            name = name.lower()
            if name in commands:
                text = get(command.help for command in Command if command.name == name)
            else:
                text = f'Нет команды "{name}"'
            update.message.reply_text(text)


@db_session
def mem(update: Update, context: CallbackContext) -> None:
    requested_topics = context.args
    for i in range(len(requested_topics)):
        requested_topics[i] = requested_topics[i].lower()

    topics = select(mem.topic for mem in Mem)

    if not requested_topics or not len(requested_topics):
        links = set(select(mem.link for mem in Mem))
        context.bot.send_photo(update.message.chat_id, *sample(links, 1))
    else:
        for topic in requested_topics:
            if topic in topics:
                links = set(select(mem.link for mem in Mem if mem.topic == topic))
                context.bot.send_photo(update.message.chat_id, *sample(links, 1))
            else:
                update.message.reply_text(f'Мемов на тему "{topic}" у меня нет')


@db_session
def music(update: Update, context: CallbackContext) -> None:
    requested_singers = context.args
    for i in range(len(requested_singers)):
        requested_singers[i] = requested_singers[i].lower()

    singers = set(select(music.singer for music in Music))

    if not requested_singers or not len(requested_singers):
        links = set(select(music.link for music in Music))
        update.message.reply_text(*sample(links, 1))

    else:
        for singer in requested_singers:
            if singer in singers:
                links = set(select(music.link for music in Music if music.singer == singer))
                update.message.reply_text(*sample(links, 1))
            else:
                update.message.reply_text(f'Музыки исполнителя "{singer}" у меня нет')


@db_session
def delete_commands(update: Update, context: CallbackContext) -> None:
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
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        name, help = context.args[0], ' '.join(context.args[1:])

        add_commands({name: help})

        update.message.reply_text(f'Команда "{name}" добавлена в базу данных.')


@db_session
def change_permissions(update: Update, context: CallbackContext) -> None:
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        requested_command_names = context.args

        names = set(select(command.name for command in Command))

        for name in requested_command_names:
            if name in names:
                key = get(command.id for command in Command if command.name == name)
                Command[key].admin = not Command[key].admin
                Command[key].date = datetime.now().strftime(date_format)

                if Command[key].admin:
                    text = f'Команда "{name}" теперь доступна только админам.'
                else:
                    text = f'Команда "{name}" теперь доступна всем пользователям.'

                update.message.reply_text(text)
            else:
                update.message.reply_text(f'Команды "{name}" нет.')


@db_session
def movies(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Работа в процессе. Вы можете поддержать проект: ')
    context.bot.send_contact(
        phone_number='+79854127639',
        first_name='raz',
        last_name='dva',
        chat_id=update.message.chat_id
    )


@db_session
def start_play(update: Update, context: CallbackContext) -> None:
    key = get(user.id for user in User if update.message.chat_id == user.chat_id)

    try:
        context.bot.editMessageReplyMarkup(User[key].chat_id, User[key].play_message_id, reply_markup=None)
    except:
        pass

    if not User[key].play:
        keyboard = [
            [
                InlineKeyboardButton(text='Начать', callback_data='-2')
            ],
            [
                InlineKeyboardButton(text='Выход', callback_data='-1')
            ]
        ]

        text = 'Запускаю игру.'
    else:
        keyboard = [
            [
                InlineKeyboardButton(text='Начать заново', callback_data='-2'),
                InlineKeyboardButton(text='Продолжить', callback_data='-3')
            ],
            [
                InlineKeyboardButton(text='Выход', callback_data='-1')
            ]
        ]
        text = 'Вы не завершили игру в прошлый раз. Желаете продолжить или начать заново?'

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = update.message.reply_text(text, reply_markup=reply_markup)
    User[key].play_message_id = message.message_id


@db_session
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    step_now = query.data

    key = get(user.id for user in User if query.message.chat_id == user.chat_id)

    reply_markup = None

    query.edit_message_reply_markup(reply_markup=None)

    if step_now == '-1':
        text = 'Игра завершена.'
        step_now = '0'
        User[key].play = False

    else:
        if step_now == '-2':
            step_now = '1'
            User[key].play = True

        elif step_now == '-3':
            step_now = str(get(user.play_plot for user in User if query.message.chat_id == user.chat_id))

        text = play_plot[step_now]['text']
        steps = play_plot[step_now]['steps']
        buttons = [InlineKeyboardButton(text=text_next, callback_data=callback_data) for callback_data, text_next in steps]
        keyboard = []
        for Button in buttons:
            keyboard.append([Button])
        keyboard.append([InlineKeyboardButton(text='Выход', callback_data='-1')])

        reply_markup = InlineKeyboardMarkup(keyboard)

    message = context.bot.send_message(query.message.chat_id, text, reply_markup=reply_markup)
    User[key].play_message_id = message.message_id

    User[key].play_plot = step_now
    commit()


@db_session
def finish_play(update: Update, context: CallbackContext) -> None:
    key = get(user.id for user in User if update.message.chat_id == user.chat_id)

    if not User[key].play:
        text = 'Вы не начинали игру.'
    else:
        text = 'Завершая игру, Вы сбрасываете весь процесс. Вы уверены, что хотите выйти?'
    update.message.reply_text(text)


@db_session
def add_admins(update: Update, contex: CallbackContext) -> None:
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        admins = {int(person) for person in contex.args}
        users = set(select(user.chat_id for user in User))

        for admin in admins:
            if admin not in users:
                update.message.reply_text(f'Пользователь "{admin}" не активизировал бота. Его невозможно назначить админом.')
            else:
                key = get(user.id for user in User if admin == user.chat_id)
                User[key].admin = True
                update.message.reply_text(f'Пользователь "{admin}" назначен админом.')


@db_session
def delete_admins(update: Update, contex: CallbackContext) -> None:
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        requested_admins = {int(person) for person in contex.args}
        admins = set(select(user.chat_id for user in User if user.admin))

        for admin in requested_admins:
            if admin in admins:
                key = get(user.id for user in User if user.chat_id == admin)
                User[key].admin = False
                update.message.reply_text(f'С пользователя "{admin}" сняты права админа.')
            else:
                update.message.reply_text(f'Пользователь {admin} не являлся админом.')


@db_session
def Add_music(update: Update, contex: CallbackContext) -> None:
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        singer, links = contex.args[0], contex.args[1:]
        add_music({singer: links})
        update.message.reply_text('Запрос выполнен.')


@db_session
def Delete_music(update: Update, contex: CallbackContext) -> None:
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        links = set(contex.args)
        delete_music(links)
        update.message.reply_text('Запрос выполнен.')


@db_session
def Add_mems(update: Update, contex: CallbackContext) -> None:
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        topic, links = contex.args[0], contex.args[1:]
        add_mems({topic: links})
        update.message.reply_text('Запрос выполнен.')


@db_session
def Delete_mems(update: Update, contex: CallbackContext) -> None:
    if get(user.admin for user in User if user.chat_id == update.message.chat_id):
        links = set(contex.args)
        delete_mems(links)
        update.message.reply_text('Запрос выполнен.')


def bochka(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('...Басс колбасит соло Колбасёр по пояс голый...')


def search(a, b):
    c = []
    for i in a:
        for j in b:
            if i == j:
                c.append(i)
                break
    return len(c)


@db_session
def echo(update: Update, context: CallbackContext):
    text = update.message.text

    text = list(map(str, text.split()))

    # морфологический анализ
    for i in range(len(text)):
        morph = pymorphy2.MorphAnalyzer()
        text[i] = morph.parse(text[i])[0].normal_form

    text = set(text)
    # print(text)

    flag = False

    if search(text, {'мем', 'мемасик'}):
        mem(update, context)
        flag = True
    if search(text, {'музыка', 'музло'}):
        music(update, context)
        flag = True
    if search(text, {'бочка'}):
        bochka(update, context)
        flag = True

    if not flag:
        update.message.reply_text('Я не понимаю о чём ты говоришь...')


def main():
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("mem", mem))
    dispatcher.add_handler(CommandHandler("music", music))
    dispatcher.add_handler(CommandHandler("movie", movies))
    dispatcher.add_handler(CommandHandler("bochka", bochka))
    dispatcher.add_handler(CommandHandler("add_command", add_command))
    dispatcher.add_handler(CommandHandler("delete_commands", delete_commands))
    dispatcher.add_handler(CommandHandler("change_permissions", change_permissions))
    dispatcher.add_handler(CommandHandler("start_play", start_play))
    dispatcher.add_handler(CommandHandler("add_admins", add_admins))
    dispatcher.add_handler(CommandHandler("delete_admins", delete_admins))
    dispatcher.add_handler(CommandHandler("finish_play", finish_play))
    dispatcher.add_handler(CommandHandler("add_music", Add_music))
    dispatcher.add_handler(CommandHandler("delete_music", Delete_music))
    dispatcher.add_handler(CommandHandler("add_mems", Add_mems))
    dispatcher.add_handler(CommandHandler("delete_mems", Delete_mems))


    dispatcher.add_handler(CallbackQueryHandler(button))


    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
