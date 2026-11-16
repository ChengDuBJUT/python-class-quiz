# -*- coding: utf-8 -*-
"""生成「考纲对照」页所需的数据。

把 2026-11 老师公布的考纲（题型分值 + 20 个考点 + 三类必考编程题）
和题库里的实际题量对起来，算出每个考点的覆盖情况，输出 data/syllabus.js。

覆盖数由脚本现算，不手写数字，所以补完题重新跑一次就能看到数字变化。

用法：python tools/build_syllabus.py
"""
import json
import os
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(BASE, 'data', 'questions.json')
EXTRA = os.path.join(BASE, 'tools', 'source', 'exam_extra.json')
OUT = os.path.join(BASE, 'data', 'syllabus.js')

# 编程题考纲范围（与 build_bank.py 的 EXAM_CODE_CHAPS 保持一致）
EXAM_CODE_CHAPS = {1, 2, 3, 4, 5, 6, 7, 8, 10}

TEMPLATES = [
    {
        'key': 'file',
        'name': '文件读写',
        'must': True,
        'why': '考纲原文「编程题必考一道文件」。分值 5 分，但它是唯一能稳定拿分的模板题——'
               '四个动作（打开 → 读/写 → 处理 → 关闭）背下来就能套。',
        'code': 'with open("test.txt", "r", encoding="utf-8") as f:\n'
                '    text = f.read()          # 全部读成字符串\n'
                '    # f.readline()   读一行\n'
                '    # f.readlines()  读全部行 → 列表\n'
                'print(text)\n'
                '\n'
                'with open("out.txt", "w", encoding="utf-8") as f:\n'
                '    f.write("要写的内容\\n")  # 写字符串，换行要自己加\n',
        'points': [
            '模式：r 只读（文件必须存在）/ w 清空重写 / a 追加末尾',
            'with 会自动 close，不写 with 就必须手动 f.close()',
            'read(n) 读 n 个字符；readlines() 返回列表且每行带 \\n，要 strip()',
            'write() 只能写字符串，写数字要先 str()；写 CSV 用 ",".join(row) + "\\n"',
            '中文一定要写 encoding="utf-8"，Windows 默认 GBK 会乱码',
        ],
    },
    {
        'key': 'recursion',
        'name': '递归',
        'must': True,
        'why': '考纲原文「编程题必考一道递归」。判分主要看有没有写对出口和递推式，'
               '再加一句"参数每次都朝出口靠近"就完整了。',
        'code': 'def fact(n):\n'
                '    if n == 1:                  # ① 终止条件（递归出口）\n'
                '        return 1\n'
                '    return n * fact(n - 1)      # ② 递推：把问题缩小一层\n'
                '\n'
                'print(fact(5))                  # 120\n',
        'points': [
            '三件套：出口 + 递推式 + 参数向出口收敛，缺一样就不是递归',
            '常见变式：阶乘、1..n 求和、斐波那契、汉诺塔、快排、字符串反转',
            '没有出口 → RecursionError: maximum recursion depth exceeded',
            'Python 默认递归深度约 1000 层，规模大要改循环或加记忆化',
        ],
    },
    {
        'key': 'base',
        'name': '数制转换',
        'must': True,
        'why': '考纲原文「…以及数进制的转换」。两种写法都要会：'
               '调内置函数（一行解决）和手写"除基取余"（考算法思路时用）。',
        'code': 'n = 26\n'
                'print(bin(n), oct(n), hex(n))   # 0b11010 0o32 0x1a\n'
                'print(bin(n)[2:])               # 11010  （切掉 0b 前缀）\n'
                'print(int("11010", 2))          # 26     （按二进制解释字符串）\n'
                '\n'
                'def to_base(n, base):           # 手写：除基取余\n'
                '    digits = "0123456789ABCDEF"\n'
                '    if n < base:\n'
                '        return digits[n]\n'
                '    return to_base(n // base, base) + digits[n % base]\n',
        'points': [
            'bin/oct/hex 返回的是带前缀的字符串，不能直接参与算术运算',
            'int(字符串, 进制) 是反方向：int("2F", 16) = 47',
            '除基取余 = 反复 %基数 得余数、//基数 缩小，余数要倒着读',
            '十六进制里 A~F 代表 10~15',
        ],
    },
]

