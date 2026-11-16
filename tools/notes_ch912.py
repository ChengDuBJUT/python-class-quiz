# -*- coding: utf-8 -*-
"""把第 9-12 章（异常、文件、标准库、扩展库）的学习卡并进 code_notes.json。

内容依据 tools/source/newcode_runs.json 里的真实执行结果撰写；
凡输出里带时间戳 / pid / 随机数 / 本机路径的，注释里都点明「每次不同」。
"""
import io
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "source", "code_notes.json")

CARDS = {}

# ============ 第 9 章 异常处理 ============
CARDS["ch9/test1.py"] = {
    "title": "列表下标越界 + 链式比较的坑",
    "notes": [
        "ls[2] 取的是第 3 个元素，下标从 0 开始；写 ls[3] 就是 IndexError，注释掉的 print(name) 同理是 NameError。",
        "`print('y'<'x'==False)` 输出 False，不是 True。Python 把连续比较当成 and 连接：`'y'<'x' and 'x'==False`。",
        "因为 'y'<'x' 已经是 False，整条 and 直接短路成 False，右边的 'x'==False 根本没算。",
        "想表达「比较结果的布尔值」，必须写括号：`('y'<'x') == False`，那才是 True。",
    ],
    "pitfall": "把 `a < b == c` 误读成 `(a < b) == c` —— 这是链式比较，语义完全不同，考试最爱在这设坑。",
}

CARDS["ch9/test2.py"] = {
    "title": "访问不存在的属性 → AttributeError",
    "notes": [
        "class Car 里只定义了类属性 color='red'，car 实例自己没有 color，读 car.color 时向上到类里找，拿到 red。",
        "car.logo 在实例和类里都找不到，Python 不会返回 None，而是直接抛 AttributeError。",
        "这是 AttributeError 和 KeyError 的区别：字典取不存在的键、对象取不存在的属性，报的是不同的异常。",
    ],
    "pitfall": "以为「取不到就是 None」—— 只有 dict.get() 才会给默认值，属性访问不会。",
}

CARDS["ch9/test3.py"] = {
    "title": "try 包住 input，连输入错误一起接住",
    "notes": [
        "开头 `from chapter7.test19 import logit` 是跨章导入，运行时要让 pythonProject-2025 在 sys.path 里（脚本里已配好 PYTHONPATH）。",
        "输出里两行 `myfunc1 was called (3, 4){}` / `test31 was called (){}` 是 logit 装饰器自己打的日志，不是你的 print。",
        "input 写在 try 里面，所以输入非数字抛的 ValueError 和除零的 ZeroDivisionError 都会被同一个 except 接住。",
        "本例输入 10 和 2，输出「结果为 5.0」—— 除法 / 永远返回 float，不是 5。",
    ],
}

CARDS["ch9/test4.py"] = {
    "title": "try 的范围只包住 print，input 在保护圈外",
    "notes": [
        "num1、num2 的 int(input(...)) 写在 try 之前，这两行真出错（比如输入中文）没有任何保护。",
        "try 里只有 print(..., num1/num2)，所以 10/0 的 ZeroDivisionError 能被下面接住，打印「出错了,原因是： division by zero」。",
        "对比 test5：那边的 input 挪进了 try，ValueError 也能被接住 —— 这就是「try 包哪几行」的差别。",
        "except ... as error 里的 error 是异常对象，直接 print 它就打印异常消息。",
    ],
    "pitfall": "以为写了 try 就一定安全。try 只保护它缩进内的那几行，缩进外的错误照样让程序崩。",
}

CARDS["ch9/test5.py"] = {
    "title": "一个 except 同时接住多种异常（元组写法）",
    "notes": [
        "`except (ZeroDivisionError, ValueError) as error:` 括号里列出多个异常类型，命中任意一个都进这个分支。",
        "本例输入「张三」和 2，int('张三') 抛 ValueError，被接住并打印 invalid literal for int() with base 10: '张三'。",
        "用元组而不是写 `except ZeroDivisionError, ValueError:` —— Python 3 里后者是语法错误（Python 2 的老写法）。",
        "如果两种异常要分别处理，就写两个 except 分支；合并成一个说明你对它们的处理方式一样。",
    ],
}

