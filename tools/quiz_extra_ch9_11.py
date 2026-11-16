# -*- coding: utf-8 -*-
"""补 ch9-11 老师更新版代码的代码自测题。

第 9-11 章换成「更新后的chapter」之后，build_code_lab.py 会跳过 QUIZ 里这几章的旧题
（旧题的内联代码和老师改过的文件已经对不上），这里补上按新代码出的题。

约定（与 build_code_lab.build_quiz 一致）：
- ans = 正确选项在 options 里的下标（构建时会做确定性轮转）
- run=True 时用 expected / expect_in 和真实 stdout 比对，verified 才为真
- run=False 用于没法真跑的（写绝对路径、改了文件内容）
"""
import json

P = 'tools/source/quiz_extra.json'
extra = json.load(open(P, encoding='utf-8'))

new = [
    # ---------------- 第 9 章 ----------------
    dict(
        ch=9, file='test6.py', kind='output',
        code=('try:\n'
              '    result = 10 / 2\n'
              'except Exception as error:\n'
              '    print("出错了,原因是：", error)\n'
              'else:\n'
              '    print(result)\n'
              'finally:\n'
              '    print("今天天气不错！")\n'),
        stem='【读结果】老师这版把计算挪到 try、打印挪进 else，这段代码的输出是？',
        options=['5.0 换行 今天天气不错！',
                 '结果为 5.0 换行 今天天气不错！',
                 '出错了,原因是： 5.0 换行 今天天气不错！',
                 '今天天气不错！'],
        ans=0,
        expl='10/2 正常完成，跳进 else 打印 result（5.0），finally 随后无条件执行。注意输出的 5.0 前面没有「结果为」三个字 —— 那是旧版 print 里的字符串。',
        expected='5.0\n今天天气不错！', run=True,
    ),
    dict(
        ch=9, file='test10.py', kind='error',
        code=("try:\n"
              "    raise IndexError('索引超出范围')\n"
              "#except Exception as error:\n"
              "except:\n"
              "    #pass\n"
              "    raise\n"),
        stem='【判行为】except 里先把 #pass 注释掉、只留 raise，运行结果是？',
        options=['抛出 IndexError: 索引超出范围，程序终止',
                 '打印「索引超出范围」后正常结束',
                 '什么都不发生，程序正常结束',
                 'SyntaxError，raise 不能单独使用'],
        ans=0,
        expl='不带参数的 raise 表示「把当前正在处理的异常原样再抛」，所以接住之后程序仍然崩。老师把 #pass 留成注释，就是在提示：如果它是真的 pass，就会静默通过。',
        run=False,
    ),
    # ---------------- 第 10 章 ----------------
    dict(
        ch=10, file='test10.py', kind='output',
        code=('lines = ["1,2,3,4\\n", "5,6,7,8\\n"]\n'
              'ls = []\n'
              'for l in lines:\n'
              "    ls.append(l.strip('\\n').split(','))\n"
              'print(ls)\n'),
        stem='【读结果】readlines 拿到的每一行再逐行 strip + split，输出是？（lines 就相当于 readlines() 的返回值）',
        options=["[['1', '2', '3', '4'], ['5', '6', '7', '8']]",
                 "['1', '2', '3', '4', '5', '6', '7', '8']",
                 "[['1,2,3,4'], ['5,6,7,8']]",
                 "['1,2,3,4\\n', '5,6,7,8\\n']"],
        ans=0,
        expl='每次循环先 strip 掉行尾换行，再按逗号切成 4 个字段，append 进 ls 后就是「列表的列表」。这正是老师把旧版 read().split(",") 改掉的原因 —— 旧写法分不清行边界。',
        expected="[['1', '2', '3', '4'], ['5', '6', '7', '8']]", run=True,
    ),
    dict(
        ch=10, file='test2.py', kind='mech',
        code=('f = open("test.txt", "a")\n'
              'f.write("Python is a great language 11161338.\\n")\n'
              'f.close()\n'),
        stem='【机制】test.txt 里原来已有两行内容，执行这段代码后文件变成？',
        options=['原来的两行保留，末尾多出一行',
                 '内容被清空，只剩这一行',
                 '报错 FileExistsError，因为文件已存在',
                 '内容被清空，且不写入任何东西'],
        ans=0,
        expl='模式 "a" 是 append：不清空、指针落在文件末尾，所以老内容保留、新内容追加在后。老师这版特意把旧版的 "w" 改成 "a"，就是在演示两者的区别。',
        run=False,
    ),
    dict(
        ch=10, file='test8.py', kind='output',
        code=('from io import StringIO\n'
              'f = StringIO("Python is a great language.")\n'
              'print(f.tell())\n'
              'print(f.read(2))\n'
              'print(f.tell())\n'),
        stem='【读结果】刚打开 → 读 2 个字符 → 再看位置，三次输出依次是？',
        options=['0 / Py / 2', '0 / Py / 3（含换行）', '2 / Py / 2', '1 / Py / 2'],
        ans=0,
        expl='打开时指针在 0；read(2) 读走 P、y 两个字符，指针移到 2。StringIO 的行为和 open 的文本模式完全一致，老师新版正是把 read(5) 改成了 read(2) 好让位置变化一眼可见。',
        expected='0\nPy\n2', run=True,
    ),
    # ---------------- 第 11 章 ----------------
    dict(
        ch=11, file='test1.py', kind='error',
        code=("import os\n"
              "os.mkdir(r'd:\\test\\example3')\n"),
        stem='【找错】假设 d:\\test 这个目录还不存在，只执行这一句会怎样？',
        options=['抛 FileNotFoundError，因为 mkdir 只能建一级、父目录必须已存在',
                 '自动把 d:\\test 和 example3 一起建出来',
                 '什么都不做，路径已存在时不报错',
                 '抛 IsADirectoryError，因为 \\t 被当成制表符'],
        ans=0,
        expl='os.mkdir 只建最后一级，父目录缺一个就 FileNotFoundError；要连父目录一起建得用 os.makedirs(..., exist_ok=True)。老师新版在它前面先 os.mkdir(path) 建了 d:\\test，才让这句能成功。',
        run=False,
    ),
    dict(
        ch=11, file='test6.py', kind='output',
        code=('import calendar\n'
              'print(calendar.firstweekday())\n'
              'calendar.setfirstweekday(6)\n'
              'print(calendar.firstweekday())\n'
              'print(calendar.isleap(2022))\n'),
        stem='【读结果】老师这版把 setfirstweekday(0) 改成了 6，三行输出是？',
        options=['0 / 6 / False', '1 / 6 / False', '0 / 5 / True', '6 / 0 / False'],
        ans=0,
        expl='firstweekday 默认 0（周一），set 成 6 就是周日，读回来自然是 6；2022 不是闰年所以 isleap 返回 False。副作用是后面 calendar.month 的表头会变成 Su Mo Tu We Th Fr Sa。',
        expected='0\n6\nFalse', run=True,
    ),
    dict(
        ch=11, file='test7-1.py', kind='mech',
        code=('from calendar import HTMLCalendar\n'
              'hc = HTMLCalendar()\n'
              'print(type(hc.formatmonth(2026, 11)).__name__)\n'),
        stem='【机制】新增的 test7-1.py 里，formatmonth() 返回的是什么？',
        options=['str（一整段 HTML 表格源码）',
                 'list（每天一个元素）',
                 'None（直接画到屏幕）',
                 'bytes（二进制）'],
        ans=0,
        expl='formatmonth 返回字符串，内容是 <table> … </table> 的 HTML 片段，可以直接写进 .html 文件；想打印出字符画月历要用 calendar.month()。',
        expected='str', run=True,
    ),
    dict(
        ch=11, file='test8.py', kind='output',
        code=('import random\n'
              'random.seed(10)\n'
              'print(random.random())\n'),
        stem='【读结果】老师把 seed(100) 改成 seed(10)，random.random() 的输出变成？',
        options=['0.5714025946899135',
                 '0.1456692551041303（旧 seed(100) 的值）',
                 '每次都不同，无法确定',
                 '10'],
        ans=0,
        expl='种子固定后序列就固定。seed(10) 的第一个随机数是 0.5714025946899135；换回 seed(100) 才是旧笔记里的 0.1456692551041303。',
        expect_in='0.5714025946899135', run=True,
    ),
]

before = len(extra)
extra.extend(new)
with open(P, 'w', encoding='utf-8') as f:
    json.dump(extra, f, ensure_ascii=False, indent=1)
print('quiz_extra: %d -> %d' % (before, len(extra)))
from collections import Counter
print('按章分布:', dict(sorted(Counter(q['ch'] for q in extra).items())))
