# -*- coding: utf-8 -*-
"""按 2026-11 老师公布的新考纲补充题目。

考纲要点决定了补题方向：
  选择 40×1（判断并入选择）、填空 10×2（简答并入填空）、编程 8×5、附加 10
  20 个考点里，题库覆盖最薄的是：递归、数制转换、类方法/静态方法、变量作用域、
  命名空间、编码方式、缩进、对象状态；编程题还明确"必考一道文件、一道递归、数制转换"。

本脚本把补的题目写成 tools/source/exam_extra.json。
编程题的参考程序会**真实执行**（带 stdin 与预置文件），把 stdout 写进 output 字段，
所以页面上显示的"运行结果"是真的跑出来的，不是手写的。

用法：python tools/build_exam_extra.py
"""
import json
import os
import subprocess
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'tools', 'source', 'exam_extra.json')
PY = r'E:/anaconda/envs/leaf_gcn/python.exe'

TITLES = {
    1: '绪论', 2: 'Python基础', 3: '数据类型', 4: '运算符', 5: '流程控制',
    6: '组合数据类型', 7: '函数', 8: '类与对象', 9: '异常、调试与测试',
    10: '文件与数据格式化', 11: '标准库应用编程', 12: '第三方库应用编程',
}

# ---------------------------------------------------------------- 客观题
# (id, 章节, 题型, 考点, 题干, 选项, 答案, 解析)
MCQ = [
    # ---------------- 数制转换 ----------------
    ('base-01', 3, 'single', ['base'],
     '表达式 bin(10) 的结果是(　　)。',
     ['0b1010', '1010', '0b1001', 'b1010'], 'A',
     'bin() 返回带前缀 0b 的字符串：10 = 8+2 = 1010(2)，所以是 "0b1010"。'
     'oct() 前缀 0o、hex() 前缀 0x，三者返回的都是字符串，不能直接参与算术运算。'),

    ('base-02', 3, 'single', ['base'],
     '表达式 int("1011", 2) 的结果是(　　)。',
     ['11', '1011', '3', '报错'], 'A',
     'int(字符串, 进制) 的第二个参数是"按几进制来解释这个字符串"，1011(2) = 8+2+1 = 11。'
     '第二个参数默认是 10，所以 int("1011") 得到的是 1011（十进制一千零一十一），别混淆。'),

    ('base-03', 3, 'blank', ['base'],
     '表达式 hex(255) 的结果是____________。',
     None, ['0xff', '0xFF', '0XFF'], '255 = 15×16 + 15，十六进制是 ff，hex() 带前缀 0x，'
     '所以结果是字符串 "0xff"（字母小写）。'),

    ('base-04', 3, 'blank', ['base'],
     '二进制数 0b1101 对应的十进制数是____________。',
     None, ['13'], '按权展开：1×2³ + 1×2² + 0×2¹ + 1×2⁰ = 8+4+0+1 = 13。'),

    ('base-05', 3, 'single', ['base'],
     '把十进制整数 26 转成二进制，结果是(　　)。',
     ['11010', '10110', '11001', '10011'], 'A',
     '除基取余、逆序排列：26÷2=13余0，13÷2=6余1，6÷2=3余0，3÷2=1余1，1÷2=0余1，'
     '余数从下往上读得 11010。这也是编程题里"不用内置函数做进制转换"的标准算法。'),

    ('base-06', 3, 'blank', ['base'],
     '十六进制数 0x2F 对应的十进制数是____________。',
     None, ['47'], '2×16 + 15 = 47。十六进制里 A=10、B=11 … F=15，F 即 15。'),

    # ---------------- 递归 ----------------
    ('rec-01', 7, 'single', ['recursion'],
     '编写递归函数时，必须包含的要素是(　　)。',
     ['终止条件（递归出口）', '循环变量', 'global 声明', 'try 语句'], 'A',
     '递归 = "自己调用自己 + 出口"。没有出口就会一直调用下去，最终触发'
     ' RecursionError: maximum recursion depth exceeded。出口通常是 if 判断最简单的情形，'
     '例如阶乘里 if n == 1: return 1。'),

    ('rec-02', 7, 'blank', ['recursion'],
     '已知 def f(n): return 1 if n <= 1 else n * f(n - 1)，则 f(5) 的值是____________。',
     None, ['120'], 'f(5)=5×f(4)=5×4×f(3)=5×4×3×f(2)=5×4×3×2×f(1)=120，'
     '共调用 f 五次，其中 f(1) 命中出口直接返回 1。'),

    ('rec-03', 7, 'single', ['recursion'],
     '已知 def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)，则 fib(6) 的值是(　　)。',
     ['8', '5', '13', '6'], 'A',
     '数列为 fib(0)=0、fib(1)=1、1、2、3、5、8…，fib(6)=8。'
     '注意出口写成 n < 2 时，0 和 1 两个基本情况都覆盖到了，这是最容易漏掉的一个。'),

    ('rec-04', 7, 'single', ['recursion'],
     '关于递归与循环，下列说法正确的是(　　)。',
     ['理论上所有递归都能改写成循环，但递归层数过深会引发 RecursionError',
      '递归的执行效率一定高于循环',
      '递归函数不需要 return 语句',
      '递归只能用于数学计算，不能处理字符串和列表'], 'A',
     '递归的代价是每层调用都要占用栈空间，Python 默认递归深度约 1000 层，'
     '超过就 RecursionError；而循环不占栈。所以"能递归也能循环"时，'
     '数据规模大就用循环或加记忆化。'),

    ('rec-05', 7, 'single', ['recursion'],
     '在函数内部定义函数、并把内层函数作为返回值返回（如 def outer(): def inner(): ... return inner），'
     '这种用法称为(　　)。',
     ['闭包', '重载', '继承', '装饰器'], 'A',
     '外层函数返回内层函数时，内层函数会"记住"外层的局部变量，即使外层已经返回——这就是闭包。'
     '要在内层改写外层的变量，得先用 nonlocal 声明。'),

    ('rec-06', 7, 'blank', ['recursion'],
     '写递归函数时，每次递归调用都必须让参数____________（填"增大"或"减小"）以逐步接近出口。',
     None, ['减小', '变小', '趋于出口'],
     '从 n 到 n-1 是"减小"，从 left/right 区间到更小的区间也是"缩小"。'
     '如果参数没朝出口靠近，即使写了出口也会无限递归。'),

    # ---------------- 文件 ----------------
    ('file-01', 10, 'single', ['file'],
     '使用 with open("a.txt", "r") as f: 读写文件的优点是(　　)。',
     ['代码块结束时会自动关闭文件，即使中途抛出异常',
      '可以省略文件名',
      '读写速度比普通 open 更快',
      '不需要指定打开模式'], 'A',
     'with 是上下文管理器：进入时调 __enter__ 拿到文件对象，退出时无论正常结束还是抛异常'
     '都会调 __exit__，由它负责 f.close()。忘了 close 会占着文件句柄，Windows 上还可能导致'
     '文件被锁、无法删除。'),

    ('file-02', 10, 'blank', ['file'],
     'open("a.txt", "a") 中的模式 "a" 表示____________。',
     None, ['追加', '追加写入', '在文件末尾追加'], '"w" 清空重写、"a" 追加到末尾、'
     '"r" 只读（文件必须存在）。"a" 模式下文件不存在会新建，指针自动落在末尾，'
     '所以同一段代码跑多次，内容会越写越长。'),

    ('file-03', 10, 'single', ['file'],
     'f.readlines() 的返回值是(　　)。',
     ['一个列表，每个元素是文件中的一行（含行尾换行符）',
      '一个字符串，包含文件全部内容',
      '一个整数，表示文件行数',
      '一个迭代器，只能遍历一次'], 'A',
     'readlines() 返回 list；read() 返回整份字符串；直接 for line in f 才是逐行迭代。'
     '注意每个元素末尾带着 "\\n"，要干净内容得 strip() 掉。'),

    ('file-04', 10, 'blank', ['file'],
     '同一个文件对象上，f.read() 已经把内容读完后，再次调用 f.read() 返回____________。',
     None, ['空字符串', '空串', '""', "''"],
     '文件指针已经到末尾，再读没有内容可读，返回空字符串 ""，而不是报错、也不是 None。'
     '想重新读要先 f.seek(0) 把指针移回开头。'),

    ('file-05', 10, 'single', ['file'],
     '用 "r" 模式打开一个不存在的文件，会(　　)。',
     ['抛出 FileNotFoundError', '自动新建这个空文件', '返回 None', '返回空字符串'], 'A',
     '"r" 要求文件必须已存在，否则 FileNotFoundError。想"没有就新建"要用 "w"、"a" 或 "x"'
     '（"x" 是文件已存在则报错）。'),

    ('file-06', 10, 'single', ['file'],
     '下面哪一句在 f 已经 close() 之后再执行会抛异常(　　)。',
     ['f.write("abc")', 'f.closed', 'print(f.name)', 'f.mode'], 'A',
     '关闭后只能读 f.name / f.mode / f.closed 这类属性，任何读写操作都会抛'
     ' ValueError: I/O operation on closed file。'),

    # ---------------- 类方法 / 静态方法 / 对象方法 ----------------
    ('cls-01', 8, 'single', ['clsmethod'],
     '用 @classmethod 修饰的类方法，其第一个参数通常是(　　)。',
     ['cls，表示类本身', 'self，表示调用它的对象', '没有参数', 'cls，表示父类'], 'A',
     '类方法的第一个参数约定写作 cls，由 Python 自动传入"当前类"，'
     '所以它既能读类属性，也能通过 cls(...) 创建对象；写成 self 会让语义混乱但语法不报错，'
     '考试按约定答 cls。'),

    ('cls-02', 8, 'single', ['objmethod'],
     '用 @staticmethod 修饰的静态方法，其参数特点是(　　)。',
     ['既没有 self 也没有 cls，就是一个普通函数', '第一个必须是 self', '第一个必须是 cls',
      '必须有且只有一个参数'], 'A',
     '静态方法只是"挂在类里的普通函数"，不接收 self/cls，既不能访问实例属性也不能访问类属性；'
     '好处是命名上归到类里、便于组织，调用时类和对象都能调。'),

    ('cls-03', 8, 'blank', ['clsmethod'],
     '在类中定义类方法，需要使用的装饰器是____________。',
     None, ['@classmethod', 'classmethod', '@ classmethod'],
     '三种方法靠装饰器区分：无装饰器 = 对象方法（第一个参数 self）；'
     '@classmethod = 类方法（第一个参数 cls）；@staticmethod = 静态方法（无 self/cls）。'),

    ('cls-04', 8, 'single', ['clsmethod'],
     '下面哪种方法可以直接用"类名.方法名()"调用而无需创建对象(　　)。',
     ['类方法和静态方法都能', '只有对象方法能', '三种都不能', '只有对象方法和类方法能'], 'A',
     '类方法拿得到 cls、静态方法不需要任何隐含参数，两者都能通过类名直接调用；'
     '对象方法必须传实例，写成 类名.方法名(对象) 也能调，但那等于手动把对象塞给 self。'),

    ('cls-05', 8, 'blank', ['objmethod'],
     '类的对象方法（实例方法）第一个参数通常命名为____________，它代表调用该方法的对象本身。',
     None, ['self'], 'self 不是关键字，只是约定名；换成 this 语法上也能跑，但可读性差、'
     '别人看不懂，考试一律写 self。'),

    # ---------------- 变量作用域 ----------------
    ('scope-01', 7, 'single', ['scope'],
     '在函数内部要给全局变量重新赋值，需要使用(　　)关键字声明。',
     ['global', 'nonlocal', 'static', 'public'], 'A',
     '函数里对变量赋值默认创建同名局部变量，不会改动全局的。加 global 声明后，'
     '函数内的赋值才作用在全局变量上。只读全局变量则不需要 global。'),

    ('scope-02', 7, 'single', ['scope'],
     '在嵌套函数的内层函数中，要修改外层函数的局部变量，应使用(　　)。',
     ['nonlocal', 'global', 'self', 'final'], 'A',
     'nonlocal 指向"最近一层外层函数的局部作用域"；global 指向模块级全局作用域。'
     '只有内层想改外层局部变量时才需要 nonlocal，只读同样不需要。'),

    ('scope-03', 7, 'blank', ['scope'],
     '在函数内部定义的变量称为____________变量，函数调用结束后它就不再可用。',
     None, ['局部', '局部变量'], '局部变量的生命周期只在函数执行期间，'
     '函数返回后它的命名空间被销毁，所以函数外访问会 NameError。'),

    ('scope-04', 7, 'single', ['scope'],
     '下面程序的输出是(　　)。\nx = 10\ndef f():\n    x = 20\nf()\nprint(x)',
     ['10', '20', 'None', '报错'], 'A',
     '函数内的 x = 20 创建了一个新的局部变量，与全局 x 无关，函数结束就销毁了，'
     '所以外面打印的仍是 10。想改全局必须写 global x。'),

    ('scope-05', 7, 'single', ['namespace'],
     'Python 查找一个变量名时的顺序是(　　)。',
     ['局部 → 嵌套（外层函数） → 全局 → 内置',
      '全局 → 局部 → 内置 → 嵌套',
      '内置 → 全局 → 局部 → 嵌套',
      '局部 → 全局 → 嵌套 → 内置'], 'A',
     '这就是常说的 LEGB：Local（函数内）→ Enclosing（外层函数）→ Global（模块级）→ Built-in'
     '（内置命名空间）。找不到才抛 NameError。'),

    # ---------------- 命名空间 ----------------
    ('ns-01', 8, 'single', ['namespace'],
     'Python 解释器的命名空间不包括(　　)。',
     ['线程命名空间', '内置命名空间', '全局命名空间', '局部命名空间'], 'A',
     '教材把解释器的命名空间分为内置、全局、局部三种（教材第2章填空题也考这三个）。'
     '内置命名空间存放 print、len 等内置函数，全局对应模块，局部对应函数/方法调用。'),

    ('ns-02', 8, 'blank', ['namespace'],
     'Python 解释器的命名空间分为____________、____________和____________。',
     None, ['内置,全局,局部', '内置命名空间,全局命名空间,局部命名空间'],
     '按"从外到内"是内置 → 全局 → 局部；按查找顺序（LEGB）则是局部先被找到。'
     '填空题三个空按任意顺序写都能判对（系统会忽略逗号等分隔符）。'),

    ('ns-03', 8, 'single', ['namespace'],
     '函数被调用时创建、调用结束时销毁的命名空间是(　　)。',
     ['局部命名空间', '全局命名空间', '内置命名空间', '模块命名空间'], 'A',
     '局部命名空间随函数调用而生、随返回而亡；全局命名空间随模块加载创建、'
     '直到程序结束；内置命名空间在解释器启动时就存在。'),

    ('ns-04', 2, 'blank', ['namespace'],
     '在当前命名空间中找不到某个变量名时，Python 会抛出____________异常。',
     None, ['NameError', 'NameError:', '命名错误'],
     '名字查找走完 LEGB 四级都没命中就抛 NameError: name \'xxx\' is not defined。'
     '注意区分：NameError 是"名字不存在"，TypeError 是"类型不对"，AttributeError 是"属性不存在"。'),

    # ---------------- 编码方式 ----------------
    ('enc-01', 2, 'single', ['encoding'],
     'UTF-8 编码中，一个常用的汉字通常占(　　)个字节。',
     ['3', '1', '2', '4'], 'A',
     'UTF-8 是变长编码：ASCII 字符 1 字节，常用汉字 3 字节；GBK 是双字节编码，'
     '一个汉字固定 2 字节。所以同一段中文用 UTF-8 存通常比 GBK 大 50%。'),

    ('enc-02', 2, 'blank', ['encoding'],
     'len("中".encode("utf-8")) 的结果是____________。',
     None, ['3'], 'encode() 把字符串编码成 bytes，len() 数的是字节数而不是字符数：'
     'UTF-8 下"中"占 3 字节。而 len("中") 是 1（字符数）。'),

    ('enc-03', 2, 'single', ['encoding'],
     'GBK 编码中，一个汉字占(　　)个字节。',
     ['2', '1', '3', '4'], 'A',
     'GBK 属于双字节编码，一个汉字固定 2 字节——这就是教材里"李杰"用 UTF-8 是 6 字节、'
     '用 GBK 是 4 字节的原因。'),

    ('enc-04', 2, 'blank', ['encoding'],
     'Python 3 的源文件默认使用____________编码保存和读取。',
     None, ['UTF-8', 'utf-8', 'utf8'], 'Python 3 默认 UTF-8；Python 2 默认 ASCII，'
     '所以老代码常在文件头写 # -*- coding: utf-8 -*-。读文件时如果系统默认编码不是 UTF-8'
     '（中文 Windows 常是 GBK），要显式写 encoding="utf-8"。'),

    ('enc-05', 2, 'single', ['encoding'],
     '关于 encode() 与 decode()，说法正确的是(　　)。',
     ['encode() 把 str 变成 bytes，decode() 把 bytes 变回 str',
      'encode() 把 bytes 变成 str，decode() 把 str 变成 bytes',
      '两者作用完全相同',
      '只有 encode() 需要指定编码'], 'A',
     '记住方向：字符串"编"成字节用 encode，字节"解"回字符串用 decode。'
     '拿 bytes 去调用字符串方法、或拿 str 直接写二进制文件，都会报错。'),

    ('enc-06', 2, 'single', ['encoding'],
     'type("abc".encode("utf-8")) 的结果是(　　)。',
     ["<class 'bytes'>", "<class 'str'>", "<class 'bytearray'>", "<class 'int'>"], 'A',
     'encode() 的返回值是 bytes 类型，打印出来带 b 前缀，例如 b\'abc\'。'
     '所以 len("abc".encode("utf-8")) 数的是字节数 3，而 len("abc") 是字符数 3——'
     '纯英文时两者相同，中文才拉开差距。'),

    # ---------------- 缩进 ----------------
    ('ind-01', 2, 'blank', ['indent'],
     'Python 中建议使用____________个空格表示一级缩进。',
     None, ['4', '四'], 'PEP 8 建议一级缩进 4 个空格。Python 用缩进表示代码块，'
     '同一代码块内缩进量必须一致。'),

    ('ind-02', 2, 'single', ['indent'],
     '同一代码块内缩进量不一致（有的 4 空格、有的 2 空格），运行时会(　　)。',
     ['抛出 IndentationError，代码无法运行', '自动对齐，正常执行', '只给警告，继续执行',
      '按第一个缩进量统一处理'], 'A',
     '缩进在 Python 里是语法而不是排版。混用 Tab 和空格、或同一块内不一致，'
     '直接 IndentationError: unexpected indent / unindent does not match any outer indentation level。'),

    ('ind-03', 2, 'single', ['indent'],
     '关于缩进，下列说法正确的是(　　)。',
     ['缩进相同的连续语句属于同一个代码块',
      '缩进只是为了让代码好看，多少都行',
      '同一程序里所有代码块必须缩进相同的空格数',
      'Tab 和空格可以随意混用'], 'A',
     '缩进决定"谁属于谁"：缩进量相同的语句构成同一个代码块，缩进多了表示进入子块。'
     '不同层级的代码块可以缩进不同量（比如外层 4 空格、内层再 4 空格），'
     '但**同一块内必须一致**，且 Tab 与空格不能混用。'),

    ('ind-04', 2, 'blank', ['indent'],
     'Python 中缩进相同的连续语句属于同一个____________。',
     None, ['代码块', '语句块', '块'],
     '这正是缩进的语义：它替代了 C/Java 的花括号，用来划分代码块。'
     '所以 if/for/while/def/class 后面那一行必须以冒号结尾，下一行必须缩进。'),

    # ---------------- 对象 / 状态 ----------------
    ('obj-01', 2, 'blank', ['state'],
     'Python 中对象的状态称为____________，对象的行为称为____________。',
     None, ['属性,方法', '属性、方法', '特征,方法'],
     '状态 = 属性（数据），行为 = 方法（函数）。教材第2章的填空原句就是'
     '"对象的状态称为属性，对象的行为称为方法"。'),

    ('obj-02', 8, 'single', ['state'],
     '类属性与实例属性的区别是(　　)。',
     ['类属性属于类、被所有实例共享；实例属性属于单个对象',
      '类属性只能通过类名访问，实例属性只能通过对象访问',
      '实例属性被所有对象共享',
      '两者完全等价，只是写法不同'], 'A',
     '类属性写在类体里，所有实例共享同一份；实例属性在 __init__ 里用 self.x 赋值，'
     '每个对象各存一份。在实例上给类属性赋值会在该实例上新建一个同名实例属性，'
     '不会影响类和其他对象——这是常考的陷阱。'),

    ('obj-03', 8, 'single', ['state'],
     '在类的外部通过对象访问实例属性，正确的写法是(　　)。',
     ['对象名.属性名', '属性名', '类名.属性名', '对象名[属性名]'], 'A',
     '点号访问是标准写法。对象成员属于对象，只能通过对象名访问；'
     '类成员（类属性、类方法）才可以用类名访问。'),

    # ---------------- Python 特性 ----------------
    ('feat-01', 1, 'single', ['feature'],
     '下列关于 Python 语言特点的说法，错误的是(　　)。',
     ['Python 是编译型语言，必须先编译成机器码再执行',
      'Python 是解释型语言，逐行翻译执行',
      'Python 是动态类型语言，变量类型在运行时确定',
      'Python 是面向对象语言，一切皆对象'], 'A',
     'Python 由解释器逐行翻译执行，属于解释型语言（严格说是"先编译成字节码再由虚拟机执行"），'
     '不需要像 C 那样提前编译成机器码。正因为是动态类型，同一个变量可以先后指向不同类型的对象。'),

    ('feat-02', 1, 'single', ['feature'],
     'Python 中用缩进来表示(　　)。',
     ['代码块（语句的从属关系）', '变量作用域的大小', '字符串的长度', '注释的范围'], 'A',
     'C/Java 用 { } 表示代码块，Python 用缩进表示。所以缩进错了程序逻辑就错了，'
     '这也是 Python 与其他语言最直观的区别。'),

    # ---------------- 异常 ----------------
    ('exc-01', 9, 'single', ['exception'],
     '关于 try 语句中的 finally 子句，下列说法正确的是(　　)。',
     ['无论是否发生异常、是否被 except 捕获，finally 都会执行',
      '只有发生异常时才执行',
      '只有不发生异常时才执行',
      '只有 except 里写了 raise 才执行'], 'A',
     'finally 的语义是"无论如何都要执行"，常用于关闭文件、释放资源。'
     '即使 try 里 return，也会先执行 finally 再返回。'),

    ('exc-02', 9, 'single', ['exception'],
     '一个 try 后面跟多个 except 时，正确的写法是(　　)。',
     ['把子类异常写在父类异常之前',
      '把父类异常写在子类异常之前',
      '顺序无所谓',
      '只能写一个 except'], 'A',
     'except 自上而下匹配，一旦匹配就跳出。如果把 Exception 写在前面，'
     '后面更具体的分支永远没机会执行（虽然不报错，但逻辑失效）。'),

    ('exc-03', 9, 'blank', ['exception'],
     '在程序中主动抛出异常使用的语句是____________。',
     None, ['raise'], 'raise ValueError("提示信息") 主动抛异常；raise 不带参数表示'
     '"把当前正在处理的异常原样再抛出去"，常用于 except 里记录日志后继续向上抛。'),

    ('exc-04', 9, 'single', ['exception'],
     'except 后面不写具体异常类型（写成 except:）时，表示(　　)。',
     ['捕获所有类型的异常', '语法错误，不能这么写', '只捕获 Exception 子类',
      '只捕获第一个异常'], 'A',
     '不写类型等价于捕获 BaseException，连 KeyboardInterrupt（Ctrl+C）都会被吞掉，'
     '所以正式代码推荐写 except Exception:，把系统退出类异常放过去。'),

    # ---------------- 函数 ----------------
    ('fn-01', 7, 'single', ['func'],
     '函数中执行 return 语句但不带任何返回值时，函数返回(　　)。',
     ['None', '0', '空字符串', '报错'], 'A',
     '没有 return 或者只写 return，函数都返回 None。所以"函数一定有返回值"这句话是对的，'
     '只是可能返回 None。'),

    ('fn-02', 7, 'blank', ['func'],
     '定义函数时，带默认值的参数必须放在参数列表的____________。',
     None, ['末尾', '最后', '后面', '最右边'],
     '语法规定：默认参数必须在所有非默认参数之后，否则 SyntaxError: '
     'non-default argument follows default argument。调用时同理，'
     '关键字参数要写在位置参数后面。'),
]

