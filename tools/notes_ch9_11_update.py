# -*- coding: utf-8 -*-
"""补 ch9-11 老师更新版代码的学习卡（title / notes / pitfall）。"""
import json

P = 'tools/source/code_notes.json'
notes = json.load(open(P, encoding='utf-8'))
new = {}

new['ch9/test6.py'] = {
    "title": "try / except / else / finally：老师这版加上了 else 分支",
    "notes": [
        "新版把 `print(\"结果为\",num1/num2)` 拆成「先算 result，再在 else 里 print(result)」，所以成功路径的输出从「结果为 5.0」变成了光秃秃的 `5.0`。",
        "输入 10 和 2：try 正常算完 → 跳过 except → 进 else 打印 result → 最后 finally 无条件打印「今天天气不错！」。",
        "else 的语义是「try 里没出错才执行」，不是「否则」；它和 except 互斥，两个最多只走一个。",
        "顺序固定：try → except（出错时）/ else（没出错时）→ finally（无论如何）。",
        "把 print 放 else 里还有个好处：try 块只装可能出错的代码，出错边界更清楚。",
    ],
    "pitfall": "else 里打印的是 result；一旦 try 中途抛异常，result 压根没被赋值，但 else 会被整个跳过，所以不会 NameError。反过来，把 print(result) 挪回 try 里再让它出错，就抓不住这个错了。",
}

new['ch9/test10.py'] = {
    "title": "except 里再 raise：接住了又重新抛出去（新版只多了行 #pass 注释）",
    "notes": [
        "新版唯一改动是 except 块里加了一行 `#pass`，它是注释，代码行为一点没变。",
        "`raise IndexError('索引超出范围')` 抛异常 → `except:` 接住 → 下一行 `raise` 不带参数，表示「把当前正在处理的异常原样再抛」。",
        "所以程序最终还是崩了：IndexError: 索引超出范围。接住不等于吞掉。",
        "老师把 `#pass` 摆在这儿是在暗示：如果这行不是注释而是真的 `pass`，程序就会静默通过、正常结束 —— 这是本段唯一会改变输出的开关。",
        "`except:` 不带类型等价于 `except BaseException`，连 Ctrl+C 都接；正常写代码应该用 `except Exception`。",
    ],
    "pitfall": "考试常考「把 pass 换成 raise（或反过来）输出怎么变」：有 raise 会崩，只有 pass 则程序正常结束、什么都不打印。",
}

new['ch10/test2.py'] = {
    "title": "open 的模式从 w 改成 a：追加而不是清空",
    "notes": [
        "老师这版把模式从 `w` 改成 `a`：w 是清空重写，a 是追加到文件末尾；文件不存在时两者都会新建。",
        "写入的两行内容换成了带学号的 `Python is a great language 11161338.`，而且两行都带换行（旧版第二行故意不带）。",
        "输出四行：`f.name: test.txt`、`a`、`False`（关闭前 closed 为 False）、`1: True`（关闭后为 True）。",
        "旧版最后那行 `f.write(...)` 写在 close 之后，会抛 ValueError: I/O operation on closed file；新版把它注释掉了，所以这段代码不再报错。",
        "a 模式指针自动落在文件末尾，所以同一段代码跑 N 次，文件就长 N 倍（本站每个文件在独立临时目录跑，不会污染课件目录）。",
    ],
    "pitfall": "w 会清空文件、a 不会；close 之后再 write/read 一律 ValueError。给「同一文件被打开两次」的题判最终内容时，先看模式，再看有没有 close。",
}

