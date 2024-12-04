import argparse
import json
import os


from domjudge.submissions import submit
from random import randint
from time import sleep

def read_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)

        # 提取所需的数据
        users = config.get('users', [])
        passwd = config.get('passwd', [])
        problems = config.get('problems', [])
        url = config.get('url', '')
        cid = config.get('contest', '')
        catogory = config.get('catogory', '')
        rounds = config.get('rounds', 1)
        speed = config.get('speed', 10)

        # 返回一个包含所有信息的字典
        return users, passwd, problems, url, cid, catogory, rounds, speed

    except Exception as e:
        print(f"Error reading config file: {e}")
        exit(0)


def get_codes(problem, path):
    res = []
    if not os.path.exists(path): return []
    with os.scandir(path) as entries:
        for entry in entries:
            if not entry.is_file(): continue
            res.append((problem, entry.path))

    return res

if __name__ == "__main__":

    # 加载config.json
    script_dir = os.path.dirname(os.path.abspath(__file__))
    users, passwd, problems, url, cid, catogory, rounds, speed= read_config(os.path.join(script_dir, 'config.json'))
    print(f'评测模式:{catogory}\n评测轮次:{rounds}\n每10s均提交{speed}')

    # 获取所有代码文件路径
    code_source = []

    for problem in problems:
        problem_path = os.path.join(script_dir, 'submissions', problem)

        if catogory == 'ac' or catogory == 'all':
            ac_path = os.path.join(problem_path, 'ac')
            ac_code = get_codes(problem, ac_path)
            code_source.extend(ac_code)

        if catogory == 'others' or catogory == 'all':
            others_path = os.path.join(problem_path, 'others')
            others_code = get_codes(problem, others_path)
            code_source.extend(others_code)


    print('total submit:', len(code_source))
    for round in range(rounds):

        cnt = 0
        for code in code_source:

            if randint(1, speed  ) == 1: sleep(1)

            id = randint(0, len(users) - 1)
            uid, pwd = users[id], passwd[id]

            print(f'round {round}/{rounds} {cnt}/{len(code_source)}')
            submit(url, cid, uid, pwd, code[0], code[1])

