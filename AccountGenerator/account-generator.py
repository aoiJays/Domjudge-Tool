import csv
import os
import shutil

def process_csv(path, output_path):
    
    # 打开 CSV 文件
    with open(path, mode='r', newline='', encoding='utf-8') as file:
        
        print('============================================================')
        print(f'\tstart to process {path}\t\t')
        print('============================================================')
              
        reader = csv.reader(file)

        # CSV文件标题行
        headers = next(reader, None)
        if headers is None:
            print(f'{path} lacks of headers')
            return
        
        data = [ row for row in reader ]

    file_name, _ = os.path.splitext(path)
    file_name = os.path.basename(os.path.normpath(file_name))

    output_path = os.path.join(output_path, file_name)
    os.mkdir(output_path)
    
    # teams.tsv
    with open(os.path.join(output_path, 'teams.tsv'), 'w', encoding='utf-8') as file:
        file.write('teams\t1\n')
        # 1    external_ID    group_id    team_name    institution_name    institution_short_name    country_code
        for team in data:
            # institution_name与institution_short_name导入后的分类结果不行
            # 建议直接通过定义Categories去分类
            # 这里直接留空
            context = f'{team[0]}\t{team[1]}\t{team[3]}\t{team[-2]}-{team[2]}\t{""}\t{""}\t\n'
            file.write(context)
    
    # accounts.tsv
    with open(os.path.join(output_path, 'accounts.tsv'), 'w', encoding='utf-8') as file:
        file.write('accounts\t1\n')
        # account_type	fullname	username	password
        for team in data:
            context = f'team\t{team[-2]}-{team[2]}\t{team[1]}\t{team[-1]}\n'
            file.write(context)



if __name__ == '__main__':
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'output')
    
    # 创建输出文件
    if os.path.exists(output_path): shutil.rmtree(output_path)
    os.mkdir(output_path)

    list_dir = os.path.join(script_dir, 'list')
    if not os.path.exists(list_dir):
        print('fail to find list')
        exit(0)


    # 获取文件夹中所有的文件和目录
    with os.scandir(list_dir) as entries:
        for entry in entries:
            # 检查是否是文件并且以 .csv 结尾
            if entry.is_file() and entry.name.endswith('.csv'):
                process_csv(entry.path, output_path)