new['ch10/test4.py'] = {
    "title": "上下文管理器 __enter__ / __exit__ 的调用时机（顺手修了个拼写）",
    "notes": [
        "新版只把 `MyContestManager` 改成了 `MyContextManager`，是一处拼写笔误的修正，逻辑完全没动。",
        "`with MyContext() as a:` 的执行顺序：先调 `__enter__()`（打印并 return self，所以 a 就是这个对象），再执行 with 块，最后退出时调 `__exit__()`。",
        "这段代码的输出顺序：__enter__() called → my name is MyContextManager → a is called → __exit__() called → e_t / e_v / t_b 三行。",
        "`__exit__(self, e_t, e_v, t_b)` 的三个参数是异常类型、异常值、traceback；with 块里 `raise ValueError(\"bjut error\")` 之后它们都有值。",
        "`__exit__` 没有 return（等于返回 None/False）→ 异常不会被吞，继续往上抛，所以最后还能看到 ValueError: bjut error。",
    ],
    "pitfall": "__exit__ 返回 True 才是「吞掉异常」，返回 None/False 会继续抛。这就是为什么这道题的输出里既有 __exit__ 的打印、结尾又有 traceback。",
}

new['ch10/test8.py'] = {
    "title": "tell() 看指针位置：新版加了 encoding，read(5) 改成 read(2)",
    "notes": [
        "`open('test.txt', encoding='utf-8')` 显式指定编码。文本模式不写 encoding 会按系统默认（中文 Windows 上是 GBK），读带中文的文件容易乱码或 UnicodeDecodeError。",
        "刚打开时 tell() 是 0；`read(2)` 读走两个字符 'Py'；再 tell() 得到 2。",
        "文本模式下 tell() 返回的是「字符位置」，二进制模式（'rb'）才是字节位置 —— 对比 test9 输出的 8 就明白了。",
        "老师把 read(5) 改成 read(2)，是为了让打印短、一眼能数清读了几个字符。",
    ],
    "pitfall": "文本模式 tell 的数值不能拿去当字节偏移用；要精确控制字节就开 'rb'。",
}

new['ch10/test9.py'] = {
    "title": "二进制模式 seek + tell：read(3) 出来的是 bytes",
    "notes": [
        "`open('test.txt','rb')` 是二进制模式，读出的是 bytes，所以打印成 `b's a'` 而不是 `s a`。",
        "`f.seek(5,0)` 从文件开头前进 5 → 位置 5；`local = f.seek(3,1)` 从当前位置再前进 3 → 位置 8，并且 seek 会把新位置作为返回值给你。",
        "所以输出三行：`8`（seek 的返回值）、`8`（tell 确认）、`b's a'`（第 8 个字节起读 3 个）。",
        "test.txt 开头是 `Python is a great language.`：P0 y1 t2 h3 o4 n5 空格6 i7 s8 → 从 8 开始三个字节正好是 s、空格、a。",
        "seek 第二个参数：0 文件开头、1 当前位置、2 文件末尾；文本模式下只允许 0，用 1/2 会报 io.UnsupportedOperation。",
    ],
    "pitfall": "`f.seek(3,1)` 的返回值是「新位置」不是「移动了几个字节」；文本文件里用 1/2 相对定位会直接报错，老师这版特意保留 rb 就为这个。",
}

new['ch10/test10.py'] = {
    "title": "老师把 read().split(',') 改成 readlines 逐行切分 —— 这才是正确的二维读法",
    "notes": [
        "旧版 `f.read().strip('\\n').split(',')` 把整份文件拍成一维，行尾的 \\r\\n 还留在元素里，会出现 '4\\n5' 这种脏数据。",
        "新版先用 `f.readlines()` 拿到「每行一个字符串」，再对每行 `strip('\\n').split(',')`，得到干净的二维列表。",
        "输出第二行就是结果：`[['1','2','3','4'], ['5','6','7','8'], ['9','10','11','12'], ['13','14','15','16']]`，4 行 4 列。",
        "第一行 `小米&华为&苹果` 是上面那段 join 的演示，和读文件无关。",
        "demo.csv 里的数字都是字符串，所以列表元素带引号，要当数字用还得 int() 一下。",
    ],
    "pitfall": "读 CSV 别用 read() + split(',')：它分不清行边界，会把 '4\\r\\n5' 这种跨行内容粘成一个元素。要么 splitlines() 再逐行 split，要么直接用 csv 模块。",
}

