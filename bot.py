#!/usr/bin/env python
# coding: utf-8


from telegram import Update
import pymorphy2
from random import randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from database import Mem, Music, db
from pony.orm import *
from pony import orm


def start(update, context):
    update.message.reply_text('Привет!')


@db_session
def help_command(update, context):
    keys = context.args
    commands = set(db.select('select name from Command'))
    for i in range(len(keys)):
        keys[i] = keys[i].lower()
        if keys[i] in commands:
            key = keys[i]
            update.message.reply_text(db.select('select help from Command where name = $key')[0])
        else:
            update.message.reply_text(f'Нет команды "{keys[i]}"')


@db_session
def mem(update, context):
    keys = context.args
    for i in range(len(keys)):
        keys[i] = keys[i].lower()

    topics = set(db.select("select topic from Mem"))

    if not keys or not len(keys):
        links = db.select("select link from Mem")
        i = randint(0, len(links) - 1)
        context.bot.send_photo(update.message.chat_id, links[i])
    else:
        for key in keys:
            if key in topics:
                links = db.select("select link from Mem where topic = $key")
                i = randint(0, len(links) - 1)
                context.bot.send_photo(update.message.chat_id, links[i])
            else:
                update.message.reply_text(f'Мемов на тему "{key}" у меня нет')


@db_session
def music(update, context):
    keys = context.args
    for i in range(len(keys)):
        keys[i] = keys[i].lower()

    singers = set(db.select('select singer from Music'))

    if not keys or not len(keys):
        links = db.select('select link from Music')
        i = randint(0, len(links) - 1)
        update.message.reply_text(links[i])

    else:
        for key in keys:
            if key in singers:
                links = db.select('select link from Music where singer = $key')
                i = randint(0, len(links) - 1)
                update.message.reply_text(links[i])
            else:
                update.message.reply_text(f'Музыки исполнителя "{key}" у меня нет')
    
    
def movies(update, context):
    update.message.reply_text('Работа в процессе. Вы можете поддержать проект: ')
    context.bot.send_contact(
        phone_number='+79854127639',
        first_name='raz',
        last_name='dva',
        chat_id=update.message.chat_id
    )
    

def bochka(update, context):
    update.message.reply_text('...Басс колбасит соло Колбасёр по пояс голый...')


def search(a, b):
    c = []
    for i in a:
        for j in b:
            if i == j:
                c.append(i)
                break
    return len(c)


def echo(update, context):
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
    dispatcher.add_handler(CommandHandler("movies", movies))
    dispatcher.add_handler(CommandHandler("bochka", bochka))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
