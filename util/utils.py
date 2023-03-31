# -*- coding: utf-8 -*-
# @Desc   :  
# @Author : ylimhs
# @Time   : 2020/5/13 9:45
import json
import time
import requests
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    encoding='utf-8')

# 获取当天0点的时间戳
zero_timestamp = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 09:00:00"), "%Y-%m-%d %H:%M:%S")))

# 获取当天下午6点的时间戳
six_pm_timestamp = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 18:00:00"), "%Y-%m-%d %H:%M:%S")))


# 判断当前时间戳是否在0点到下午6点之间
def check_time(current_timestamp):
    if isinstance(current_timestamp,str):
        current_timestamp = int(current_timestamp)
    if zero_timestamp <= current_timestamp <= six_pm_timestamp:
        return True
    else:
        return False


def request(method, url, headers, payload=None, rerty=3):
    if payload is None:
        payload = {}
    logging.info("URL: " + url)
    # logging.info("headers:\n" + json.dumps(headers, indent=2, ensure_ascii=False))
    logging.info("payload: " + json.dumps(payload, indent=2, ensure_ascii=False))
    response = ""
    while rerty > 0:
        try:
            response = requests.request(method, url, headers=headers, data=payload).json()
            # logging.info(response)
            if response.get("err_no") == 0 and response.get("err_msg"):
                return response
            else:
                logging.warning("Request URL: " + url + " failed and rerty ... with res is " + str(response))
                rerty += -1
        except Exception as err:
            logging.warning(err)
            logging.warning("Request URL: " + url + " failed and rerty ... with res is " + str(response))
            rerty += -1

    return response
