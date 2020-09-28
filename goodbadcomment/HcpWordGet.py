import pandas as pd
import time
import json
import requests

headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Cookie': 'G_zj_gsid=0000c14f43674814932373db8542e030-gsid-', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

index = 1
df = pd.DataFrame()
while True:
    reqBody = {"pageNum": index, "pageSize": 1000, "startTime": 1571356800000, "endTime": 1596153600000, "affairStartTime": "", "affairEndTime": "", "channelList": [], "areaList": ["ff8080815d551320015d589cc1da0014", "ff8080815d551320015d589cc1da0014$0", "ff8080815df350d4015df3d64603057a", "ff8080815df350d4015df4333f0006cb", "ff8080815df350d4015df44090fd06f5", "ff8080815df350d4015df44e7d100706", "ff8080815de36663015de3e0d0380000", "ff8080815de36663015de3ef492c0015", "ff8080815df45323015df461a0e6000b", "ff8080815df482ba015df7dceec40326", "ff8080815df45323015df46e7610001d", "ff8080815df482ba015df7eb3a8c0367", "ff8080815df45323015df47feebf0116", "ff8080815dfd3779015dfdc8850c06c5", "ff8080815dfc9cb1015dfcf0c19f109f", "bb4a9da3634a58f601636c22dc381288", "bb4a9da3634a58f601636c22583f125b", "ff8080816f12372d016f1d5959bb7545"], "textStatus": 1}

    res = json.loads(requests.post(url = 'https://opt.zjzwfw.gov.cn/rest/api/evaluation/text/audit/list?ctoken=f35c2972-53b6-408c-b4a8-1cac8b51bd78', json=reqBody, headers = headers).text)
    if not res['data']['list']:
        break
    df = df.append(pd.DataFrame(res['data']['list']), ignore_index=True)
    index += 1
    time.sleep(1)

df.to_excel('好差评结果.xls', index=False)

print(res)

