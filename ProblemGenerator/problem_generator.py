import os
import shutil
import json

def read_config(config_path):
    try:
        # 打开并读取JSON配置文件
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config_data = json.load(config_file)

        # 获取配置项
        title = config_data.get('title', None)
        timelimit = config_data.get('timelimit', None)
        memory = config_data.get('memory', None)

        return title, timelimit, memory

    except FileNotFoundError:
        print(f"The specified configuration file '{config_path}' does not exist.")
        return None, None, None
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from the file '{config_path}'.")
        return None, None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None, None

def data_checker(data_entries):

    # 数据没有一一对应
    if len(data_entries) % 2 == 1: return False

    # 检查数据
    for i in range(0, len(data_entries), 2):

        ans_file, in_file = data_entries[i], data_entries[i + 1]

        ans_base_name, ans_extension = os.path.splitext(ans_file)
        in_base_name, in_extension = os.path.splitext(in_file)

        # 检查数据后缀名
        if ans_extension != '.ans': return False
        if in_extension != '.in': return False

        # 检查对应关系
        if ans_base_name != in_base_name: return False
    return True

def create_file_with_content(path, file_name, content):
    try:
        # 构建完整的文件路径
        full_path = os.path.join(os.path.abspath(path), file_name)

        # 确保目标目录存在，如果不存在则创建
        os.makedirs(path, exist_ok=True)

        # 使用with语句打开文件进行写入操作
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(content)

        return True

    except Exception as e:
        print(f"An error occurred while creating the file: {e}")
        return False

if __name__ == "__main__":

    print('--------start to generate problem file--------')

    script_dir = os.path.dirname(os.path.abspath(__file__))
    problem_path = os.path.join(script_dir, 'problems')

    if not os.path.exists(problem_path):
        print(f"The folder '{problem_path}' does not exist.")
        exit(0)

    # 列出题目列表
    entries = os.listdir(problem_path)
    problems = [entry for entry in entries if os.path.isdir(os.path.join(problem_path, entry))]
    problems.sort()
    if len(problems) == 0:
        print('problems is null. script exited. ')
        exit(0)

    # 检查'output'文件夹是否存在
    output_path = os.path.join(script_dir, 'output')
    # 如果存在先删除一下
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    # 重新建立
    os.mkdir(output_path)

    # 输出题目列表
    print(f'{len(problems)} problems found.')
    for problem in problems: print(problem)

    # 生成domjudge题目zip包
    for problem in problems:
        print(f'--------start processing {problem}--------')

        # 检查config.json
        config_path = os.path.join(problem_path, problem, 'config.json')
        if not os.path.exists(config_path):
            print(f'{problem} config file does not exist.')
            continue

        title, timelimit, memory = read_config(config_path)
        if title is not None and timelimit is not None and memory is not None:
            print(f"Title: {title}")
            print(f"Time Limit: {timelimit} seconds")
            print(f"Memory Limit: {memory} MB")
        else:
            print(f'{problem} Config content is missing')
            continue

        # 检查题目PDF文件
        problem_pdf_path = os.path.join(problem_path, problem, 'problem.pdf')
        if not os.path.exists(problem_pdf_path):
            print(f'{problem} PDF file does not exist.')
            continue

        # 检查题目data
        data_path = os.path.join(problem_path, problem, 'data')
        if not os.path.exists(data_path):
            print(f'{problem} data file does not exist.')
            continue

        # 数据列表
        data_entries = os.listdir(data_path)
        data_entries.sort()
        if not data_checker(data_entries):
            print('data entries is not correct.')
            continue

        # 交互题查找
        interactor_path = os.path.join(problem_path, problem, 'interactor.cpp')
        if not os.path.exists(interactor_path): interactor_path = None
        else: print('interactor file exists. ')

        # spj查找
        spj_path = os.path.join(problem_path, problem, 'checker.cpp')
        if not os.path.exists(spj_path): spj_path = None
        else: print('spj file exists. ')



        # 生成题目zip
        ## 创建临时工作区
        workplace_path = os.path.join(script_dir, '.workplace')
        if os.path.exists(workplace_path): shutil.rmtree(workplace_path)
        os.mkdir(workplace_path)

        ### data
        '''
            domjudge 数据格式：
            - data
                - secret
                    - x.in
                    - x.ans
                - sample(这里不做了 意义不大 数据够多的话)
                    ...
        '''
        os.mkdir(os.path.join(workplace_path, 'data'))
        shutil.copytree(data_path, os.path.join(workplace_path, 'data', 'secret'))

        ### 题目文件pdf
        shutil.copy(problem_pdf_path, os.path.join(workplace_path, 'problem.pdf'))

        ### SPJ 文件
        if spj_path is not None:

            os.mkdir(os.path.join(workplace_path, 'output_validators'))
            spj_file_path = os.path.join(workplace_path, 'output_validators','validate')
            os.mkdir(spj_file_path)

            shutil.copy( os.path.join(script_dir, 'testlib.h'), os.path.join(spj_file_path, 'testlib.h'))
            shutil.copy( spj_path, os.path.join(spj_file_path, 'checker.cpp'))
        elif interactor_path is not None:
            os.mkdir(os.path.join(workplace_path, 'output_validators'))
            interactor_file_path = os.path.join(workplace_path, 'output_validators','validate')
            os.mkdir(interactor_file_path)

            shutil.copy( os.path.join(script_dir, 'testlib.h'), os.path.join(interactor_file_path, 'testlib.h'))
            shutil.copy( interactor_path, os.path.join(interactor_file_path, 'interactor.cpp'))

        ### domjudge-problem.ini
        domjudge_problem_ini = f"timelimit='{timelimit}'"
        create_file_with_content(workplace_path, 'domjudge-problem.ini', domjudge_problem_ini)

        ### problem.yaml
        validation = 'validation: custom' if spj_path is not None else ""
        if interactor_path is not None: validation = 'validation: custom interactive'
        
        problem_yaml = f'''
name: '{title}'
{validation}
limits:
  memory: {memory}
'''
        create_file_with_content(workplace_path, 'problem.yaml', problem_yaml)

        ### 打包zip(不要中文)
        shutil.make_archive(os.path.join(output_path, f'{problem}'), 'zip', workplace_path)

        ## 删除临时工作区
        if os.path.exists(workplace_path): shutil.rmtree(workplace_path)

        print(f'Finished generating problem file {problem}')