CARDS["ch9/test6.py"] = {
    "title": "finally：不管出不出错都执行",
    "notes": [
        "输入 10 和 2，没异常，输出「结果为 5.0」，然后 finally 照样打印「今天天气不错！」。",
        "finally 的语义是「无论如何」，正常结束、异常被接住、甚至 try 里有 return，它都会跑。",
        "常用来收尾：关文件、断开连接、释放锁。",
        "except Exception 能接住几乎所有业务异常（KeyboardInterrupt、SystemExit 这类 BaseException 除外）。",
    ],
}

CARDS["ch9/test7.py"] = {
    "title": "else：只有 try 里没出错才走这里",
    "notes": [
        "结构是 try → except → else，本例 10/2 没异常，所以跳过 except，走 else 打印 5.0。",
        "else 的作用是把「成功后才做的事」和「容易被异常打断的事」分开，让 try 里只留可能抛错的那一行。",
        "注意两个 input 写在 try 外面，输入非数字会直接崩 —— 这是故意留的对比点。",
        "如果把 input 挪进 try，非数字输入就由 except 接，那时走的是 except 而不是 else。",
    ],
}

CARDS["ch9/test8.py"] = {
    "title": "try / except / else / finally 四件套全用上",
    "notes": [
        "本例输入 10 和 0，走 except 打印「出错了,原因是： division by zero」，然后 finally 打印「这是一定要执行的代码」。",
        "else 只有 try 不抛异常才执行，所以这次的输出里没有它。",
        "四个分支的执行顺序永远是：try →（有异常则 except，无异常则 else）→ finally。",
        "把 input 放在 try 里，输入非数字时也能被 except Exception 接住，不会崩。",
    ],
    "pitfall": "认为 finally 在 except 之后才决定要不要执行 —— 它是无条件执行的，哪怕 except 分支里又 raise。",
}

CARDS["ch9/test9.py"] = {
    "title": "raise 主动抛异常",
    "notes": [
        "`raise IndexError()` 是代码自己抛异常，没有真实的下标越界，所以没有任何 traceback 的业务原因，只有一行 IndexError。",
        "注释掉的 `raise IndexError('索引超出范围')` 会带上自定义消息，报错行显示 IndexError: 索引超出范围。",
        "raise 后面必须跟异常类或异常实例；`raise IndexError`（不带括号）也合法，Python 会自动实例化。",
        "主动抛异常常用于参数校验：不满足条件就立刻中止，而不是带着脏数据往下跑。",
    ],
}

CARDS["ch9/test10.py"] = {
    "title": "except 里再 raise：接住了又重新抛出",
    "notes": [
        "try 里 `raise IndexError('索引超出范围')` 抛出异常。",
        "`except:` 不带类型，接住所有异常（相当于 except BaseException），比 except Exception 更宽。",
        "关键在 `raise` 这一行：不带参数的 raise 表示「把当前正在处理的异常原样再抛出去」。",
        "所以程序最终还是崩了，报 IndexError: 索引超出范围 —— 接住不等于吞掉。",
    ],
    "pitfall": "在 except 里写 raise 却没意识到程序仍会终止；它的用途是「记录日志后交给上层处理」，不是「忽略这个错」。",
}

CARDS["ch9/test11.py"] = {
    "title": "assert 断言：条件不成立就抛 AssertionError",
    "notes": [
        "`assert num2 != 0, '除数不能为 0'` 等价于 `if not (num2 != 0): raise AssertionError('除数不能为 0')`。",
        "本例输入 10 和 0，断言失败，输出停在提示语后面，抛 AssertionError: 除数不能为 0。",
        "注释掉的那两行 if 判断就是想对比：assert 是更短的自检写法。",
        "assert 会被 python -O 优化掉，所以别用它做必须执行的业务校验，只用于「调试期自检」。",
    ],
}

CARDS["ch9/test12.py"] = {
    "title": "自定义异常类：带 length / atleast 两个属性",
    "notes": [
        "class ShortInputError(Exception) 继承 Exception，就成为一个能被 raise / except 的异常类型。",
        "__init__ 里把 length、atleast 存成实例属性，所以 except 里可以用 error.length 取出来。",
        "本例输入 123（长度 3 < 6），raise ShortInputError(3, 6)，输出「输入密码的长度是3,密码长度至少应该是6」。",
        "注意 except 用的是 Exception：因为自定义异常也是 Exception 的子类，所以能接住。",
        "如果用 `except ShortInputError as error` 更精确，避免把别的异常也当密码错误处理。",
    ],
    "pitfall": "自定义异常忘了调 super().__init__()（本例没存 message 所以不影响），但继承 Exception 后想打印消息时就要传。",
}

