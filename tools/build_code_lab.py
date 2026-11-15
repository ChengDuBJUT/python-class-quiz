# -*- coding: utf-8 -*-
"""把 pythonProject-2025 第 1-12 章代码整理成「代码复习」数据，并生成代码自测题。

输出: ../data/questions.js  (window.QUESTION_BANK / window.CODE_LAB)
"""
import os
import re
import json
import glob
import subprocess
import tempfile
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.join(os.path.dirname(BASE), 'pythonProject-2025')
BANK_JSON = os.path.join(BASE, 'data', 'questions.json')
OUT_JS = os.path.join(BASE, 'data', 'questions.js')

CHAPTER_TITLES = {
    1: '绪论', 2: 'Python基础', 3: '数据类型', 4: '运算符',
    5: '流程控制', 6: '组合数据类型', 7: '函数', 8: '类与对象',
    9: '异常、调试与测试', 10: '文件与数据格式化', 11: '标准库应用编程',
    12: '第三方库应用编程',
}

# 每章复习要点（结合课件章名与该目录下实际代码整理）
POINTS = {
    1: ['导入模块的三种写法：import / from…import / import…as',
        '内置模块 math、numpy 的调用方式（math.pi、math.sqrt、np.array）',
        '用 class 定义类、类属性与实例方法，self 的作用',
        'turtle 绘图的基本思路：fd / seth / circle',
        '模块顶层代码与 if __name__ == "__main__" 的区别'],
    2: ['单行注释 # 与三引号文档字符串（"""…"""）',
        '缩进表示代码块，续行与隐式换行',
        'keyword.kwlist 查看保留字；标识符命名规则、大小写敏感',
        '对象 = 属性 + 方法；命名空间（内置 / 全局 / 局部）',
        '自定义模块并在另一个文件中 import 调用'],
    3: ['数值类型：int / float / bool / complex，type() 与类型转换',
        '字符串三种引号、转义字符 \\n \\r 与原始字符串 r""',
        'f-string 与 format() 格式化输出',
        '列表的索引、切片、嵌套列表取值',
        '元组、集合、字典的创建与常用操作（dict()、zip、update）'],
    4: ['算术运算符优先级：2**2 先于 //，40//2**2 = 10',
        '比较 / 逻辑 / 身份运算符：is 与 == 的区别',
        '海象运算符 := 在表达式中赋值',
        '三目表达式：A if 条件 else B',
        '位运算符 & | ^ ~ << >> 与赋值运算符'],
    5: ['if / elif / else 多分支与嵌套',
        'for-in 遍历序列、range()、while 循环',
        'break / continue / pass 的差别',
        'match-case 结构匹配（Python 3.10+）与通配 case _',
        '嵌套循环打印九九乘法表、循环中的累加'],
    6: ['列表：remove / pop / sort / sorted / 切片反转 [::-1]',
        '列表推导式与带 if 的筛选、多重 for、zip',
        '字符串方法：ljust / rjust / center / find / replace / strip',
        '元组不可变但内部可变对象仍可修改',
        '集合去重、字典键值操作与 update()'],
    7: ['def 定义函数、return 返回值、文档字符串',
        '位置参数 / 关键字参数 / 默认参数 / *args / **kwargs',
        '参数解包：*dict 取键、**dict 取键值对',
        '作用域：global 与 nonlocal、局部变量',
        '模块间函数调用、if __name__ == "__main__" 测试代码'],
    8: ['class 定义类、__init__ 构造方法、__del__ 析构方法',
        '类属性 vs 实例属性，self 的使用',
        '私有成员 __name 与名称改写',
        '@classmethod / @staticmethod / 实例方法的区别',
        '继承、方法重写与多态；对象方法可通过类调用（需传实例）'],
    9: ['常见异常：NameError / IndexError / ZeroDivisionError / FileNotFoundError',
        'try-except-else-finally 的执行顺序',
        'raise 主动抛异常、assert 断言',
        '自定义异常类继承 Exception',
        '异常捕获后程序继续执行，与调试、单元测试的关系'],
    10: ['open() 的模式：r / w / a / w+ / wb+ 与 encoding',
        'read / readline / readlines / write / close 与 with 上下文',
        'seek() / tell() 文件指针操作',
        '一维 / 二维数据的 CSV 读写、split() 与 join()',
        'ord / chr / bin 与字符编码'],
    11: ['os 模块：getcwd / listdir / mkdir / path.splitext',
        'sys 模块：exit / argv / path',
        'time 模块：time / localtime / strftime / sleep',
        'random 模块：randint / seed / choice',
        'multiprocessing 与 threading 的基本用法、socket 与 sqlite'],
    12: ['NumPy：np.array、ndim / shape、axis=0/1 的 max / min / mean',
        'Pandas：Series / DataFrame、head / isnull / sum / mean',
        'Matplotlib：figure / plot / bar / scatter / show',
        'python-docx / python-pptx / pyexcel 读写 Office 文件',
        'requests / wordcloud / Flask / web3 等第三方库的安装与用途'],
}

