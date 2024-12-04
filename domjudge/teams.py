import requests

'''
使用这个api需要以下权限：
Administrative User
API reader
API writer
Source code reader
'''

def getTeam(base_url, cid, tid, username, password):
    url = '{}api/v4/contests/{}/teams/{}?strict=false'.format(base_url, cid, tid)
    response = requests.get(url, auth=(username, password))
    return response.json()