CARDS["ch9/test13.py"] = {
    "title": "异常沿调用链层层上传：div → mul → test",
    "notes": [
        "执行顺序看输出：mul() 先启动并要乘数，然后才调 div() 要两个输入。本例输入 3、10、0。",
        "div() 里 10/0 抛 ZeroDivisionError，except 里 `raise error` 把它原样再抛，交给调用者 mul()。",
        "mul() 没有 try，异常继续上传到 test()；test() 的 except 打印「test--捕获到异常信息division by zero」后又 raise 一次。",
        "最后 test() 也没人接，异常传到顶层，程序以 traceback 结束 —— 输出的 traceback 里能看到 div 里两次 raise 的位置。",
        "这说明 except + raise 只是「路过时记一笔」，不能阻止异常继续往上走。",
    ],
    "pitfall": "以为在内层 except 里处理过就不再往上抛；只要写了 raise（或根本不写 try），异常都会继续上传到顶层。",
}

# ============ 第 10 章 文件与编码 ============
CARDS["ch10/test1.py"] = {
    "title": "ord / chr 与字符编码",
    "notes": [
        "ord('A') 得到 65，bin(65) 得到 0b1000001 —— bin() 返回带 0b 前缀的二进制字符串。",
        "ord('中') 得到 20013，说明中文字符在 Unicode 里也是单个码位，不是按字节拆开的。",
        "chr(65) 反向得到 A，chr(20013) 得到 中，和 ord 互为逆运算。",
        "`print((3.5*4.6)==True)` 输出 False：浮点结果 16.1 与 True(即 1) 不相等，浮点比较别和布尔值混着写。",
    ],
}

CARDS["ch10/test2.py"] = {
    "title": "open('w') 的模式、closed 状态与关闭后写入",
    "notes": [
        "open(..., 'w') 是只写模式：文件不存在就新建，已存在就清空重写。",
        "f.name 是 'test.txt'，f.mode 是 'w'，f.closed 是 False —— 三个都是文件对象的属性，不是方法，不用加括号。",
        "f.write() 返回写入的字符数，这里没接收返回值，所以看不到。",
        "f.close() 之后 `print(\"1: \" + str(f.closed))` 输出 1: True；紧接着再 f.write(...) 就抛 ValueError: I/O operation on closed file. —— 这是故意演示。",
    ],
    "pitfall": "忘了 close 就想继续读写；用 with 语句可以避免这个错误（见 test3）。",
}

CARDS["ch10/test3.py"] = {
    "title": "with 语句：出块就自动关闭",
    "notes": [
        "with open(...) as f 在块的末尾自动调 f.close()，不用手写。",
        "块内打印 f.name=test.txt、f.mode=w、f.closed=False。",
        "块外再打印 f.closed，得到 True —— 说明 f 这个变量还在（Python 没有块级作用域），只是文件已关。",
        "所以 with 结束后不能再用 f 读写，否则和 test2 一样报 I/O operation on closed file。",
    ],
}

CARDS["ch10/test4.py"] = {
    "title": "自己写上下文管理器：__enter__ / __exit__",
    "notes": [
        "进入 with 块时自动调 __enter__()，它返回的对象绑定给 as 后面的 a，所以 a 就是 MyContext 实例。",
        "__exit__(e_t, e_v, t_b) 接三个参数：异常类型、异常值、traceback 对象。块内正常结束时它们全是 None。",
        "本例块内 raise ValueError('bjut error')，所以 e_t 打印 <class 'ValueError'>，e_v 打印 bjut error，t_b 打印一个 traceback 对象。",
        "__exit__ 的返回值决定异常是否被吞掉：这里没有 return，等价返回 None（假值），异常继续抛出，所以程序最后报 ValueError: bjut error。",
        "想让 with 块里的异常不往外传播，就在 __exit__ 里 return True。",
    ],
    "pitfall": "以为 __exit__ 会自动吃掉异常 —— 默认不会，必须显式 return True。",
}

CARDS["ch10/test5.py"] = {
    "title": "f.write() 的返回值是写入的字符数",
    "notes": [
        "string 共 45 个字符（含两个换行符 \\n），f.write(string) 返回 45，所以输出 45。",
        "write 只接受字符串，写数字要先 str() 转换（注释里那句「只能写入字符串」就是这个意思）。",
        "write 不会自动加换行，需要自己在字符串里写 \\n。",
    ],
}

