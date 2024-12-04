import requests

'''
只能get到Contest visible on public scoreboard为true的比赛
并且不能封榜单
'''
def getScoreboard(base_url, cid):
    url = '{}api/v4/contests/{}/scoreboard'.format(base_url, cid)
    response = requests.get(url)
    return response.json()

