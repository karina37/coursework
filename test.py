#!/usr/bin/env python
# coding: utf-8

from datetime import datetime
from database import *
import pony.orm

@db_session
def t():
    # db.drop_table(User)
    User(chat_id=393396177, admin = True, play = False, play_plot = '0', date = '31.03.21 02:00:58', play_message_id=0)
    User(chat_id=525926026, admin = True, play = False, play_plot = '0', date = '30.03.21 23:02:53', play_message_id=0)
    User(chat_id=376854165, admin = False, play = False, play_plot = '0', date = '31.03.21 01:33:14', play_message_id=0)
    User(chat_id=274375218, admin = False, play = False, play_plot = '0', date = '31.03.21 02:05:19', play_message_id=0)

t()