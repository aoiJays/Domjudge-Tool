import requests

'''
使用这个api需要以下权限：
Administrative User
API reader
API writer
Source code reader
'''

def getJudgementsList(base_url, cid, username, password):
    url = '{}api/v4/contests/{}/judgements?strict=false'.format(base_url, cid)
    response = requests.get(url, auth=(username, password))
    return response.json()