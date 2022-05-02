import json
import requests
import time
import random


base_url = 'http://10.4.7.250:5000'
user_id = '62912edebb1611eca41d1cbfc0eb0cdc'

'''
模拟上传温湿度信息等
'''

def getToken():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
    }

    url = base_url + '/user/login'

    data = {
        "username": "admin",
        "password": '123456'
    }

    response = requests.post(headers=headers, url=url, json=data).text
    res = json.loads(response)
    token = res['data']['token']
    return token


def addTH(token):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        "Authorization": token
    }

    url = base_url +'/produce_th'

    data = {
        "user_id": user_id,
        "area_id": 1,
        "batch": 1,
        "temp": random.uniform(0, 30),
        "hum": random.uniform(70, 95),
    }

    response = requests.post(headers=headers, url=url, json=data).text
    print('上传成功:', '温度为:', data['temp'], '湿度为:', data['hum'])
    # print(json.loads(response))




if __name__ == '__main__':
    token = getToken()
    while True:
        time.sleep(900)
        print("---------------上传温湿度----------------")
        try:
            addTH(token)
        except Exception:
            print('上传失败')
            token = getToken()