CARDS["ch10/test6.py"] = {
    "title": "f.writelines() 与 write() 的区别",
    "notes": [
        "本例传的是字符串而不是列表，writelines 会把字符串当成字符序列，逐个字符写出去，效果上等于 write。",
        "writelines 的返回值是 None（所以输出 None），而 write 返回写入字符数 —— 这是两者最容易考的差别。",
        "writelines 也不会自动在每个元素后加换行，列表里的每行要自己带 \\n。",
    ],
    "pitfall": "以为 writelines 会帮忙加换行；它只是「把一堆字符串依次写进去」，返回值永远是 None。",
}

CARDS["ch10/test7.py"] = {
    "title": "readlines() 保留行尾换行符",
    "notes": [
        "readlines() 返回列表，每个元素是一行，而且行尾的 \\r\\n 原样保留。",
        "print 又自带一个换行，所以输出里每行之间多出一个空行 —— 这不是代码写错，是双重换行。",
        "想避免就写 print(a[b].strip()) 或 print(a[b], end='')。",
        "本例读到的 test.txt 是章节目录里那份：第 1 行 Python is a great language.，第 2 行 Bjut is a good university.。",
        "f 后面那个分号 `a = f.readlines();` 是 Python 允许但不推荐的写法。",
    ],
}

CARDS["ch10/test8.py"] = {
    "title": "tell() 记录当前读到的位置（字符数）",
    "notes": [
        "刚打开时 tell() 是 0。",
        "read(5) 读 5 个字符，得到 Pytho。",
        "再 tell() 得到 5 —— 文本模式下位置按字符算，一个中文也算 1。",
        "打开的 test.txt 第一行是 Python is a great language.，所以前 5 个字符正好是 Pytho。",
    ],
}

CARDS["ch10/test9.py"] = {
    "title": "seek 的三种 whence：0 开头 / 1 当前 / 2 末尾",
    "notes": [
        "`f.seek(5, 0)` 从文件开头往后移 5 个字节；`f.seek(3, 1)` 从当前位置再往后 3 个字节。",
        "seek 的返回值是新的绝对位置：先到 5，再 +3 得 8，所以打印 8，接着 tell() 也是 8。",
        "注意这个例子用的是 'rb' 二进制模式，二进制下位置按字节算，所以能看到 b's a great language.\\r\\n...' 这样的原始字节串。",
        "文本模式做相对 seek 有限制（只能 seek(0, 2) 或回到 0），带 whence=1 的相对偏移要配合 'rb' 用。",
        "从第 8 个字节开始读，得到 s a great language. 加 CRLF 和下一行 —— 说明之前跳过了 Pytho 和 n 后的第 8 个字符。",
    ],
}

CARDS["ch10/test10.py"] = {
    "title": "一次读完再按逗号切分 —— 行尾 \\r\\n 会把两行粘在一起",
    "notes": [
        "`'&'.join(ls)` 把列表用 & 连成一个字符串，输出 小米&华为&苹果 —— join 是「用分隔符连接列表」，不是 split 的逆操作那么直观。",
        "读文件用的是 `f.read().strip('\\n').split(',')`：strip 只去掉首尾的换行，文件中间的 \\r\\n 原样保留。",
        "所以 split(',') 之后，每行最后一个字段会和下一行第一个字段粘成 '4\\n5' 这种 —— 输出里的列表就能看到 '4\\n5'、'8\\n9'、'12\\n13'、'16\\n17'。",
        "这段代码本意是按行切成二维结构，用 read 一次读完是错的；正确做法是按行遍历（见 test11）。",
        "文件里的 demo.csv 每行是逗号分隔的 4 个数字，共 5 行。",
    ],
    "pitfall": "strip('\\n') 只清首尾，不管中间。想按行切就得 splitlines() 或按行遍历，别指望 strip 能救。",
}

CARDS["ch10/test11.py"] = {
    "title": "逐行读 CSV：唯一正确的切分方式",
    "notes": [
        "for line in f 每次拿到一行（含行尾 \\r\\n），`line.strip('\\n').split(',')` 把它切成 4 个字段的列表。",
        "输出是二维列表 [[...], [...], ...]，共 5 行，每行 4 个字符串 —— 注意全是字符串，不是数字。",
        "ls[2][3] 是第 3 行第 4 列，得到 '12'；ls[3][3] 是 '16'；相加要先 int() 转换，所以写 int(...)+int(...) 得 28。",
        "开头三引号那段注释是写文件的代码（生成 demo.csv 的内容），被注释掉了，只留读取部分。",
    ],
    "pitfall": "直接 '12' + '16' 会得到 '1216'（字符串拼接），必须 int() 转成数字再算。",
}

