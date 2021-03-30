#!/usr/bin/env python
# coding: utf-8


users = {1, 2, 3}
admins = {1, 2, 3, 4, 5}

for i in users | admins:
    print(i)
