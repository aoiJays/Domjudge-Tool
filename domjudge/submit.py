import requests
import os


'''
获取文件后缀名
'''
def get_file_extension(filename):
    # 使用os.path.splitext()分离文件名和扩展名
    base_name, extension = os.path.splitext(filename)
    return extension

'''
base_url, cid, username, password, problem, file_path
domjudge地址 比赛id
用户名 密码 题目id 代码地址 

sumbit(
    'http://10.199.227.101/',
    2,
    "dummy", "dummy",
    1, "./submission/1.cpp"
)


'''

def sumbit(base_url, cid, username, password, problem, file_path):

    url = '{}api/v4/contests/{}/submissions'.format(base_url, cid)

    lan = get_file_extension(file_path)
    if lan == '.cpp': lan = 'cpp'
    if lan == '.c': lan = 'c'
    if lan == '.py': lan = 'python3'
    if lan == '.java': lan = 'java'

    data = {
        'problem': problem,
        'language': lan,
    }

    print(f'Submit {file_path} to contest {cid} problem {problem} by {lan}' )
    with open(file_path, 'rb') as f:
        files = {'code[]': f}
        response = requests.post(url, data=data, files=files, auth=(username, password))

    if response.status_code == 200:
        print('Submission successful')
    else:
        print('Failed to submit')

    return response.status_code == 200