# ============ 第 11 章 标准库 ============
CARDS["ch11/test1.py"] = {
    "title": "os 模块：getcwd / listdir / mkdir",
    "notes": [
        "os.getcwd() 打印当前工作目录。这里显示的是一个临时目录，因为示例脚本是在独立临时目录里跑的，不是章节目录。",
        "`path=r'd:\\test'` 这个路径是老师本机的目录，本机没有 d 盘这个路径，所以 os.listdir 抛 FileNotFoundError: 系统找不到指定的路径。",
        "r'...' 表示原始字符串，反斜杠不转义 —— Windows 路径必须这么写，否则 \\t 会被当成制表符。",
        "os.mkdir(path2) 建目录，只能建一级，父目录不存在会报错；要多级用 os.makedirs。",
        "注释掉的 os.remove 是删除文件（不是目录，删目录用 os.rmdir / shutil.rmtree）。",
    ],
    "pitfall": "路径写死成自己机器上的 d:\\test，换台电脑就崩。考试里如果考「这段为什么报错」，答案就是路径不存在。",
}

CARDS["ch11/test2.py"] = {
    "title": "sys 模块：解释器与运行环境信息",
    "notes": [
        "sys.version 是解释器版本串，sys.platform 在 Windows 上是 win32。",
        "sys.path[0] 是脚本所在目录（不是当前工作目录），sys.path 才是模块搜索路径列表。",
        "sys.argv 是命令行参数列表，第 0 个是脚本路径；这里没用命令行参数，所以只有一个元素。",
        "sys.stdin 打印出来是 <_io.TextIOWrapper name='<stdin>' mode='r'>，说明标准输入也是个文件对象，可以用 read/readline。",
        "sys.executable 是当前 python 解释器的绝对路径 —— 这些值每台机器都不同，别背输出，要记「各代表什么」。",
    ],
}

CARDS["ch11/test3.py"] = {
    "title": "sys.stdin.readline 与 input 的长度差一位",
    "notes": [
        "sys.getdefaultencoding() 输出 utf-8，说明源码里的中文按 UTF-8 编码。",
        "循环两轮，每轮先 sys.stdin.readline() 再 input('请输入：')，所以要喂 4 行输入。",
        "本例输入 hello / hi / world / bye：readline 读到 'hello\\n'，len 是 6（把换行算进去了）；input 读到 'hi' 并自动去掉换行，len 是 2。",
        "打印顺序是 readline 的 len（6）、再用 sys.stdout.write 打印一次 6（write 不像 print 会自动换行，代码自己加了 \\n），然后才是 input 的 2。",
        "sys.exit(8) 让进程以退出码 8 结束 —— 正常退出是 0，非 0 表示异常结束。",
    ],
    "pitfall": "忘记 readline 会把行尾 \\n 算进 len：同样输入 hello，readline 得到 6，input 得到 5。",
}

CARDS["ch11/test4.py"] = {
    "title": "time 模块：时间戳 → 结构体 → 字符串 → 再解析回来",
    "notes": [
        "time.time() 返回从 1970-01-01 起的秒数（浮点），本例 t1 是一个大数；time.ctime(t1) 把它转成可读串。",
        "time.localtime(t1) 得到本地时区的 struct_time（本例小时是 15），time.gmtime(t1) 得到 UTC（小时是 7），两者差 8 小时就是时区差。",
        "time.strftime('%Y-%m-%d %H:%M:%S', t2) 把结构体格式化成字符串；time.strptime(...) 是逆操作，把字符串解析回结构体。",
        "time.perf_counter() 是高精度计时器，本例前后差 1.018 秒 —— 因为中间有 time.sleep(1)。",
        "所有具体时间数值每次都变，学习时只看「谁转成谁」，别记数字。",
    ],
}

CARDS["ch11/test5.py"] = {
    "title": "datetime.date 的构造与各种转换",
    "notes": [
        "datetime.date(2023, 4, 13) 手工造一个日期；date.today() 取今天。",
        "date.fromtimestamp(t0) 把时间戳转成日期，date.toordinal(d2) 转成「从公元 1 年 1 月 1 日起的第几天」。",
        "date.timetuple(d2) 得到 struct_time，和 time 模块的结构体是同一个东西。",
        "date.isoweekday(d2) 返回 1-7（周一是 1）；date.isocalendar 返回 (年, 第几周, 星期几)；date.isoformat 返回 'YYYY-MM-DD' 字符串。",
        "输出的具体日期随运行日期变化（本例是 2026-11-16），考试看方法名和返回类型即可。",
    ],
}

