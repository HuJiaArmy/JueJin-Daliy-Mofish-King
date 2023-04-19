# -*- coding: utf-8 -*-
# @Desc   :  
# @Author : ylimhs
# @Time   : 2020/5/13 9:45

import json

from util.utils import request


def get_pins(cursor="0"):
    url = "https://api.juejin.cn/recommend_api/v1/short_msg/recommend"
    payload = json.dumps({
        "id_type": 4,
        "sort_type": 300,
        "cursor": cursor,
        "limit": 40
    })
    headers = {
        'Host': 'api.juejin.cn',
        'content-type': 'application/json',
        'accept': '*/*',
        'accept-language': 'zh-cn',
        'origin': 'https://juejin.cn',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15',
        'referer': 'https://juejin.cn/'
    }

    return request("POST", url, headers=headers, payload=payload)


def get_user_dynamic(user_id, cursor="0"):
    url = "https://api.juejin.cn/user_api/v1/user/dynamic?user_id=" + user_id + "&cursor=" + cursor
    payload = {}
    headers = {
        'authority': 'api.juejin.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://juejin.cn',
        'referer': 'https://juejin.cn/',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    return request("GET", url, headers=headers, payload=payload)


def publish_pin(content, cookie):
    if cookie is None:
        return
    url = "https://api.juejin.cn/content_api/v1/short_msg/publish"

    payload = json.dumps({
        "content": "[7101489546776281124#今天沸点有什么好看的#]  \n " + content,
        "topic_id": "6824710203301167112",
        "sync_to_org": False,
        "theme_id": "7101489546776281124"
    })
    headers = {
        'authority': 'api.juejin.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'cookie': cookie,
        'origin': 'https://juejin.cn',
        'referer': 'https://juejin.cn/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'x-secsdk-csrf-token': '0001000000016ed9ee2925fffe9493f2814d0461b737ee506c201a54c9b69a9368a40ad337ad175169091c537492'
    }

    return request("POST", url, headers=headers, payload=payload)