new['ch10/test10-1.py'] = {
    "title": "新增文件：用 join 生成 demo.csv，给 test10 准备数据",
    "notes": [
        "这是老师新加的文件，专门负责写 demo.csv：4 行 4 列的数字字符串。",
        "核心写法 `f.write(\",\".join(row) + \"\\n\")`：join 把一行里的 4 个字段用逗号连成一个字符串，再补换行，一次写一行 —— 最朴素的 CSV 写文件方式。",
        "`open(\"demo.csv\",\"w\")` 没指定 encoding，中文 Windows 下按 GBK 写；这次内容全是 ASCII 数字所以没事，一旦写中文就会踩编码坑（对比 test10 里注释掉的 GB2312 那行）。",
        "表里的 '1' 是字符串不是数字：join 只能拼字符串，写 1 会 TypeError。",
        "本文件没有任何 print，所以「运行输出」是空的 —— 它的产物是 demo.csv 文件本身。",
    ],
    "pitfall": "join 的参数必须是「字符串的序列」，混了 int 会报 TypeError: sequence item 0: expected str instance, int found；写 CSV 时要么保证全 str，要么 map(str, row)。",
}

new['ch11/test1.py'] = {
    "title": "os 模块：mkdir 建目录 + listdir 列内容（新版补上了 mkdir）",
    "notes": [
        "新版在 `path=r'd:\\test'` 后面加了一行 `os.mkdir(path)`，先建目录再 listdir，才不会一上来就报「路径不存在」。",
        "三次输出依次是：当前工作目录、`[]`（刚建好的空目录）、`['example3']`（又建了 example3 之后）。",
        "本站跑这段时把 `d:\\test` 换成了临时目录里的 dtest（跑完即删），否则会在你的 D 盘根目录真的建出两个文件夹 —— 代码逻辑和输出形态不变。",
        "`os.mkdir` 只能建一级目录，父目录不存在抛 FileNotFoundError；要连父目录一起建用 `os.makedirs(path, exist_ok=True)`。",
        "目录已存在时 mkdir 抛 FileExistsError —— 这也是它比 makedirs 更容易踩坑的地方。",
    ],
    "pitfall": "mkdir 建一级、makedirs 建多级；已存在都会报错（makedirs 加 exist_ok=True 可忽略）。删空目录用 os.rmdir，删非空目录得 shutil.rmtree。",
}

new['ch11/test6.py'] = {
    "title": "calendar：setfirstweekday(6) 让一周从周日开始",
    "notes": [
        "`calendar.firstweekday()` 默认返回 0（周一），所以第一行打印 0。",
        "`setfirstweekday(6)` 把「每周第一天」改成周日（0=周一 … 6=周日），再读回来就打印 6。",
        "`calendar.isleap(2022)` 是 False —— 2022 不是闰年。",
        "`calendar.month(2026, 11, w=2, l=1)` 打印 2026 年 11 月的月历文本：w=2 是日期列宽，l=1 是每周占的行数。",
        "因为前面把周首日改成了周日，表头变成 `Su Mo Tu We Th Fr Sa`，11 月 1 日落在周日那一列（第一行最右）。",
        "老师这版把 setfirstweekday(0) 改成 6、月份从 2026-05 换成 2026-11，正好让「周首日影响排版」一眼可见。",
    ],
    "pitfall": "setfirstweekday 改的是全局状态，会影响后面所有 calendar 调用；想恢复就再 setfirstweekday(0)。month() 返回字符串，print 出来才有图形。",
}

