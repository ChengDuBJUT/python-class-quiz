# -*- coding: utf-8 -*-
"""合并第 1-3 章代码学习卡到 source/code_notes.json。

注释都对照过 newcode_runs.json 里的真实输出；报错的文件注明是
「故意演示」还是「环境缺库」。中文行文里的引号统一用「」，避免和外层字符串冲突。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(BASE, "source", "code_notes.json")

N = {}

# ============ 第 1 章 ============
N["ch1/test0.py"] = {
    "title": "赋值语句不产生输出，只有 print 才有",
    "notes": [
        'hello = "hello, python!" 只是把字符串绑定到名字 hello，整个程序不会有任何输出。',
        '真正打印的是下一行 print("hello, python!")——它打的是字面量，不是变量 hello。',
        '变量定义了却没用，Python 不报错也不提示；只有 pylint/flake8 这类静态检查才会警告 unused variable。',
    ],
    "pitfall": "最容易答成「输出两行」——赋值不算输出。",
}

N["ch1/test1.py"] = {
    "title": "import 的三种写法、math 与 numpy 的 pi，以及被导入模块的顶层代码会执行",
    "notes": [
        'import numpy as np 起别名，之后用 np.pi；import math 直接用 math.pi，两者都是 3.141592653589793。',
        'x = np.array([1,2,3]) 后 x[0] 是 1；print(x) 打印成 [1 2 3]（没有逗号），这是 numpy 数组的显示格式，和列表不同。',
        'from test0 import hello as hhh 把 test0 里的变量 hello 直接绑成 hhh；导入的一瞬间 test0 的顶层代码也会执行，所以 hello, python! 又多打印一次。',
        'abs(-20) 是内置函数，不用导入就能用。',
    ],
    "pitfall": '数 hello, python! 出现几次：本文件 print 一次 + import test0 时执行它自己的 print 一次 = 2 次（不是 3 次）。',
}

N["ch1/test2.py"] = {
    "title": "中文标识符、类属性与实例属性（self.颜色 = 白色 之后到底变了什么）",
    "notes": [
        '类体里 颜色 = "黑色"、腿数 = 4 是类属性，所有实例共享；小海 = 海龟() 之后 print(小海.颜色) 输出 黑色。',
        '变色() 里 self.颜色 = "白色" 不是修改类属性，而是给这个实例新建一个同名实例属性；所以后面 显色() 输出 白色。',
        '方法定义在类里要带 self 形参，调用时不用传（小海.前进()）。',
        '海龟.颜色 仍然是 黑色——实例属性只影响那一个对象，不会回写类属性。',
    ],
    "pitfall": "问「类属性 海龟.颜色 现在是什么」，答案是 黑色，别被最后打印的 白色 带跑。",
}

N["ch1/test3.py"] = {
    "title": "turtle 窗口：setup 设窗口大小，screensize 设画布大小",
    "notes": [
        'turtle.setup(200,100,100,100) 四个参数是 宽、高、左上角 x、左上角 y（后两个可省略）。',
        'turtle.screensize(400,200,"green") 设的是画布（可滚动区域）大小和底色，和窗口大小是两件事。',
        'turtle.done() 让窗口保持不关闭，程序停在这里等用户关窗口。',
        '这个文件没有 print，所以运行结果是一块 200×100、底色 green 的窗口，控制台没有任何输出。',
    ],
    "pitfall": "setup 的第三、四个参数是窗口位置的 x/y，不是画布宽高，别和 screensize 混。",
}

N["ch1/test4.py"] = {
    "title": "import turtle as pen：绘图前先把画笔设好（形状/粗细/颜色/速度）",
    "notes": [
        'as pen 只是别名，等价于 import turtle 之后写 turtle.xxx。',
        '顺序很关键：先 width(10)/color("green")/speed(5) 再 forward(100)，否则画出来是默认的黑色细线。',
        'shape("turtle") 改的是画笔图标（显示成海龟），不影响线条本身。',
        'forward(100) 沿当前朝向（默认朝右，即 0 度）前进 100 像素。',
    ],
    "pitfall": "speed(5) 既不是画 5 条线也不是速度 5 像素每秒，只是动画快慢（0 最快、1 最慢）。",
}

N["ch1/test5.py"] = {
    "title": "相对运动 forward/backward/left/right 与绝对转向 setheading",
    "notes": [
        'left(45)/right(45) 是相对当前朝向转；setheading(45) 是直接把朝向设成 45 度，不管之前朝哪。',
        'backward(50) 是倒退，方向与当前朝向相反。',
        'goto(-100,-100) 是绝对移动，会从当前位置画一条线过去（除非先 penup）。',
        '同样一串指令，把 setheading(45) 换成 left(45)，画出的折线形状完全不同——这是最爱考的对比点。',
    ],
    "pitfall": "right(45) 后再 left(45) 等于回到原朝向；但 setheading(45) 永远指向 45 度。",
}

N["ch1/test6.py"] = {
    "title": "circle 的半径/角度、steps 画正多边形、begin_fill 与 end_fill 填充",
    "notes": [
        'circle(90,60) 画半径 90、圆心在左侧的 60 度圆弧；半径取负 circle(-90,60) 圆心在右侧（弧往另一边弯）；角度取负表示顺时针画。',
        'home() 回到原点 (0,0) 并把朝向恢复成 0 度。',
        'circle(50, steps=6) 画的不是圆弧，而是外接圆半径 50 的正 6 边形。',
        '填充要 begin_fill() 和 end_fill() 成对出现，且 fillcolor("red") 必须在 begin_fill 之前设。',
    ],
    "pitfall": "circle(50) 只给一个参数时画的是整圆（360 度）；只有传了 steps 才变成多边形。",
}

# ============ 第 2 章 ============
N["ch2/test.py"] = {
    "title": "导入自定义模块、hex() 进制转换，以及函数里 print 与 return 的先后",
    "notes": [
        'import test3 会执行 test3.py 的顶层代码；test3 里只有函数定义，所以这一刻什么都不打印。',
        'test3.add(2,3) 内部先执行 print(locals())，此时 z 已算出 5，所以打印 {x:2, y:3, z:5}，然后 return 5 交给外层 print。',
        '所以输出顺序是 locals() 在前、5 在后——return 的值要等外层 print 才显示。',
        'hex(10) 把十进制转成十六进制字符串，输出 0xa（带 0x 前缀、小写）。',
    ],
    "pitfall": "locals() 在函数内部调用返回的是当前函数的局部变量表，在模块顶层调用返回的才是全局名字表。",
}

N["ch2/test1.py"] = {
    "title": "三引号是字符串不是注释；列表可以跨行书写",
    "notes": [
        '开头三引号里那一整段 if/else 是字符串字面量，不会执行，所以没有任何 True/False 输出。',
        "列表的方括号里允许换行，Python 会自动接续，打印结果合并成一行 ['a', 'b', 'c', 'd', 'e']。",
        '列表打印带引号和逗号；如果是 numpy 数组则不带（对比第 1 章 test1.py）。',
    ],
    "pitfall": "三引号只是没被赋值的字符串（docstring），技术上不是注释；真正不执行的是 # 注释。",
}

N["ch2/test2.py"] = {
    "title": "keyword.kwlist：关键字清单与数量，不能拿来当变量名",
    "notes": [
        'keyword.kwlist 是当前 Python 版本的全部关键字列表，这里输出 35 个。',
        'True / False / None 首字母大写，也是关键字，所以写 true、false、null 会 NameError。',
        'len() 取元素个数，输出 35——换 Python 版本数量可能不同，答题以本机实测为准。',
        '关键字不能作标识符，但可以出现在字符串和字典键里。',
    ],
    "pitfall": "and / or / not / is / in 都在列表里；print、input 这类内置函数不在——它们是内置函数不是关键字。",
}

N["ch2/test3.py"] = {
    "title": "函数定义本身不执行；locals() 只有被调用时才看得到局部变量",
    "notes": [
        '这个文件只有 def add(x,y) 的定义和一行被注释掉的调用，直接运行没有任何输出。',
        '函数体里的 print(locals()) 要等 add 被调用才执行（在 ch2/test.py 里就能看到效果）。',
        'return z 把结果交回调用者，函数自己不会打印结果。',
    ],
    "pitfall": "问「运行这个文件输出什么」，答案是什么都没有——别把函数体里的 print 当成会执行。",
}

N["ch2/test4.py"] = {
    "title": "capitalize / title / upper 三个大小写方法的区别",
    "notes": [
        'capitalize() 只把第一个字符变大写、其余全部变小写：Ahu learning python。',
        'title() 每个单词首字母大写：Ahu Learning Python。',
        'upper() 全部变大写：AHU LEARNING PYTHON。',
        '三个方法都返回新字符串，原变量 sr 不变（字符串不可变）。',
    ],
    "pitfall": "capitalize 会把其余字母都变小写，不只是把首字母变大写；给 AHU 开头的串要特别注意。",
}

N["ch2/test5.py"] = {
    "title": "继承：子类自动拥有父类的属性和方法",
    "notes": [
        'class BigDog(Dog) 继承 Dog；bDog.say() 用的是父类方法，bDog.color 拿到父类类属性 White。',
        'bDog.size 是子类自己加的类属性 big。',
        'dog.say() 内部先 print 再 return，所以 wang,wang,wang.... 会出现两次：一次在 res=dog.say()，一次在 f-string 里调用 bDog.say()。',
        'f-string 里的 {bDog.say()} 会真的调用方法，它打印的内容先出现，返回值 Hello 再被拼进字符串。',
    ],
    "pitfall": "f-string 里写函数调用会执行函数——这是数输出行数最容易漏的地方。",
}

N["ch2/test6.py"] = {
    "title": "type() 动态建类，以及 __name__ 的取值",
    "notes": [
        'type("Dog", (object,), dict(...)) 三个参数是 类名、父类元组、属性字典，等价于用 class 语句定义。',
        'dict 里放的是函数对象，挂到类上就成为方法，第一个参数仍然是 self。',
        'print(__name__)：直接运行输出 __main__；被别的模块 import 时输出的是模块名（ch2/test7.py 里能看到 test.__name__ 是 test）。',
        '输出顺序：__main__ → say 的 print → bark 的 print → white → Hello → bark → small。',
    ],
    "pitfall": "res1 = dog.say() 里 say 先打印再返回，所以 wang,wang,wang 出现在 white 之前，不是之后。",
}

N["ch2/test7.py"] = {
    "title": "if __name__ == '__main__'：被 import 时不会执行的那一段",
    "notes": [
        "直接运行 test7.py 时 __name__ 是 __main__，所以打印 demo.py 是主模块执行。",
        'import test 会执行 test.py 的顶层代码，于是 test.py 里 import test3、print(hex(10))、numpy 那几行全部执行，输出混进来。',
        'test.__name__ 是 test（模块名），当前文件自己的 __name__ 仍是 __main__。',
        "这就是库里为什么要包 if __name__ == '__main__':——被导入时那段不执行。",
    ],
    "pitfall": "本文件自己的「主模块执行」那句话，在 import 场景下不会出现；直接运行时才出现。",
}

N["ch2/test8.py"] = {
    "title": "文件写入三步：open('w') → write → close",
    "notes": [
        "open(test.txt, 'w') 以写模式打开：文件不存在就创建，已存在会清空。",
        "write() 不会自动换行，所以每句都手写了 \\n。",
        "不 close() 可能内容还在缓冲区没落盘；更安全的写法是 with open(...) as f:。",
        "该程序没有任何控制台输出，结果体现在 test.txt 里有三行——题目若问输出什么，要答「无输出」。",
    ],
    "pitfall": "'w' 是覆盖不是追加，追加要用 'a'；常考的变体是第二次运行后文件里有几行。",
}

# ============ 第 3 章 ============
N["ch3/test0.py"] = {
    "title": "混合类型列表的索引、切片与 type()",
    "notes": [
        'aList = ["python", 1, [2,3,4], 3.0, "计算机"]：一个列表里可以混放不同类型。',
        "aList[0:3] 取下标 0、1、2（切片左闭右开）：['python', 1, [2, 3, 4]]。",
        "aList[2][0] 先取第 3 个元素（内层列表），再取它的第 1 个，结果是 2。",
        "type([...]) 输出 <class 'list'>。",
    ],
    "pitfall": "aList[2] 是整个 [2, 3, 4]；aList[2][0] 才是 2，别把两者看成一回事。",
}

N["ch3/test1.py"] = {
    "title": "引号嵌套、转义字符与原始字符串 r''",
    "notes": [
        "字符串里有单引号就用双引号包，有双引号就用单引号包，可以省掉转义。",
        "单引号、双引号、反斜杠、\\n（换行）、\\r（回车）都是转义序列，print 时才生效。",
        'r"..." 或 R"..." 是原始字符串，里面的 \\n \\r 按两个普通字符处理，不再转义。',
        "最后两行对比：print 一串 \\n 会打出一堆空行，而 print(r...) 原样打出 \\n\\n...\\r。",
        "f-string：f\"My name is {name}\" 把变量值填进去。",
    ],
    "pitfall": "r 只影响转义，不改变引号规则；原始字符串也不能以单个反斜杠结尾。",
}

N["ch3/test2.py"] = {
    "title": "字符串索引（正/负）与切片",
    "notes": [
        "s1[2] 取第 3 个字符（下标从 0 开始）。",
        "s1[2:5] 取下标 2、3、4 三个字符，不含 5。",
        "负索引从末尾数：s2[-2] 是倒数第 2 个字符。",
        "s2[-3:-1] 从倒数第 3 个取到倒数第 2 个（不含 -1 那个位置本身）。",
    ],
    "pitfall": "切片终点永远不含；写 s2[-3:-1] 会漏掉最后一个字符，要到末尾就用 s2[-3:]。",
}

N["ch3/test3.py"] = {
    "title": "input() 一律返回字符串，要算数必须先转换",
    "notes": [
        'input("提示") 的返回值永远是 str，括号里只是提示语，不会自动换行。',
        "int(input(...)) 把输入字符串转整数，float(...) 转浮点。",
        "喂入 张三 / 18 / 90 时输出：张三 18 90.0（最后一个被 float 转成浮点）。",
        "若直接拿 input() 的返回值加 1，会 TypeError：字符串和整数不能相加。",
    ],
    "pitfall": "输出里三个提示连成一行，是因为管道输入时没有回车回显——不是程序写错了。",
}

N["ch3/test4.py"] = {
    "title": "% 格式化、format() 与 f-string 三种写法（以及 print 到文件）",
    "notes": [
        '"%s %d %f" % 元组 是旧式格式化，%.2f 表示保留两位小数。',
        '"{}".format(...) 按位置填，{0}{1} 指定序号，{name1} 按关键字填。',
        'f-string（f"..."）最简洁，{score:.2f} 可以带格式说明符。',
        "该文件的 print 都写了 file=f，所以屏幕上没有任何输出，内容写进了 1.txt。",
        "顶部的 from ipywidgets import Datetime 只是被 import 了却没用到；没装这个库会直接 ModuleNotFoundError（考试不考这个）。",
    ],
    "pitfall": "print(..., file=f) 不打印到屏幕；题目问屏幕输出时答案是空。",
}

N["ch3/test5.py"] = {
    "title": "bytes 对象：索引得到整数、切片仍是 bytes",
    "notes": [
        "b'Hello,python!' 是 bytes 字面量，每个元素是 0-255 的整数。",
        "by1[1] 得到 101（字符 e 的 ASCII），是 int；by1[0:5] 仍是 bytes，显示为 b'Hello'。",
        "bytes(中国字, encoding='utf-8') 用指定编码把字符串编码成字节，一个汉字通常 3 字节。",
        "by2 是「跟着阿虎学编程。」的 UTF-8 字节：by2[3] 是 231（第二个汉字的起始字节 0xE7），by2[3:5] 得到 b'\\xe7\\x9d'。",
    ],
    "pitfall": "bytes 索引返回 int，不是长度为 1 的 bytes——这是和 str 最大的区别。",
}

N["ch3/test6.py"] = {
    "title": "encode / decode：编码和解码必须用同一种字符集",
    "notes": [
        "bytes(北京工业大学, encoding='utf-8') 得到 UTF-8 字节串，print 出来是 b'\\xe5\\x8c\\x97...' 这种形式。",
        "by.decode('utf-8') 把字节还原成字符串。",
        "st.encode('gbk') 用 GBK 重新编码：同一个汉字 GBK 占 2 字节、UTF-8 占 3 字节，所以 GBK 字节串明显更短。",
        "用 utf-8 编码却用 gbk 解码，会得到乱码或抛 UnicodeDecodeError。",
    ],
    "pitfall": "问哪种编码字节数更多——UTF-8 中文 3 字节一字，GBK 2 字节一字。",
}

N["ch3/test7.py"] = {
    "title": "list() 类型转换：字符串按字符拆，字典只取键",
    "notes": [
        "list(hello) 把字符串按字符拆成 ['h','e','l','l','o']。",
        "元组不可修改（tuple_1[1] = R 会 TypeError），但可以 list(tuple_1) 转成列表再改。",
        "list(dict1) 只拿键；要值用 dict1.values()，要键值对用 dict1.items()。",
        "range(1,6) 左闭右开，list() 后是 [1,2,3,4,5]；list() 无参是空列表 []。",
    ],
    "pitfall": "list(字典) 拿到的是键列表，不是键值对列表。",
}

N["ch3/test8.py"] = {
    "title": "列表的索引、带步长切片与切片赋值",
    "notes": [
        "url = list(阿虎编程，虎虎生风。) 把字符串拆成单字列表：['阿','虎','编','程','，','虎','虎','生','风','。']。",
        "url[1:9:2] 从下标 1 开始每 2 个取一个，到 9（不含）：['虎','程','虎','生']。",
        "url[-6:-1] 用负索引切片，取不到最后一个字符。",
        "url[1]=龙 按下标改一个元素；url[2:4]=练武 用切片一次替换两个元素（长度可以不等，列表会伸缩）。",
        "注释掉的 del url 若执行，后面再 print 就会 NameError。",
    ],
    "pitfall": "切片赋值的右边是字符串时会被当成字符序列逐个填入，容易和替换成一个元素搞混。",
}

N["ch3/test9.py"] = {
    "title": "集合去重与无序，以及 {} 到底是字典还是集合",
    "notes": [
        "{1,'c',1,(1,2,3),'c'} 会自动去重，只剩 3 个元素，且打印顺序不保证。",
        "a = {} 是空字典不是空集合，type(a) 是 dict；空集合只能写 set()。",
        "{3} 有一个元素，是集合；{1,[1,2]} 会 TypeError，因为列表不可哈希。",
        "add() 加元素、discard() 删元素（不存在也不报错），remove() 删不存在的元素会报 KeyError。",
    ],
    "pitfall": "{} 是空字典——这是最高频的陷阱；集合元素的打印顺序也不能背。",
}

N["ch3/test10.py"] = {
    "title": "字典的创建方式、键的要求、keys() 遍历",
    "notes": [
        "dict0['name'] = zhang 是边建边加；scores = {'数学':95} 是字面量创建。",
        "键必须是可哈希的不可变类型：字符串、数字、元组可以，列表不行。",
        "dict([('two',2),('one',1)]) 和 dict(zip(keys, values)) 都能从序列构造字典。",
        "遍历字典默认遍历键；.keys() 拿键、.values() 拿值、.items() 拿键值对。",
        "dict7 = {tuple1: lable} 用整个元组当键，打印时键就是一整个长元组。",
    ],
    "pitfall": "for i in dc8 遍历的是键；键是长元组时打印出来是一长串，别误以为是值。",
}

N["ch3/test11.py"] = {
    "title": "字典的增改删，以及 del 之后再用会 NameError",
    "notes": [
        "dict((['two',90],['one',80],['three',100])) 用列表的列表构造字典，每个内层是一对键值。",
        "dc['four'] = 89：键存在就改值，不存在就新增。",
        "del(dc['four']) 删的是这一对键值；del dc 删的是整个变量名。",
        "del dc 之后再 print(dc) 会 NameError: name 'dc' is not defined——这是本文件唯一报错的地方，属于故意演示。",
    ],
    "pitfall": "del dc['four'] 和 del dc 完全不同：前者删一个元素，后者把变量本身删掉。",
}

N["ch3/test14.py"] = {
    "title": "猜拳游戏：while True + try/except 校验输入",
    "notes": [
        "options = ['剪刀','石头','布']：用下标 0/1/2 对应三种手势。",
        "while True 里先 int(input())；输入不是数字会 ValueError，被 except 捕获提示重输；数字不在 0 到 2 则提示重新输入。",
        "用 [player, computer] in winning_combinations 判断胜负——列表 in 列表是判断是否存在这个子列表。",
        "random.randint(0,2) 让电脑随机出拳，所以每次运行结果可能不同（本次输入 1 出石头，电脑出布，判你输了）。",
    ],
    "pitfall": "结果随机，别背死输出；要能说清 random.randint(0,2) 取的是 0、1、2 三个整数（含两端）。",
}

# ---- 合并 ----
with open(PATH, encoding="utf-8") as f:
    data = json.load(f)

data.update(N)
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

print("merged %d cards, total %d" % (len(N), len(data)))