# 20 个考点（老师考纲原文的列举顺序），mode=chapter 表示整章都算该考点
TOPICS = [
    ('feature', 'Python 特性', [1], 'chapter', []),
    ('encoding', '编码方式', [2, 3], 'kw', ['编码', 'utf-8', 'gbk', 'ascii', '字节', 'encode', 'decode']),
    ('dtype', '数据类型', [3, 6], 'chapter', []),
    ('control', '控制结构', [5], 'chapter', []),
    ('output', '输出', [2, 3, 6], 'kw', ['print', '输出', 'format', 'f-string', '格式化', '%d', '%s']),
    ('logic', '判断逻辑', [4, 5], 'chapter', []),
    ('func', '函数', [7], 'chapter', []),
    ('scope', '变量（局部/全局）', [7, 2], 'kw', ['局部', '全局', 'global', 'nonlocal', '作用域']),
    ('oop', '面向对象特征', [8], 'chapter', []),
    ('clsmethod', '类方法', [8], 'kw', ['classmethod', '类方法', 'cls']),
    ('objmethod', '对象方法', [8], 'kw', ['self', '实例方法', '对象方法']),
    ('exception', '异常', [9], 'chapter', []),
    ('recursion', '函数嵌套递归', [7], 'kw', ['递归', '嵌套', '闭包', '阶乘', 'fib']),
    ('file', '文件读取关闭', [10], 'kw', ['open', 'read', 'write', 'close', '文件', 'csv']),
    ('import', '导入模块', [1, 2, 11], 'kw', ['import', '模块', '包']),
    ('indent', '缩进', [2], 'kw', ['缩进', 'tab']),
    ('namespace', '命名空间', [2, 7, 8], 'kw', ['命名空间', 'namespace', 'legb', '内置']),
    ('object', '对象', [2, 8], 'kw', ['对象']),
    ('state', '状态', [2, 8], 'kw', ['状态', '属性', '__dict__']),
    ('base', '数制转换', [3], 'kw', ['进制', 'bin(', 'oct(', 'hex(', '二进制', '八进制', '十六进制']),
]

OBJ_TYPES = ('single', 'blank', 'judge', 'short')


def text_of(q):
    parts = [q.get('stem') or '']
    parts += [str(x) for x in (q.get('options') or [])]
    for k in ('answer', 'answerText', 'explanation', 'code'):
        v = q.get(k)
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, list):
            parts += [str(x) for x in v]
    return ' '.join(parts).lower()


def main():
    bank = json.load(open(BANK, encoding='utf-8'))
    if os.path.exists(EXTRA):
        bank += json.load(open(EXTRA, encoding='utf-8'))

    topics = []
    for key, name, chaps, mode, kws in TOPICS:
        hits_obj = []
        hits_code = []
        for q in bank:
            if q['chapter'] not in chaps:
                continue
            if mode == 'kw':
                t = text_of(q)
                if not any(k.lower() in t for k in kws):
                    continue
            if q['type'] in OBJ_TYPES:
                hits_obj.append(q)
            elif q['type'] == 'code':
                hits_code.append(q)
        n_obj, n_code = len(hits_obj), len(hits_code)
        in_exam_code = bool(EXAM_CODE_CHAPS & set(chaps))
        if n_obj >= 12 or (n_obj >= 5 and n_code >= 5):
            level = 'ok'
        elif n_obj >= 5 or n_code >= 1:
            level = 'thin'
        else:
            level = 'gap'
        topics.append({
            'key': key,
            'name': name,
            'chapters': chaps,
            'nObj': n_obj,
            'nCode': n_code,
            'level': level,
            'codeInExam': in_exam_code,
        })

    stats = defaultdict(int)
    for q in bank:
        stats[q['type']] += 1

    data = {
        'updated': '2026-11-16',
        'paper': [
            {'name': '选择题', 'n': 40, 'per': 1, 'total': 40,
             'note': '判断题并入，统一出选择题'},
            {'name': '填空题', 'n': 10, 'per': 2, 'total': 20,
             'note': '简答题并入，统一出填空题'},
            {'name': '编程题', 'n': 8, 'per': 5, 'total': 40,
             'note': '必考：文件读写 1 道、递归 1 道、数制转换'},
            {'name': '附加题', 'n': 1, 'per': 10, 'total': 10,
             'note': '难度高，拉开分差'},
        ],
        'range': {
            'chapters': '第 1–12 章（含课件 PPT、课后练习题）',
            'objective': '选择 40 + 填空 10 = 60 分，覆盖全 12 章',
            'code': '编程 8×5 = 40 分，第 1–8 章 + 第 10 章（文件）',
            'codeOut': '第 9、11、12 章编程不考',
            'note': '判断/简答不再单独出题：判断题按选择题考、简答题按填空题考，'
                    '所以题库里的判断题、简答题同样是考试范围。',
        },
        'topics': topics,
        'templates': TEMPLATES,
        'stats': dict(stats),
        'total': len(bank),
    }

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('/* 自动生成，请勿手改。重建：python tools/build_syllabus.py */\n')
        f.write('window.SYLLABUS = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n')

    print('考点覆盖（客观题 / 编程题）：')
    for t in topics:
        print('  %-14s %-8s 客观 %3d  编程 %2d' % (
            t['name'], {'ok': '充足', 'thin': '偏薄', 'gap': '缺口'}[t['level']],
            t['nObj'], t['nCode']))
    print('题库统计:', dict(stats), '合计', len(bank))
    print('->', OUT)


if __name__ == '__main__':
    main()