new['ch11/test7-1.py'] = {
    "title": "新增文件：HTMLCalendar 生成 HTML 版月历",
    "notes": [
        "老师新加的文件：`HTMLCalendar().formatmonth(2026, 11)` 返回一段 HTML 表格字符串，不是终端里的字符画月历。",
        "输出开头 `<tr><th colspan=\"7\" class=\"month\">November 2026</th></tr>` 是标题行，后面每天一个 `<td>`，class 用星期缩写（mon/tue/…/sun）。",
        "没日期的格子写成 `class=\"noday\"`，所以每行都是整齐 7 列 —— 这正是 HTML 表格比字符画好用的地方。",
        "它的周首日是默认的周一（Mon…Sun），和 test6 里 setfirstweekday(6) 之后的效果正好相反，两个对比着看很直观。",
        "这段输出可以直接粘进 .html 文件当网页月历，浏览器打开就能看。",
    ],
    "pitfall": "formatmonth 返回的是字符串不是打印；想要周日起排得先 calendar.setfirstweekday(calendar.SUNDAY)，这个全局设置同样会影响 test6 的输出。",
}

new['ch11/test8.py'] = {
    "title": "random.seed(10)：种子一变，整串随机结果全变",
    "notes": [
        "`random.seed(10)` 固定种子后，每次运行得到的序列完全相同：0.5714025946899135、7、3.1750152005686805、剪刀、27、['l','k','r','f','a']、[6,7,5,1,3]。",
        "老师这版把 seed(100) 改成 seed(10)，所以这些值和你旧笔记里的不一样 —— 种子一换，后面每一项都跟着变。",
        "不写 seed 时用系统时间当种子，每次运行结果都不同（也就是不可复现）。",
        "同一个种子 + 同样的调用顺序 = 完全可复现，这就是机器学习里「固定随机性」的标准做法。",
    ],
    "pitfall": "只要中间多插一句 random 调用，后面所有值都会整体错位。复现实验时除了固定种子，调用顺序也得固定。",
}

new['ch11/test9.py'] = {
    "title": "多进程：老师把 time.sleep(2) 的注释去掉了，父子进程交替打印",
    "notes": [
        "新版唯一的改动是把 `#time.sleep(2)` 的 # 去掉，于是子进程每轮真的停 2 秒 —— 这才看得出父子交替。",
        "主进程循环 3 次、子进程循环 5 次，都 sleep(2)，所以时间戳两秒一跳，父进程 3 行、子进程 5 行，pid 明显是两个不同的值。",
        "父进程 3 次打印完就结束，子进程还在后台把剩下的 2 次跑完（输出里子进程的行比父进程多，时间戳也更靠后）。",
        "`if __name__ == '__main__'` 守卫在 Windows 上是必须的：子进程启动时会重新 import 主模块，没有守卫会无限创建进程。",
        "输出顺序由系统调度决定，所以父/子两组交错顺序每次可能不同，但各行数是确定的。",
    ],
    "pitfall": "多进程输出顺序不确定，别当固定顺序背；能确定的是 pid 有两个、父进程 3 行、子进程 5 行、时间戳间隔 2 秒。",
}

new['ch11/test11.py'] = {
    "title": "多线程：子线程的循环变量从 i 改成 j，避开和主线程重名",
    "notes": [
        "老师这版把子线程的循环变量从 i 改成 j，所以输出里能看到 `j =0`、`j =1` —— 提示父子线程各用各的变量，别同名。",
        "主线程 MainThread 循环 2 次、子线程 Thread-1 循环 2 次，都 sleep(1)，四行时间戳两两一组。",
        "`threading.currentThread()` 在新版 Python 里已弃用（运行时给 DeprecationWarning），等价写法是 `threading.current_thread()`。",
        "子线程名打印成 `Thread-1 (task_thread)`：Python 3.10+ 会带上 target 函数名，排错时更好认。",
        "这里是两个线程各自 sleep + print，没有共享变量写入，所以不存在竞争；真要改全局变量得上 Lock。",
    ],
    "pitfall": "currentThread() 还能用但已过时；线程结束顺序不等于启动顺序，别用 print 的先后判断谁先跑完。",
}

notes.update(new)
with open(P, 'w', encoding='utf-8') as f:
    json.dump(notes, f, ensure_ascii=False, indent=1)
print('notes 总数:', len(notes), '本次更新:', len(new))