# 代码自测题。ans = 正确选项下标；expected = 真实 stdout（用于自动核验）
QUIZ = [
    dict(ch=1, file='test1.py', code='import math\nprint(math.sqrt(9))\n',
         stem='chapter1 中 math.sqrt(9) 的输出是？',
         options=['3.0', '3', '9', 'TypeError'], ans=0, expected='3.0',
         expl='math.sqrt() 永远返回浮点数 3.0，即使刚好是整数。'),
    dict(ch=1, file='test2.py',
         code='class 海龟:\n    颜色 = "黑色"\n    def 显色(self):\n        print(self.颜色)\n\n小海 = 海龟()\n小海.显色()\n',
         stem='创建「海龟」对象并调用显色()，输出是？',
         options=['黑色', '白色', 'None', 'AttributeError'], ans=0, expected='黑色',
         expl='类属性 颜色="黑色"，实例通过 self.颜色 读到它；中文标识符在 Python 3 中合法。'),

    dict(ch=2, file='test.py', code='print(hex(10))\na = 56\nprint(type(a).__name__)\n',
         stem='chapter2 中 hex(10) 与 type(56) 的输出依次是？',
         options=['0xa / int', '10 / int', '0xA / float', '0xa / str'], ans=0,
         expected='0xa\nint',
         expl='hex() 返回小写前缀的字符串 "0xa"；整数字面量的类型是 int。'),
    dict(ch=2, file='test1.py', code='print(["a", "b",\n       "c",\n       "d"])\n',
         stem='括号内的隐式换行列表，打印结果是？',
         options=["['a', 'b', 'c', 'd']", "['a', 'b']", 'SyntaxError', "['a', 'b', 'c', 'd', 'e']"],
         ans=0, expected="['a', 'b', 'c', 'd']",
         expl='方括号内的换行属于同一表达式，列表含 4 个元素。'),

    dict(ch=3, file='test1.py', code='s = r"转义中：\\n 表示换行"\nprint(s)\n',
         stem='原始字符串 r"" 中的 \\n 会被打印成？',
         options=['字面量 \\n（反斜杠+n）', '一个换行', '两个换行', 'SyntaxError'],
         ans=0, expected='转义中：\\n 表示换行',
         expl='r 前缀关闭转义，\\n 保持为两个字符；若是普通字符串则会换行。'),
    dict(ch=3, file='test0.py',
         code='aList = ["python", 1, [2, 3, 4], 3.0, "计算机"]\nprint(aList[2][0])\n',
         stem='嵌套列表 aList[2][0] 的值是？',
         options=['2', 'python', '[2, 3, 4]', '3.0'], ans=0, expected='2',
         expl='aList[2] 是列表 [2,3,4]，再取索引 0 得到整数 2。'),

    dict(ch=4, file='test0.py', code='print(40 // 2 ** 2)\n',
         stem='表达式 40 // 2 ** 2 的值是？',
         options=['10', '20', '40', '2'], ans=0, expected='10',
         expl='** 优先级高于 //：2**2=4，40//4=10。'),
    dict(ch=4, file='test2.py', code='x = 5\ns = x + (y := 10)\nprint(s, y)\n',
         stem='含海象运算符的这段代码输出？',
         options=['15 10', '5 10', '15 5', 'SyntaxError'], ans=0, expected='15 10',
         expl='(y := 10) 在表达式内把 10 赋给 y 并返回 10，故 s=5+10=15。'),

    dict(ch=5, file='test1.py',
         code='total = 0\nfor i in range(1, 5):\n    if i % 2 == 0:\n        continue\n    total += i\nprint(total)\n',
         stem='跳过偶数后累加，输出是？',
         options=['4', '10', '6', '3'], ans=0, expected='4',
         expl='range(1,5)=1,2,3,4；偶数被 continue 跳过，只累加 1+3=4。'),
    dict(ch=5, file='test1.py',
         code='day = "3"\nmatch day:\n    case "1":\n        print("一")\n    case "2":\n        print("二")\n    case "3":\n        print("三")\n    case _:\n        print("其他")\n',
         stem='match-case 匹配字符串 "3" 时输出？',
         options=['三', '一', '其他', 'SyntaxError'], ans=0, expected='三',
         expl='match 按顺序匹配字面量分支，命中 case "3"；case _ 是兜底。'),

    dict(ch=6, file='test11.py',
         code='ls1 = [1, 3, 5, 7, 9]\nls1.remove(3)\nls1.pop(2)\nprint(ls1)\n',
         stem='先 remove(3) 再 pop(2)，列表变为？',
         options=['[1, 5, 9]', '[1, 5, 7, 9]', '[1, 3, 7, 9]', '[5, 7, 9]'],
         ans=0, expected='[1, 5, 9]',
         expl='remove(3) 按值删除 → [1,5,7,9]；pop(2) 按索引删除 7 → [1,5,9]。'),
    dict(ch=6, file='test10.py', code="sr = 'code'\nprint(sr.center(8, '%'))\n",
         stem='center(8, "%") 的输出是？',
         options=['%%code%%', 'code%%%%', '%code%', '  code  '], ans=0, expected='%%code%%',
         expl='字符串长 4，居中到 8 需左右各补 2 个 "%"。'),

    dict(ch=7, file='test10.py',
         code='def test1(a, b, c=33, *args, **kwargs):\n    print(a, b, c, args, kwargs)\n\ntest1(1, 2, 3, 4, e=6)\n',
         stem='混合参数传递的打印结果是？',
         options=["1 2 3 (4,) {'e': 6}", "1 2 3 (4, 6) {}", "1 2 33 (3, 4) {'e': 6}", 'TypeError'],
         ans=0, expected="1 2 3 (4,) {'e': 6}",
         expl='a=1, b=2, c=3（位置参数覆盖默认值），多余的 4 进 *args，e=6 进 **kwargs。'),
    dict(ch=7, file='test11.py',
         code='number = 10\ndef test():\n    print(number)\n\ntest()\n',
         stem='函数内读取全局 number，输出？',
         options=['10', 'NameError', 'None', '0'], ans=0, expected='10',
         expl='只读取不赋值时，函数会沿 LEGB 链找到全局变量 number=10。'),

    dict(ch=8, file='test1.py',
         code='class Car:\n    color = "red"\n    def drive(self):\n        print("行驶")\n\ncar = Car()\nprint(car.color)\ncar.drive()\n',
         stem='访问类属性并调用实例方法，输出？',
         options=['red / 行驶', '行驶 / red', 'None / 行驶', 'AttributeError'],
         ans=0, expected='red\n行驶',
         expl='实例可读取类属性 color；drive(self) 由实例调用时 self 自动传入。'),
    dict(ch=8, file='test10.py',
         code='class Car:\n    def __init__(self, color):\n        self.color = color\n\ncar = Car("blue")\nprint(car.color)\n',
         stem='构造方法中赋值实例属性，输出？',
         options=['blue', 'red', 'None', 'TypeError'], ans=0, expected='blue',
         expl='__init__ 接收 "blue" 并绑定到 self.color，创建对象时自动执行。'),

    dict(ch=9, file='test10.py',
         code="try:\n    raise ValueError('x')\nexcept Exception as e:\n    print(type(e).__name__)\nfinally:\n    print('done')\n",
         stem='主动抛出 ValueError 并捕获，输出？',
         options=['ValueError / done', 'x / done', 'Exception / done', 'done / ValueError'],
         ans=0, expected='ValueError\ndone',
         expl='except 先打印异常类型名，finally 无论是否异常都会执行。'),
    dict(ch=9, file='test11.py',
         code="try:\n    print(1 / 0)\nexcept ZeroDivisionError:\n    print('zero')\n",
         stem='除零被捕获后的输出？',
         options=['zero', 'ZeroDivisionError', '0', '程序崩溃无输出'], ans=0, expected='zero',
         expl='1/0 触发 ZeroDivisionError，被配套 except 捕获后打印 zero。'),

    dict(ch=10, file='test10.py', code="ls = ['小米', '华为', '苹果']\nprint('&'.join(ls))\n",
         stem='使用 join 拼接列表，输出？',
         options=['小米&华为&苹果', "['小米', '华为', '苹果']", '小米,华为,苹果', 'TypeError'],
         ans=0, expected='小米&华为&苹果',
         expl='str.join() 用分隔符把序列中的字符串连成一个字符串。'),
    dict(ch=10, file='test11.py', code="line = '1,2,3,4'\nprint(line.split(','))\n",
         stem='split(",") 的结果是？',
         options=["['1', '2', '3', '4']", '[1, 2, 3, 4]', "'1','2','3','4'", '1 2 3 4'],
         ans=0, expected="['1', '2', '3', '4']",
         expl='split 返回字符串列表，元素仍是 str，不会自动转整数。'),

    dict(ch=11, file='test1.py', code="import os\nprint(os.path.splitext('demo.csv')[1])\n",
         stem='os.path.splitext("demo.csv")[1] 返回？',
         options=['.csv', 'demo', 'demo.csv', 'csv'], ans=0, expected='.csv',
         expl='splitext 拆成 (根, 扩展名)，扩展名包含点号。'),
    dict(ch=11, file='test11.py', code='import threading\nprint(threading.current_thread().name)\n',
         stem='主线程中 current_thread().name 通常是？',
         options=['MainThread', 'Thread-1', 'main', 'None'], ans=0, expected='MainThread',
         expl='主线程默认名为 MainThread；子线程默认为 Thread-N。'),

    # 需要 numpy / pandas，本机 python3 未安装，按库语义给定答案
    dict(ch=12, file='test1.py', run=False,
         code='import numpy as np\ndata = np.array([[1, 2, 3], [4, 5, 6]])\nprint(np.max(data, axis=0))\n',
         stem='对 2×3 数组按 axis=0 求最大值，输出？',
         options=['[4 5 6]', '[3 6]', '6', '[1 2 3]'], ans=0, expected='[4 5 6]',
         expl='axis=0 沿行方向压缩，得到每一列的最大值 [4,5,6]；axis=1 才是 [3,6]。'),
    dict(ch=12, file='test2.py', run=False,
         code='import pandas as pd\ns = pd.Series([1, 2, 3])\nprint(s.head(2).tolist())\n',
         stem='Series 取前两行再转 list，输出？',
         options=['[1, 2]', '[1, 2, 3]', '0    1\n1    2', '[2, 3]'], ans=0, expected='[1, 2]',
         expl='head(2) 取前两个元素，tolist() 转成 Python 列表 [1, 2]。'),
]


