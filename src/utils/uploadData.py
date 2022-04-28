import json
import requests
import time

'''
模拟上传温湿度信息等
'''

def getToken():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
    }

    url = 'http://127.0.0.1:5000/user/login'

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

    url = 'http://127.0.0.1:5000/produce_th'

    data = {
        "user_id": 'admin',
        "area_id": 1,
        "batch": 1,
        "temp": 10,
        "hum": 20,
    }

    response = requests.post(headers=headers, url=url, json=data).text
    print(json.loads(response))


def get_out_blocks(token):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        "Authorization": token
    }

    url = 'http://127.0.0.1:5000/blockchain/out-chain'

    response = requests.get(headers=headers, url=url).text
    return json.loads(response)


'''
可以在运输类中引用，让添加物流状态为已到货时调用此方法自动添加区块
'''
def add_block(token, data):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        "Authorization": token
    }

    url = 'http://127.0.0.1:5000/blockchain'

    response = requests.post(headers=headers, url=url, json=data)
    if response.status_code == 500:
        print(data)


def auto_add_block():
    token = getToken()
    while True:
        try:
            time.sleep(60000)
            data = get_out_blocks(token)
            if len(data) > 0:
                add_block(token, data)
        except Exception:
            token = getToken()


def auto_add_th():
    token = getToken()
    while True:
        try:
            time.sleep(1800000)
            addTH(token)
        except Exception:
            token = getToken()



if __name__ == '__main__':
    auto_add_block()