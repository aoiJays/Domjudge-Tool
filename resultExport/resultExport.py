'''
只能get到Contest visible on public scoreboard为true的比赛
并且不能封榜单
'''


import json
import os
import shutil
from domjudge.teams import  getTeam
from domjudge.scoreboard import getScoreboard

def read_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)

        url = config.get('url', '')
        cid = config.get('contest', '')
        cds_username = config.get('cds-username', '')
        cds_passwd = config.get('cds-passwd', '')

        # 返回一个包含所有信息的字典
        return url, cid, cds_username, cds_passwd

    except Exception as e:
        print(f"Error reading config file: {e}")
        exit(0)


if __name__ == "__main__":

    script_dir = os.path.dirname(os.path.realpath(__file__))
    url, cid, username, passwd = read_config(os.path.join(script_dir, 'config.json'))

    scoreboard = getScoreboard(url, cid)["rows"]

    # 创建输出文件
    output_path = os.path.join(script_dir, 'output')
    if os.path.exists(output_path): shutil.rmtree(output_path)
    os.mkdir(output_path)

    with open(os.path.join(output_path, 'scoreboard.csv'), 'w') as file:
        file.write('rk,name,categories,num_solved,total_time\n')

        for team in scoreboard:
            rk, num_solved, total_time, team_id = team["rank"], team["score"]["num_solved"], team["score"]["total_time"], team["team_id"]
            team_info = getTeam(url, cid, team_id, username, passwd)

            team_name = team_info["name"]
            categories = team_info['group_ids'][0]

            file.write(f'{rk},{team_name},{categories},{num_solved},{total_time}\n')
