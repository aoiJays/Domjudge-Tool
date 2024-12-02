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