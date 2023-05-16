# -*- coding: utf-8 -*-
# @Desc   :  
# @Author : ylimhs
# @Time   : 2020/5/13 9:45
import json
import os

from model.mofisher import mofisher
from src.spider import get_pins, get_user_dynamic, publish_pin
from util.utils import logging, check_time

cookie = os.getenv("COOKIE")


def get_fishers():
    fisher_list = list()
    cursor = "0"
    has_more = True
    while has_more:
        result = get_pins(cursor)
        data = result.get("data")
        cursor = result.get("cursor")
        # logging.info("cursor:")
        # logging.info(cursor)
        has_more = result.get("has_more")
        # logging.info("has_more:")
        # logging.info(has_more)
        for d in data:
            fisher_map = dict()
            author_user_info = d.get("author_user_info")
            user_id = author_user_info.get("user_id")
            user_name = author_user_info.get("user_name")
            msg_Info = d.get("msg_Info")
            ctime = msg_Info.get("ctime")
            mtime = msg_Info.get("mtime")
            if check_time(ctime) or check_time(mtime):
                fisher_map.update({
                    "user_id": user_id,
                    "user_name": user_name
                })

                fisher = mofisher(user_id, user_name)
                if not any(d.user_id == user_id for d in fisher_list):
                    fisher_list.append(fisher)
            else:


                has_more = False
        # has_more = False
    return fisher_list


def calculation_activity(user, acion_list, has_more):
    if acion_list is None:
        return user, False
    for ac in acion_list:
        action = ac['action']
        time = ac['time']
        if check_time(time):
            user.calculation_activity(action)
        else:
            has_more = False
            break
    return user, has_more


def get_actives(user):
    user_id = user.user_id
    has_more = True
    cursor = "0"
    max_retry = 3
    while has_more and max_retry > 0:
        try:
            result = get_user_dynamic(user_id, cursor)
        except Exception as err:
            max_retry -= 1
            continue

        data = result.get("data")
        cursor = data.get("cursor")
        has_more = data.get("hasMore")
        acion_list = data.get("list")
        user, has_more = calculation_activity(user, acion_list, has_more)
    return user


def print_result(fishers):
    fishers = sorted(fishers, key=lambda x: x.active_score, reverse=True)
    contentMsg = ""
    msg = "-------------------Today Mofish King------------------"
    contentMsg += msg
    contentMsg += "\n"
    logging.info(msg)
    for i in range(3):
        msg = "Top " + str(i + 1) + " is:"
        contentMsg += msg
        contentMsg += "\n"
        logging.info(msg)
        msg = "\tuser_name: " + fishers[i].user_name + "(" + str(fishers[i].user_id) + ")" + "   active_score: " + str(
            fishers[i].active_score)
        logging.info(msg)
        contentMsg += msg
        contentMsg += "\n"
        msg = "\tdetail action is : "
        contentMsg += msg
        contentMsg += "\n"
        logging.info(msg)
        msg = "\t\t\t 发布文章数量 : " + str(fishers[i].publish_art_num)
        contentMsg += msg
        contentMsg += "\n"
        logging.info(msg)
        msg = "\t\t\t 点赞文章数量 : " + str(fishers[i].like_art_num)
        contentMsg += msg
        contentMsg += "\n"
        logging.info(msg)
        msg = "\t\t\t 发布沸点数量 : " + str(fishers[i].publish_pin_num)
        contentMsg += msg
        contentMsg += "\n"
        logging.info(msg)
        msg = "\t\t\t 点赞沸点数量 : " + str(fishers[i].like_pin_num)
        contentMsg += msg
        contentMsg += "\n"
        logging.info(msg)
        msg = "\t\t\t 关注掘友数量 : " + str(fishers[i].following_num)
        contentMsg += msg
        contentMsg += "\n"
        logging.info(msg)
    msg = "----------------------------------------------"
    contentMsg += msg
    contentMsg += "\n"
    logging.info(msg)

    # for fish in fishers:
    #     logging.info(json.dumps(fish.__dict__))
    # print(contentMsg)
    return contentMsg

def get_mofish_king():
    fishers = get_fishers()

    logging.info(" today get_fishers is " + str(len(fishers)))
    index = 1
    for u in fishers:
        logging.info(
            f"Get no.{index} acitive info for the user: {u}  user_id is {u.user_id} user_name is {u.user_name}")
        get_actives(u)
        index += 1
    content = print_result(fishers)
    if cookie is not None and cookie != '':
        publish_pin_to_jj(content)


def publish_pin_to_jj(content):
    result = publish_pin(content, cookie)
    if result is None:
        return
    if "success" == result.get("err_msg"):
        data = result.get("data")
        push_msg_id = data.get("msg_id")
        logging.info("publish success and msg_id is :" + push_msg_id)


def main():
    get_mofish_king()


if __name__ == '__main__':
    main()