CARDS["ch11/test6.py"] = {
    "title": "calendar 模块：首周日、闰年判断、打印月历",
    "notes": [
        "calendar.firstweekday() 返回本周第一天，默认 0 表示周一。",
        "calendar.setfirstweekday(0) 显式设成周一，再读还是 0 —— 本例只是演示读写同一属性。",
        "calendar.isleap(2022) 返回 False，2022 不是闰年。",
        "calendar.month(2026, 5, w=2, l=1) 直接打印 2026 年 5 月的月历：w 是列宽，l 是每周的行数。",
        "月历输出是分多行的字符串，前面两个空格表示 5 月 1 日是周五。",
    ],
}

CARDS["ch11/test7.py"] = {
    "title": "math 模块：nan / fabs / log2 / 弧度与三角函数",
    "notes": [
        "math.nan 是「非数字」，打印出来就是 nan；判断它要用 math.isnan(x)，不能用 == nan（永远 False）。",
        "math.fabs(-10) 返回 10.0，注意是浮点，和内置 abs(-10) 返回整数 10 不同。",
        "math.log2(5) 约 2.3219，是 log 以 2 为底。",
        "math.sin 这类三角函数吃的是弧度，所以先用 math.radians(60) 把 60 度转成 1.0472 弧度，sin 得到 0.866。",
        "直接 math.sin(60) 会得到 -0.3048，因为 60 被当成 60 弧度了 —— 这是最常见的错。",
    ],
    "pitfall": "角度直接丢给 sin/cos，忘了 math.radians 转换，结果完全不对。",
}

CARDS["ch11/test8.py"] = {
    "title": "random.seed(100)：种子固定，结果可复现",
    "notes": [
        "random.seed(100) 之后，整串随机结果就固定了：random() 得 0.1457…、randint(1,10) 得 8、uniform(1.1,5.4) 得 5.19…。",
        "换台机器、换个 Python 版本，同一个种子也基本能复现同一串 —— 这是随机实验可重复的关键。",
        "random.choice 从序列里挑一个，本例挑到 剪刀；random.randrange(1,100,2) 在 1-99 的奇数里挑，得到 91。",
        "random.sample(字符串, 5) 不重复抽 5 个字符；random.shuffle(r) 原地打乱列表并返回 None（所以不能写 print(random.shuffle(r))）。",
        "不调 seed 时，种子取自系统时间，每次结果都不同。",
    ],
    "pitfall": "randint(a, b) 是闭区间（两端都可能取到），而 randrange(a, b) 是左闭右开 —— 差一个数的经典坑。",
}

CARDS["ch11/test9.py"] = {
    "title": "multiprocessing.Process：父子进程各跑各的",
    "notes": [
        "Process(target=task_process) 创建子进程，start() 之后子进程和父进程并发执行。",
        "输出里子进程 pid 是一个值，父进程 pid 是另一个值；pid 每次运行都不同，别记数字。",
        "子进程里 for i in range(5) 连着打印 5 次，中间那句 time.sleep(2) 被注释掉了，所以 5 次几乎是同时出来的。",
        "父进程循环 3 次、每次 sleep(2)，所以父进程的三行大约在第 0、2、4 秒出现。",
        "`if __name__ == '__main__':` 在 Windows 上必须写，否则会无限递归创建子进程 —— Windows 用 spawn 方式启动新进程，会重新 import 这个文件。",
    ],
    "pitfall": "Windows 下漏掉 if __name__ == '__main__' 保护，程序会疯狂自我复制直到崩溃（RuntimeError: already started）。",
}

CARDS["ch11/test10.py"] = {
    "title": "继承 Process 并重写 run()",
    "notes": [
        "class MyProcess(Process) 里重写 run()，进程启动时执行的就是 run() 里的代码，不用再传 target。",
        "__init__ 里的 super().__init__() 必须调，否则 Process 的内部状态没初始化，start() 会报错。",
        "子进程循环 3 次、每次 sleep(1)，父进程也是 3 次、每次 sleep(1)，所以两边的行会交错出现。",
        "本例输出的顺序是父进程 3 行在前、子进程 3 行在后 —— 实际顺序不保证，取决于操作系统调度。",
        "继承方式和 target 方式只是写法不同，本质都是「另起一个进程跑一段函数」。",
    ],
}

