import pandas as pd
import time
import json
import requests
import tqdm

headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Cookie': 'G_zj_gsid=3df3a355fdec42a7a939e90893e6e9d5-gsid-', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

index = 1
df = pd.DataFrame()
while True:
    reqBody = {"pageNum": index, "pageSize": 1000, "createTimeFrom": 1577836800000, "createTimeTo": 1600992000000, "channelList": [], "areaList": ["ff8080815d551320015d589cc1da0014", "ff8080815d551320015d589cc1da0014$0", "ff8080815df350d4015df3d64603057a", "ff8080815df350d4015df4333f0006cb", "ff8080815df350d4015df44090fd06f5", "ff8080815df350d4015df44e7d100706", "ff8080815de36663015de3e0d0380000", "ff8080815de36663015de3ef492c0015", "ff8080815df45323015df461a0e6000b", "ff8080815df482ba015df7dceec40326", "ff8080815df45323015df46e7610001d", "ff8080815df482ba015df7eb3a8c0367", "ff8080815df45323015df47feebf0116", "ff8080815dfd3779015dfdc8850c06c5", "ff8080815dfc9cb1015dfcf0c19f109f", "bb4a9da3634a58f601636c22dc381288", "bb4a9da3634a58f601636c22583f125b", "ff8080816f12372d016f1d5959bb7545"], "statusList": []}
    res = json.loads(requests.post(url = 'https://opt.zjzwfw.gov.cn/rest/api/evaluation/case/historyForHandle/list?ctoken=f35c2972-53b6-408c-b4a8-1cac8b51bd78', json=reqBody, headers = headers).text)
    if not res['data']['list']:
        break

    df = df.append(pd.DataFrame(res['data']['list']), ignore_index=True)
    index += 1
    time.sleep(0.5)

df.to_excel('好差评结果.xls', index=False)


df = pd.read_excel('好差评结果.xls', dtype=str)
resDf = pd.DataFrame()

process = tqdm.tqdm(total=df.shape[0])

for idx, row in df.iterrows():
    res = json.loads(requests.get(url='https://opt.zjzwfw.gov.cn/rest/api/evaluation/detail?ctoken=f35c2972-53b6-408c-b4a8-1cac8b51bd78&id={}&isQueryCaseInfo=true&portalTyp=G'.format(row['evaluationId']), headers=headers).text)['data']

    #申诉理由
    appealReason = res['caseDTO']['appealReason']

    #驳回理由
    failedReason = res['caseDTO']['failedReason']

    #差评人联系方式
    phone = res['raterInfoDTO']['phoneNum']

    #整改理由
    solution = res['caseDTO']['solution']
    row['申诉理由'] = appealReason
    row['驳回理由'] = failedReason
    row['整改回复'] = solution
    row['差评联系人手机'] = phone

    resDf = resDf.append(row)
    time.sleep(0.3)
    process.update(1)


process.close()
resDf.to_excel('差评信息.xls', index=False)