def collect_files():
    chapters = []
    for n in range(1, 13):
        d = os.path.join(PROJ, 'chapter%d' % n)
        paths = glob.glob(os.path.join(d, '*.py'))

        def key(p):
            m = re.search(r'(\d+)', os.path.basename(p))
            return (int(m.group(1)) if m else 0, os.path.basename(p))

        files = []
        for p in sorted(paths, key=key):
            try:
                code = open(p, encoding='utf-8', errors='replace').read().rstrip()
            except Exception as e:
                code = '# 读取失败: %s' % e
            files.append({'name': os.path.basename(p), 'code': code})
        chapters.append({'n': n, 'title': CHAPTER_TITLES[n],
                         'points': POINTS[n], 'files': files})
    return chapters


def run_snippet(code):
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code)
        path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True,
                           encoding='utf-8', env=env, timeout=8)
        if r.returncode != 0:
            return None, (r.stderr or '').strip()[-300:]
        return r.stdout.rstrip('\n'), ''
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def norm(s):
    return re.sub(r'\s+', '', str(s)).replace('／', '/')


def matched(option, stdout):
    o = norm(option)
    s = norm(stdout)
    if o == s:
        return True
    if '/' in option:
        if norm(''.join(x.strip() for x in option.split('/'))) == s:
            return True
    return False


