# -*- coding: utf-8 -*-
# @Desc   :  
# @Author : ylimhs
# @Time   : 2020/5/13 9:45
from util.const import *


class mofisher:
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name
        self.publish_art_num = 0
        self.like_art_num = 0
        self.publish_pin_num = 0
        self.like_pin_num = 0
        self.following_num = 0
        self.active_score = 0

    def add_num(self):
        self.publish_art_num += 1

    def calculation_activity(self, action):
        if action == 0:
            self.publish_art_num += 1
            self.active_score += PUBLISH_ARCIICE
        if action == 1:
            self.like_art_num += 1
            self.active_score += LIKE_ARCIICE
        if action == 2:
            self.publish_pin_num += 1
            self.active_score += PUBLISH_PIN
        if action == 3:
            self.like_pin_num += 1
            self.active_score += LIKE_PIN
        if action == 4:
            self.following_num += 1
            self.active_score += FOLLOWING
