import json

import requests
# status = "free"
# # start = "free"
# params = {"msg": "start"}
# payload = {'status': 'free'}
# payload1 = {'value': False}
# resp = requests.post("http://192.168.101.254:8056/status", params=payload)
# resp2 = requests.post("http://192.168.101.254:8056/start", params=payload1)
# print(resp.text)
# print(resp.url)
# resp1 = requests.get("http://192.168.101.254:8056/status")
# resp3 = requests. get("http://192.168.101.254:8056/start")
# # resp2 = requests.get("http://192.168.101.254:8056/start")
# resp4 = requests.get("http://192.168.101.254:8056/recipe")
# print(resp1.text)
# # print(resp2.text)
# print(resp3.text)
# print(resp4.text)


def test_1():
    return requests.post("http://192.168.101.51/recipe", json=[])


test_1()
print(requests.get("http://192.168.101.51/recipe").text)
if not json.loads(requests.get("http://192.168.101.51/recipe").text):
    print('xyi')