CARDS["ch11/test11.py"] = {
    "title": "threading.Thread(target=...)：线程共享进程",
    "notes": [
        "Thread(target=task_thread) 创建线程，start() 启动；主线程 continue 往下跑，两者交替输出。",
        "输出里的时间戳和交错顺序每次都不一样：本例先子后父、再父后子，换个时间跑可能正好相反。",
        "threading.currentThread().name 拿当前线程名：主线程叫 MainThread，新建的线程叫 Thread-1（新版 Python 显示成 Thread-1 (task_thread)）。",
        "currentThread() 在新版 Python 已弃用，正确写法是 current_thread()（运行时会打 DeprecationWarning，不影响结果）。",
        "线程和进程的区别：线程共享内存，改同一个变量会互相影响；进程各自独立，要通过队列/管道通信。",
    ],
}

CARDS["ch11/test12.py"] = {
    "title": "继承 Thread 并重写 run()",
    "notes": [
        "class MyThread(Thread) 重写 run()，start() 之后执行的就是 run()。",
        "输出里父线程 2 行、子线程 2 行，顺序交替，具体谁先谁后不固定。",
        "子线程名是 Thread-1，主线程名是 MainThread —— 和 test11 的 target 写法一致。",
        "如果想等子线程跑完再继续，调 thread.join()；本例没调，主线程跑完就直接退出。",
        "currentThread() 同样已弃用，用 current_thread()。",
    ],
}

CARDS["ch11/test13.py"] = {
    "title": "asyncio 协程：两个任务交替 await",
    "notes": [
        "async def 定义协程函数，调用它不会立刻执行，只得到一个协程对象。",
        "loop.create_task(...) 把协程包装成任务并排进事件循环，两个任务都进队列后才会并发推进。",
        "每个协程里循环 2 次，每次 await asyncio.sleep(2) 两回，所以每个任务总耗时约 8 秒，两个任务交替打印。",
        "输出里协程 1 和协程 2 的时间戳成对出现（例如都是 15:00:25），说明它们在同一个事件循环里交替执行，不是串行跑完一个再跑另一个。",
        "注意 `loop.run_until_complete(task1)` 再 `task2`：task2 在 task1 期间其实也在跑，所以第二次调用很快就结束。",
        "新版 Python 推荐用 asyncio.run(main()) 代替手动 get_event_loop。",
    ],
    "pitfall": "以为 async def 里不写 await 也会并发；没有 await 的话协程就是普通函数，整段同步执行完才交还控制权。",
}

# ============ 第 12 章 扩展库 ============
CARDS["ch12/test1.py"] = {
    "title": "numpy 数组与 axis 的方向",
    "notes": [
        "np.array(嵌套列表) 把二维列表变成 ndarray，打印时没有逗号、按矩阵对齐。",
        "np.max(data, axis=0) 求每列最大值，得到 [7 8 9]；axis=1 才是每行最大值，得到 [3 6 9]。",
        "axis 记法：axis=0 沿「行方向」压扁，也就是把每一列纵向聚合成一个值 —— 所以结果长度等于列数。",
        "不加 axis 就是对全部元素求一个值。",
        "np.mean(data) 输出 5.0（1 到 9 的平均），另写了 median / var / std 但没 print，所以看不到结果。",
        "最后一行 data.ndim 只取值没打印，所以没有输出。",
    ],
    "pitfall": "把 axis=0 记成「按行」—— 实际 axis=0 是跨行聚合（每列一个结果）。",
}

CARDS["ch12/test2.py"] = {
    "title": "pandas 的 Series 与 DataFrame：shape / ndim / axes",
    "notes": [
        "pd.Series(np.random.uniform(-0.5,1,10)) 生成 10 个 -0.5~1 的随机数，左侧自动配 0-9 的索引。",
        "dser.get(1) 按索引标签取值，得到第 2 个元素（索引 1），本例 0.136…。",
        "dser.shape 是 (10,)，ndim 是 1；ddat.shape 是 (4, 4)，ndim 是 2 —— 这是 Series 和 DataFrame 最本质的区别。",
        "axes 打印的是索引对象：Series 一个 RangeIndex，DataFrame 两个（行索引 + 列索引）。",
        "head(2) 只取前 2 行；isnull() / notnull() 返回同形状的布尔表（本例没有缺失值，所以全 False / 全 True）。",
        "dser.sum() 是全部元素求和，dser.mean() 是平均值 —— 这两个值每次运行都不同，因为数据是随机生成的。",
    ],
}

