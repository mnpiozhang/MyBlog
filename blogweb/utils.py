#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random

def random_choice(choice_lst):
    randomNum = random.randint(0,len(choice_lst)-1)
    return choice_lst[randomNum]