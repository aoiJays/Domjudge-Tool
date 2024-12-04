import json
import os
import argparse
import shutil

from domjudge.submissions import getSubmission, getCode
from domjudge.judgements import getJudgementsList
from domjudge.teams import getTeam

def read_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)

        # 提取所需的数据
        url = config.get('url', '')
        cid = config.get('cid', '')
        cds_username = config.get('cds-username', '')
        cds_passwd = config.get('cds-passwd', '')
        cat = config.get('category', '')
        # 返回一个包含所有信息的字典
        return url, cid, cds_username, cds_passwd, cat

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(0)


def sortByTeam(url, cid, cds_username, cds_passwd, output_path):
    judgements = getJudgementsList(url, cid, cds_username, cds_passwd)

    judgements_size = len(judgements)
    cnt = 0

    for judgement in judgements:

        submission_id = judgement['submission_id']
        status = judgement['judgement_type_id']
        submission = getSubmission(url, cid, submission_id, cds_username, cds_passwd)

        team_id = submission['team_id']
        problem = submission['problem_id']
        language = submission['language_id']

        code = getCode(url, cid, submission_id,cds_username, cds_passwd)
        team = getTeam(url, cid, team_id, cds_username, cds_passwd)
        team_name = team['name']

        # 判断是否创建队伍文件夹
        team_path = os.path.join(output_path, team_name)
        if not os.path.exists(team_path): os.makedirs(team_path)

        # 判断是否创建文件夹
        problem_path = os.path.join(team_path, problem)
        if not os.path.exists(problem_path):
            os.makedirs(problem_path)
            os.mkdir(os.path.join(problem_path, 'ac')) # ac代码
            os.mkdir(os.path.join(problem_path, 'others')) # un ac 代码

        if status == 'AC':
            with open(os.path.join(problem_path, 'ac', f'{submission_id}.{language}'), 'wb') as file:
                file.write(code)
        else:
            with open(os.path.join(problem_path, 'others', f'{submission_id}.{language}'), 'wb') as file:
                file.write(code)

        cnt += 1
        print(f'finished {cnt}/{judgements_size}')

def sortByProblem(url, cid, cds_username, cds_passwd, output_path):

    judgements = getJudgementsList(url, cid, cds_username, cds_passwd)
    judgements_size = len(judgements)
    cnt = 0


    for judgement in judgements:

        submission_id = judgement['submission_id']
        status = judgement['judgement_type_id']
        submission = getSubmission(url, cid, submission_id, cds_username, cds_passwd)

        problem = submission['problem_id']
        language = submission['language_id']

        code = getCode(url, cid, submission_id,cds_username, cds_passwd)

        # 判断是否创建题目文件夹
        problem_path = os.path.join(output_path, problem)
        if not os.path.exists(problem_path):
            os.makedirs(problem_path)
            os.mkdir(os.path.join(problem_path, 'ac')) # ac代码
            os.mkdir(os.path.join(problem_path, 'others')) # un ac 代码

        if status == 'AC':
            with open(os.path.join(problem_path, 'ac', f'{submission_id}.{language}'), 'wb') as file:
                file.write(code)
        else:
            with open(os.path.join(problem_path, 'others', f'{submission_id}.{language}'), 'wb') as file:
                file.write(code)

        cnt += 1
        print(f'finished {cnt}/{judgements_size}')

if __name__ == '__main__':

    script_dir = os.path.dirname(os.path.realpath(__file__))
    url, cid, cds_username, cds_passwd, cat = read_config(os.path.join(script_dir, 'config.json'))

    print('start to process', url, cid, cds_username, cds_passwd, '\nsort by', cat)

    # 创建输出文件
    output_path = os.path.join(script_dir, 'output')
    if os.path.exists(output_path): shutil.rmtree(output_path)
    os.mkdir(output_path)

    if cat == 'team': sortByTeam(url, cid, cds_username, cds_passwd, output_path)
    elif cat == 'problem': sortByProblem(url, cid, cds_username, cds_passwd, output_path)