CARDS["ch12/test3.py"] = {
    "title": "matplotlib 画图：控制台没有任何输出",
    "notes": [
        "fig = plt.figure(num=1, figsize=(4,4)) 建一个 4×4 英寸的画布，编号 1。",
        "plt.plot([1,2,3,4], [1,2,3,2]) 用两组数画折线，x 是 1-4，y 是 1、2、3、2。",
        "plt.show() 弹出窗口显示图 —— 在无界面环境（后端是 Agg）下不会弹窗，只会提示 FigureCanvasAgg is non-interactive。",
        "所以这段代码「没有输出」是正常的：结果是图，不是文字。",
        "想存图用 plt.savefig('a.png')；想在没有显示器的机器上跑，设 MPLBACKEND=Agg。",
    ],
}

CARDS["ch12/test4.py"] = {
    "title": "jieba 分词三种模式：精确 / 全 / 搜索引擎",
    "notes": [
        "cut(..., cut_all=False) 是精确模式，输出 小红，打算，到，中国科学院，研究生院，图书馆，学习 —— 不重复、不遗漏。",
        "cut(..., cut_all=True) 是全模式，把句子所有可能成词的组合都列出来，所以会有 中国、中国科学院、科学、科学院、学院 这种重叠项。",
        "cut_for_search 是搜索引擎模式，在精确模式基础上把长词再切出短词（中国科学院 → 中国、科学、学院、科学院、中国科学院），便于检索召回。",
        "三种模式的对比是这章的常考点：精确模式用于正文分析，全模式用于关键词扫描，搜索模式用于建索引。",
        "首次运行会在 stderr 打印 Building prefix dict… 和 Loading model cost … 的日志，那是 jieba 在加载词典，不是报错。",
    ],
}

CARDS["ch12/test5.py"] = {
    "title": "jieba.posseg 词性标注",
    "notes": [
        "pseg.cut 返回的不是字符串而是 (词, 词性) 对，可以直接解包成 w.word 和 w.flag。",
        "输出：我 r（代词）、爱 v（动词）、北京 ns（地名）、天安门 ns（地名）。",
        "常用词性缩写：n 名词、v 动词、a 形容词、r 代词、ns 地名、nr 人名、m 数词。",
        "和 cut 一样，首次运行会有加载词典的日志输出到 stderr。",
    ],
}

CARDS["ch12/test7.py"] = {
    "title": "三目表达式 + 链式比较 + 函数对象没加括号",
    "notes": [
        "`c = a if a>b else a+b` 是 Python 的条件表达式：a=1、b=2，条件不成立，所以 c 取 a+b=3。但 c 没打印，所以输出里看不到。",
        "`print('y'<'x'==False)` 输出 False，链式比较等价于 `'y'<'x' and 'x'==False`，左边就短路了。",
        "`print(time.ctime)` 输出 `<built-in function ctime>` —— 忘了加括号，打印的是函数对象本身，不是调用结果。",
        "`print(time.localtime())` 打印的是 struct_time 结构体，不是格式化字符串。",
        "这三行凑在一起就是典型的「看起来都会，实际全是坑」的复习题。",
    ],
    "pitfall": "print 函数名忘了加括号，输出 <built-in function ...>；print 结构体忘了格式化，输出一串 tm_year=...。",
}

CARDS["ch12/test8.py"] = {
    "title": "位运算：右移 >>、按位与 &、按位取反 ~",
    "notes": [
        "输入 20，bin(20) 是 0b10100。",
        "a>>4 把 20 的二进制右移 4 位，得到 1（0b10100 → 0b1），相当于整除 2 的 4 次方。",
        "`~(~0<<4)` 是构造低 4 位全 1 的掩码：~0 是 -1（全 1），左移 4 位得到 ...11110000，再取反得 0b1111（即 15）。",
        "b & c 即 1 & 15，结果是 1，打印 0b10100,0b1。",
        "位运算常用来做掩码、开关状态、颜色通道拼接；负数的 ~ 涉及补码，别用十进制直觉去推。",
    ],
}


def main():
    if os.path.exists(OUT):
        with io.open(OUT, encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    before = len(data)
    data.update(CARDS)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("cards %d -> %d (added %d)" % (before, len(data), len(data) - before))
    for ch in ("ch9", "ch10", "ch11", "ch12"):
        n = sum(1 for k in data if k.startswith(ch + "/"))
        print("  %s: %d" % (ch, n))


if __name__ == "__main__":
    main()