# ---------------------------------------------------------------- 编程题
# (id, 章节, 考点, 题干, 参考程序, stdin, 预置文件, 解析/易错点, 是否附加题)
CODE = [
    ('base-p1', 3, ['base'],
     '编程实现：从键盘输入一个十进制正整数，输出它的二进制、八进制和十六进制形式。',
     'n = int(input())          # 输入样例：26\n'
     'print("二进制：", bin(n))\n'
     'print("八进制：", oct(n))\n'
     'print("十六进制：", hex(n))\n',
     '26\n', None,
     '金句：bin/oct/hex 直接给带前缀的字符串。若要"纯数字"的 11010，'
     '用 bin(n)[2:] 把前缀切掉（或用 format(n, "b")）。', False),

    ('base-p2', 3, ['base'],
     '编程实现：不使用内置转换函数，用"除基取余"把十进制正整数 n 转换成二进制并输出。',
     'n = int(input())          # 输入样例：26\n'
     'base = 2                      # 改成 8 / 16 就是八进制、十六进制版本\n'
     'digits = "0123456789ABCDEF"   # 超过 9 的数位用 A~F\n'
     's = ""\n'
     'while n > 0:\n'
     '    s = digits[n % base] + s   # 余数放在最前面：逆序拼接\n'
     '    n = n // base              # 整除，继续取下一位\n'
     'print(s if s else "0")\n',
     '26\n', None,
     '除基取余的要点有两个：① 余数要"往前插"（逆序），不是往后追加；'
     '② 循环条件是 n > 0，最后别忘了处理 n=0 的情况。把 2 换成 8 或 16 就是通用版本。', False),

    ('base-p3', 3, ['base'],
     '编程实现：输入一个二进制字符串（如 "1101"），输出它对应的十进制数；再输入一个十六进制'
     '字符串，输出对应的十进制数。',
     'b = input()               # 输入样例：1101\n'
     'h = input()               # 输入样例：2F\n'
     'print(int(b, 2))\n'
     'print(int(h, 16))\n',
     '1101\n2F\n', None,
     'int(字符串, 进制) 是反向转换的关键：第二个参数告诉 Python 按几进制解释。'
     'int("2F", 16) = 47，不必自己写循环。', False),

    ('rec-p1', 7, ['recursion'],
     '编程实现：用递归函数求 n 的阶乘（n!），n 由键盘输入。',
     'def fact(n):\n'
     '    if n == 1:              # 递归出口：1! = 1\n'
     '        return 1\n'
     '    return n * fact(n - 1)  # 递归调用：n! = n × (n-1)!\n'
     '\n'
     'n = int(input())          # 输入样例：5\n'
     'print(n, "的阶乘是", fact(n))\n',
     '5\n', None,
     '递归三件套：出口、递推式、参数向出口收敛（这里 n-1 每次减小）。'
     '漏掉出口就是无限递归 → RecursionError。', False),

    ('rec-p2', 7, ['recursion'],
     '编程实现：用递归函数输出斐波那契数列的前 10 项（fib(0)=0，fib(1)=1）。',
     'def fib(n):\n'
     '    if n < 2:                        # 出口：0 和 1 两种情况\n'
     '        return n\n'
     '    return fib(n - 1) + fib(n - 2)   # 前两项之和\n'
     '\n'
     'print(" ".join(str(fib(i)) for i in range(10)))\n',
     '', None,
     'fib(0)=0 这个出口很容易被写成 n == 1，导致 fib(0) 一路递归到负数。'
     '另外这样写是指数级重复计算，n 大了很慢——附加题里可以加记忆化。', False),

    ('rec-p3', 7, ['recursion'],
     '编程实现：用递归函数求 1 + 2 + 3 + … + n 的和（n 由键盘输入）。',
     'def total(n):\n'
     '    if n == 1:                 # 出口\n'
     '        return 1\n'
     '    return n + total(n - 1)    # 递推\n'
     '\n'
     'n = int(input())          # 输入样例：100\n'
     'print("1 到", n, "的和是", total(n))\n',
     '100\n', None,
     '这是递归最朴素的模板，考试里换成"求 n 的平方和""求列表元素和"都是同一个套路。'
     '出口还可以写成 if n == 0: return 0，这样 n=0 也安全。', False),

    ('rec-p4', 7, ['recursion'],
     '编程实现：用递归函数完成汉诺塔（3 个盘子从 A 柱移到 C 柱，B 柱作辅助），'
     '打印每一步的移动过程。',
     'def hanoi(n, a, b, c):\n'
     '    if n == 1:                     # 只剩一个盘子，直接搬\n'
     '        print(a, "->", c)\n'
     '        return\n'
     '    hanoi(n - 1, a, c, b)          # 上面 n-1 个先搬到辅助柱\n'
     '    print(a, "->", c)              # 最大的那个搬到目标柱\n'
     '    hanoi(n - 1, b, a, c)          # 辅助柱上的 n-1 个搬到目标柱\n'
     '\n'
     'hanoi(3, "A", "B", "C")\n',
     '', None,
     '汉诺塔是"递归分解"的经典：把 n 个盘子的任务拆成三次调用。'
     '移动次数是 2ⁿ−1，3 个盘子 7 步。参数顺序 (n, 起点, 辅助, 终点) 别写乱，'
     '这是最容易出错的地方。', False),

    ('file-p1', 10, ['file'],
     '编程实现：读取当前目录下文本文件 test.txt 的前 8 个字符并打印出来。',
     'with open("test.txt", "r", encoding="utf-8") as f:\n'
     '    s = f.read(8)      # 读 8 个字符\n'
     'print(s)\n',
     '', {'test.txt': 'Python is a great language.\n'},
     'read(8) 在文本模式下读的是 8 个"字符"。文件里是"Python is a great language."，'
     '前 8 个字符是 "Python i"（P-y-t-h-o-n-空格-i）。用 with 就不用手写 f.close()。', False),

    ('file-p2', 10, ['file'],
     '编程实现：读取文件 word.txt 的全部内容，统计其中有多少个单词（以空格分隔）并输出。',
     'with open("word.txt", "r", encoding="utf-8") as f:\n'
     '    text = f.read()\n'
     'words = text.split()      # 不带参数：按任意空白（空格/换行/Tab）切分\n'
     'print("单词个数：", len(words))\n',
     '', {'word.txt': 'hello world python is fun\n'},
     'split() 不传参数才会按"任意空白"切分并自动丢掉空串；写 split(" ") 时'
     '连续空格和换行会产生空字符串元素，统计结果偏大——这是本题的判分陷阱。', False),

    ('file-p3', 10, ['file'],
     '编程实现：把一个二维列表写成的数据（姓名、成绩）保存为 CSV 格式文件 score.csv。',
     'rows = [["姓名", "成绩"], ["张三", "90"], ["李四", "85"]]\n'
     'with open("score.csv", "w", encoding="utf-8") as f:\n'
     '    for row in rows:\n'
     '        f.write(",".join(row) + "\\n")   # 一行内的字段用逗号连接\n'
     'print("已写入", len(rows), "行")\n',
     '', None,
     'join 的参数必须是"字符串的序列"，row 里混了 int 会抛 TypeError，'
     '所以要么全用字符串，要么 map(str, row)。写 CSV 每行末尾必须补 \\n，'
     '否则所有内容会挤成一行。', False),

    ('file-p4', 10, ['file'],
     '编程实现：向 note.txt 末尾追加一行"第三行"，然后读取整个文件，输出总行数和每一行内容。',
     'with open("note.txt", "a", encoding="utf-8") as f:\n'
     '    f.write("第三行\\n")          # a 模式：追加到末尾，不清空原内容\n'
     '\n'
     'with open("note.txt", "r", encoding="utf-8") as f:\n'
     '    lines = f.readlines()\n'
     '\n'
     'print("共", len(lines), "行")\n'
     'for line in lines:\n'
     '    print(line.strip())          # 去掉行尾换行符再打印\n',
     '', {'note.txt': '第一行\n第二行\n'},
     '注意两次 open 是分开的：先写后读必须重新打开（或用 "a+" 模式后 seek(0)）。'
     '换成 "w" 会把原来的两行清空，只剩一行——这是本题想考的区别。', False),

    ('hard-p1', 7, ['recursion', 'base'],
     '【附加题】编程实现：用递归把十进制正整数 n 转换成任意进制（2~16），'
     '并分别输出 26 的二进制和 255 的十六进制。',
     'def to_base(n, base):\n'
     '    digits = "0123456789ABCDEF"      # 超过 9 的数位用 A~F\n'
     '    if n < base:                     # 出口：只剩一位\n'
     '        return digits[n]\n'
     '    return to_base(n // base, base) + digits[n % base]\n'
     '\n'
     'print(to_base(26, 2))     # 11010\n'
     'print(to_base(255, 16))   # FF\n',
     '', None,
     '这题把两个必考点缝在一起：递归 + 数制转换。关键是"先递归求高位、再把当前位拼在后面"——'
     '所以是 to_base(...) + digits[n % base]，顺序反过来就成了倒序的错答案。'
     '这是附加题最可能出现的形态。', True),

    ('hard-p2', 10, ['file', 'recursion'],
     '【附加题】编程实现：统计 word.txt 中出现次数最多的 3 个单词（不区分大小写），'
     '按次数从多到少输出。',
     'with open("word.txt", "r", encoding="utf-8") as f:\n'
     '    text = f.read().lower()            # 统一成小写，避免 Python/python 分开统计\n'
     '\n'
     'counts = {}\n'
     'for w in text.split():\n'
     '    counts[w] = counts.get(w, 0) + 1   # 字典计数的标准写法\n'
     '\n'
     'top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:3]\n'
     'for w, c in top:\n'
     '    print(w, c)\n',
     '', {'word.txt': 'Python is easy\npython is fun\nPYTHON is everywhere\n'},
     '三处容易丢分：① 不转小写就统计（Python/python/PYTHON 变三个词）；'
     '② counts[w] = counts[w] + 1 会 KeyError，要用 get(w, 0)；'
     '③ sorted 的 key 忘了指定 kv[1]，结果按键名排序而不是次数。', True),

    ('hard-p3', 7, ['recursion'],
     '【附加题】编程实现：用递归实现快速排序，把列表 [5, 3, 8, 1, 9, 2] 从小到大排序并输出。',
     'def quick_sort(lst):\n'
     '    if len(lst) <= 1:                     # 出口：空表或单元素天然有序\n'
     '        return lst\n'
     '    pivot = lst[0]                        # 以第一个元素为基准\n'
     '    left = [x for x in lst[1:] if x < pivot]\n'
     '    right = [x for x in lst[1:] if x >= pivot]\n'
     '    return quick_sort(left) + [pivot] + quick_sort(right)\n'
     '\n'
     'print(quick_sort([5, 3, 8, 1, 9, 2]))\n',
     '', None,
     '快排的递归结构：出口（长度 ≤ 1）+ 分治（比基准小的、比基准大的）+ 合并。'
     '切片 lst[1:] 是必须的，否则基准自己会被重复比较，无限递归。', True),
]


