# Domjudge-Tool
> 一些准备校赛时候留下来的Python脚本

## ProblemGenerator
> 出题人一般都是懒狗，只会丢一堆奇怪的数据和标程发给我们

使用的`testlib.h`默认用的都是文件夹下的那一份，如果想换的话直接换掉就好

具体看一下sample

- problems：对于每道题你需要新建一个子题目文件夹，把需要的东西放到文件夹里
  - data:所有的数据请命名为`.in`和`.ans`，全部丢在这里即可
  - problem.pdf：题面放在子文件夹下
  - config.json：填写题目显示名
    - title：题目名（字符串，例如：'背包问题' ）
    - timelimit：时限（单个数字，单位是秒，例如：2.5）
    - memory：空间限制（单个数字，单位是M，例如：512）
  - 如果有SPJ，请命名为`checker.cpp`也放在子文件夹里（没有找到spj文件默认传统题目）
  - 如果是交互题，请命名为`interactor.cpp`也放在子文件夹里（没有找到交互文件默认传统题目）
  
```bash
python problem_generator.py
```
生成的题目文件zip文件在`output`底下


## AccountGenerator
> 用于生成账号

先在domjudge系统`domjudge/jury/categories`创建好队伍分类，方便管理，记好每个分类的id

在`AccountGenerator/list/`创建一个或多个csv文件

需要的信息如下：`id,tid,name,Categories,info,passwd`
- id：编号（不能够与以往的数据重复）
- tid：登陆账号id，序号或者座位号
- name：队伍名（选手名）
- Categories：账号分类，用于系统管理
- info：学校名/班级名，用于榜单分类
- passwd：密码

```bash
python AccountGenerator/account-generator.py
```

输出在`output`

在OJ后台`domjudge/jury/import-export`导入即可

在Tab-separated import
- Type选择team, 先导入teams.tsv
- Type选择account, 先导入accounts.tsv


## Submit

当你已经导入完题目、测试账号时，肯定需要交一发正解测试一下

在`Submit`文件夹下修改`config.json`

```json
{
  "url": "http://10.199.227.101/",
  // 比赛url
  "contest": 3,
  // 比赛id 在jury界面查看
  // 题目编号列表 最好是按照abcde顺序
  "problems": ["19","20","21","22","23","24","25","26","27","28","29"],
  
  // 执行交题程序的账号列表
  "users": [
    "validtor01","validtor02","validtor03","validtor04","validtor05",
    "validtor06","validtor07","validtor08","validtor09","validtor10"
  ],
  // 执行交题程序的密码列表，与账号对应
  "passwd": [
    "lqsauv","lqsauv","lqsauv","lqsauv","lqsauv",
    "lqsauv","lqsauv","lqsauv","lqsauv","lqsauv"
  ],
  "rounds": 1, // 提交轮次（每题会被提交rounds遍 可以测试服务器）
  "speed": 3, // 交题速度 每交一次题 有1/speed的概率sleep 1s
  "catogory": "ac" // 只交ac代码（"others"只交错误代码 "all"全部交）
}

```
在`Submit/submissions`文件夹下添加对应题号的文件夹：
以题目19为例，我们在其对应文件夹下新建2个子文件夹：
- ac：把对应题目的应该ac的代码放在这里即可
- others：不能ac的题目放到这里

```plain
.
├── Submit.py
├── config.json
└── submissions
    ├── 19
    │         ├── ac
    │         └── others
    ├── 20
    │         ├── ac
    │         └── others

```

```bash
python Submit/Submit.py 
```

## CodeExport

赛后需要导出选手代码，或是验题后导出所有验题程序

```json
{
  "url": "http://ip/", // url
  "cid": 3, // 导出的比赛
  "cds-username": "cds", // 必须拥有admin权限的账号
  "cds-passwd": "cds",
  "category": "problem" // 按题目分类（team 按队伍分类）
}
```

```bash
python CodeExport/codeExport.py
```
输出结果在`output`中