def build_quiz():
    items = []
    counters = {}
    warnings = []
    for item in QUIZ:
        ch = item['ch']
        counters[ch] = counters.get(ch, 0) + 1
        seq = counters[ch]
        verified = False
        if item.get('run', True):
            real, err = run_snippet(item['code'])
            if real is None:
                warnings.append('运行失败 ch%d-%02d: %s' % (ch, seq, err))
            elif real != item['expected']:
                warnings.append('输出与预期不符 ch%d-%02d: 实际=%r 预期=%r'
                                % (ch, seq, real, item['expected']))
            if real is not None and matched(item['options'][item['ans']], real):
                verified = True
        # 确定性轮转选项，避免正确答案全落在 A 上
        shift = (ch * 7 + seq * 3) % len(item['options'])
        rotated = item['options'][shift:] + item['options'][:shift]
        new_ans = (item['ans'] - shift) % len(item['options'])
        items.append({
            'id': 'lab%d-read-%02d' % (ch, seq),
            'chapter': ch,
            'chapterTitle': CHAPTER_TITLES[ch],
            'type': 'coderead',
            'exam': False,  # pythonProject 代码属复习材料，不计入考试范围
            'sourceKind': '代码复习',
            'sourceFile': 'pythonProject-2025/chapter%d/%s' % (ch, item['file']),
            'sourceLocator': '第%d章 代码自测 %d' % (ch, seq),
            'stem': item['stem'],
            'code': item['code'].rstrip(),
            'options': ['%s. %s' % (chr(65 + i), o) for i, o in enumerate(rotated)],
            'answer': chr(65 + new_ans),
            'explanation': item['expl'],
            'verified': verified,
        })
    return items, warnings


def js(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2)


def main():
    bank = json.load(open(BANK_JSON, encoding='utf-8'))
    for q in bank:
        if q['type'] == 'judge':
            q['answer'] = (q['answer'] == '对')
    lab = collect_files()
    quiz, warnings = build_quiz()
    allq = bank + quiz
    with open(OUT_JS, 'w', encoding='utf-8') as f:
        f.write('/* 自动生成，请勿手改。重建：python3 tools/build_bank.py && python3 tools/build_code_lab.py */\n')
        f.write('window.QUESTION_BANK = ' + js(allq) + ';\n\n')
        f.write('window.CODE_LAB = ' + js(lab) + ';\n')
    print('教材题=%d 代码自测=%d 合计=%d 代码文件=%d' % (
        len(bank), len(quiz), len(allq), sum(len(c['files']) for c in lab)))
    print('自动核验通过:', sum(1 for q in quiz if q['verified']), '/', len(quiz))
    for w in warnings:
        print('  WARN', w)
    print('->', OUT_JS)


if __name__ == '__main__':
    main()