def flat(text):
    return ' '.join(str(text).split())


def run_code(code, stdin, files):
    work = tempfile.mkdtemp(prefix='exam_extra_')
    try:
        for name, content in (files or {}).items():
            with open(os.path.join(work, name), 'w', encoding='utf-8') as f:
                f.write(content)
        path = os.path.join(work, '_main.py')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(code)
        env = dict(os.environ, PYTHONIOENCODING='utf-8')
        r = subprocess.run([PY, path], input=stdin or '', capture_output=True, text=True,
                           encoding='utf-8', errors='replace', env=env, cwd=work, timeout=30)
        return r.stdout.rstrip('\n'), r.stderr.strip()
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)


def main():
    items = []
    for qid, ch, typ, topics, stem, opts, ans, expl in MCQ:
        item = {
            'id': 'ex-' + qid,
            'chapter': ch,
            'chapterTitle': TITLES[ch],
            'type': typ,
            'exam': True,
            'topics': topics,
            'sourceKind': '考纲补充',
            'sourceFile': '2026-11 老师考纲 · 补充题',
            'sourceLocator': '考纲补充 · ' + ('选择题' if typ == 'single' else '填空题'),
            'stem': stem,
            'explanation': expl,
        }
        if typ == 'single':
            item['options'] = ['%s. %s' % (chr(65 + i), o) for i, o in enumerate(opts)]
            item['answer'] = ans
        else:
            item['answer'] = ans
            # 多空题用顿号分隔，显示更好看（判分时两种分隔符都会被忽略）
            item['answerText'] = ans[0].replace(',', '、')
        items.append(item)

    bad = []
    for qid, ch, topics, stem, code, stdin, files, expl, hard in CODE:
        out, err = run_code(code, stdin, files)
        if err:
            bad.append((qid, err[-300:]))
        item = {
            'id': 'ex-' + qid,
            'chapter': ch,
            'chapterTitle': TITLES[ch],
            'type': 'code',
            'exam': True,
            'topics': topics,
            'sourceKind': '考纲补充',
            'sourceFile': '2026-11 老师考纲 · 补充题',
            'sourceLocator': '考纲补充 · 编程题' + ('（附加）' if hard else ''),
            'stem': stem,
            'answer': code.rstrip('\n'),
            'output': out,
            'explanation': expl,
        }
        if hard:
            item['hard'] = True
        if stdin:
            item['stdin'] = stdin.rstrip('\n')
        if files:
            item['fixtures'] = {k: v for k, v in files.items()}
        items.append(item)

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=1)
    print('补充题 %d 道（客观 %d / 编程 %d）-> %s' % (
        len(items), len(MCQ), len(CODE), OUT))
    for qid, e in bad:
        print('  RUN FAIL', qid, e)
    for it in items:
        if it['type'] == 'code':
            print('  %-12s out=%r' % (it['id'], (it.get('output') or '')[:60]))


if __name__ == '__main__':
    main()
