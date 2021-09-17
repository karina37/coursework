#!/usr/bin/env python
# coding: utf-8

from datetime import datetime
from database import *
import pony.orm

@db_session
def t():
    musics = list(select(music for music in Music))
    for music in musics:
        if music.singer == 'random':
            Music[music.id].singer = 'другое'

t()