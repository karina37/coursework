#!/usr/bin/env python
# coding: utf-8


from telegram import Update
import pymorphy2
from random import sample
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from database import Mem, Music, Command, User, db, play_plot
from pony.orm import *
from pony import orm


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет!')


@db_session
def help_command(update: Update, context: CallbackContext):
    requested_command_names = context.args

    if not requested_command_names:
        text = 'Список команд:\n/' + '\n/'.join(set(select(command.name for command in Command)))
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
def mem(update: Update, context: CallbackContext):
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
def music(update: Update, context: CallbackContext):
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
    
    
def movies(update: Update, context: CallbackContext):
    update.message.reply_text('Работа в процессе. Вы можете поддержать проект: ')
    context.bot.send_contact(
        phone_number='+79854127639',
        first_name='raz',
        last_name='dva',
        chat_id=update.message.chat_id
    )


def play(update: Update, context: CallbackContext):

    pass
    

def bochka(update: Update, context: CallbackContext):
    update.message.reply_text('...Басс колбасит соло Колбасёр по пояс голый...')


def search(a, b):
    c = []
    for i in a:
        for j in b:
            if i == j:
                c.append(i)
                break
    return len(c)


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
    updater = Updater("1567467293:AAEvG0QFnuOqvZxKAHKVTLhA9ay6ySiEAFw", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("mem", mem))
    dispatcher.add_handler(CommandHandler("music", music))
    dispatcher.add_handler(CommandHandler("movie", movies))
    dispatcher.add_handler(CommandHandler("bochka", bochka))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
