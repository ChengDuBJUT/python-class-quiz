# -*- coding: utf-8 -*-
"""生成 ch4-8 新版代码的自测题（多考察方式）→ tools/source/quiz_extra.json"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "source", "quiz_extra.json")

Q = []


def add(ch, file, kind, code, stem, options, ans, expl, expect_in=None, run=True):
    Q.append(dict(ch=ch, file=file, kind=kind, code=code, stem=stem,
                  options=options, ans=ans, expl=expl, expect_in=expect_in, run=run))


# ======================= 第 4 章 运算符 =======================
add(4, 'test1.py', 'output', """a = 0
b = a and print("1a:", a)
print("1b:", b)
""",
    "【读结果】a = 0 时，b = a and print(...) 的完整输出是？",
    ["1b: 0", "1a: 0 换行 1b: 0", "1b: None", "1b: False"], 0,
    "and 左边为假立即短路，右边的 print 根本不执行，所以没有 “1a:” 这行；b 直接得到操作数 0。",
    "1b: 0")

add(4, 'test1.py', 'output', """a = 0
b = not a and print("2a:", a)
print("2b:", b)
""",
    "【读结果】not 0 得 True，and 必须继续算右边，b 最终是什么？",
    ["None", "True", "0", "2a: 0"], 0,
    "print() 的返回值是 None，所以 b 拿到 None，输出 “2a: 0” 和 “2b: None” 两行。",
    "2b: None")

add(4, 'test1.py', 'concept', """a = 0
b = not a or print("4a:", a)
print("4b:", b)
""",
    "【机制】表达式 not a or print(...) 中，右侧的 print 会不会执行？",
    ["不会执行，or 左边已为 True 直接短路，b 得到 True",
     "会执行，因为没有括号",
     "会执行，or 一定算右边",
     "报语法错误"],
    0,
    "not 0 == True，or 左边为真立即短路并返回左值 True，右侧 print 不执行。",
    "4b: True")

add(4, 'test3.py', 'output', """x = [1, 2, 3]
y = [1, 2, 3]
z = x
print(x is y, x == y, z is x)
""",
    "【读结果】三个判断依次输出的结果是？",
    ["False True True", "True True True", "False False True", "True False True"], 0,
    "x、y 是两个内容相同的不同对象：is 判身份为 False、== 判值相等为 True；z = x 是同一个对象，z is x 为 True。",
    "False True True")

add(4, 'test3.py', 'output', """A = {1, 2, 3, 4, 5}
B = {1, 3, 5, 7, 9, 11}
print(A - B)
print(A ^ B)
""",
    "【读结果】差集 A - B 与对称差 A ^ B 依次是？",
    ["{2, 4} 和 {2, 4, 7, 9, 11}", "{2, 4} 和 {7, 9, 11}",
     "{1, 3, 5} 和 {2, 4, 7, 9, 11}", "{2, 4} 和 {1, 2, 3, 4, 5, 7, 9, 11}"], 0,
    "- 是差集（在 A 不在 B）；^ 是对称差（只属于其中一个集合）。",
    "{2, 4}")

add(4, 'test5.py', 'output', """for i in range(10, 20):
    print(i, end=" ")
""",
    "【读结果】这段循环最后输出的那个数字是？",
    ["19", "20", "18", "10"], 0,
    "range(10, 20) 左闭右开，生成 10~19 共 10 个数，不包含 20。",
    "19")

add(4, 'test4.py', 'output', """x = 8
y = 3
print(x - y if x + y > 10 else x * y)
print(x + y if x > y else (x - y if x + y > 10 else x * y))
""",
    "【读结果】两行输出依次是？",
    ["5 和 11", "24 和 11", "5 和 5", "11 和 5"], 0,
    "第一个：x+y=11>10 成立取 x-y=5；第二个：x>y 成立直接取 x+y=11，后面嵌套不求值。",
    "5\n11")


# ======================= 第 5 章 流程控制 =======================
add(5, 'test1.py', 'output', """day = "3"
match day:
    case "1":
        print("星期一")
    case "3":
        print("星期三")
    case _:
        print("请输入一个有效数字！")
""",
    "【读结果】day = \"3\" 时输出什么？",
    ["星期三", "星期一", "请输入一个有效数字！", "没有输出"], 0,
    "match 按顺序比对字面量，命中 case \"3\" 后执行并退出整个 match；case _ 是兜底分支。",
    "星期三")

add(5, 'test1.py', 'concept', """day = 3
match day:
    case "3":
        print("星期三")
    case _:
        print("其他")
""",
    "【找错】输入用 input() 得到的是字符串，若这里写 day = 3（整数），会输出什么？",
    ["其他", "星期三", "报 TypeError", "没有任何输出"], 0,
    "case \"3\" 是字符串，而 day 是整数 3，类型不同匹配不上，只能落到兜底 case _。",
    "其他")

add(5, 'test2.py', 'output', """score = 0
if score >= 90:
    print("考试优秀")
elif 80 <= score < 90:
    print("考试良好")
elif 60 <= score < 70:
    print("考试及格")
else:
    print("考试不及格")
    print("Good luck to you!")
""",
    "【读结果】score = 0 时输出几行、内容是什么？",
    ["两行：考试不及格 / Good luck to you!", "一行：考试不及格",
     "一行：考试优秀", "什么都不输出"], 0,
    "所有条件都不成立走 else；else 块里有两条语句，靠缩进决定它们都属于 else。",
    "Good luck to you!")

add(5, 'test3.py', 'output', """gender = "女"
height = 165
if gender == "男":
    if height > 170:
        print("高个子男生")
    else:
        print("矮个子男生")
else:
    if height > 170:
        print("高个子女生")
    else:
        print("矮个子女生")
""",
    "【读结果】gender = \"女\"、height = 165 时输出？",
    ["矮个子女生", "高个子女生", "矮个子男生", "高个子男生"], 0,
    "外层 gender == \"男\" 不成立走外层 else，内层 height > 170 不成立，输出矮个子女生。",
    "矮个子女生")

add(5, 'test4.py', 'output', """i = 1
sum = 0
while i <= 10:
    sum = sum + i
    i = i + 1
print(sum)
""",
    "【读结果】循环结束后打印的 sum 是？",
    ["55", "45", "10", "66"], 0,
    "i 从 1 加到 10，sum = 1+2+…+10 = 55；i 变成 11 时条件不成立退出。",
    "55")

add(5, 'test5.py', 'output', """print(range(5))
result = 0
for i in range(101):
    result = result + i
print(result)
""",
    "【读结果】print(range(5)) 与累加结果依次是？",
    ["range(0, 5) 和 5050", "[0, 1, 2, 3, 4] 和 5050",
     "range(0, 5) 和 4950", "0 1 2 3 4 和 5050"], 0,
    "range 对象直接打印显示为 range(0, 5)；range(101) 生成 0~100，累加得 5050。",
    "range(0, 5)")

add(5, 'test5.py', 'concept', """result = 0
for i in range(101):
    result = result + i
print(result)
""",
    "【机制】range(101) 一共生成多少个数？",
    ["101 个（0 到 100）", "100 个（1 到 100）", "101 个（1 到 101）", "100 个（0 到 99）"], 0,
    "range(n) 从 0 开始、到 n-1 结束，共 n 个数；这里 n=101，所以是 0~100 共 101 个。",
    "5050")

add(5, 'test6.py', 'output', """my_dict = {'python 教程': 'http://a', 'java 教程': 'http://b'}
for ele in my_dict:
    print(ele)
""",
    "【读结果】for ele in my_dict 时 ele 得到的是什么？",
    ["字典的键（如 python 教程）", "字典的值（如 http://a）",
     "键值对组成的元组", "会抛异常"],
    0,
    "直接遍历字典拿到的是键；要取值必须写 my_dict[ele]，要键值对用 my_dict.items()。",
    "python 教程")

add(5, 'test7.py', 'output', """j = 3
i = 1
while i <= j:
    print(f'{i}*{j}={j*i}', end='\\t')
    i += 1
print()
""",
    "【读结果】这一段（j=3）会打印几个式子？",
    ["3 个，写在同一行（用制表符分隔）", "3 个，各占一行", "1 个", "9 个"], 0,
    "内层 i 从 1 到 3 共 3 次；end='\\t' 让它们不换行、用制表符隔开，最后的 print() 才换行。",
    "3*3=9")

add(5, 'test9.py', 'concept', """for j in range(3):
    for i in range(6):
        if i == 4:
            continue
        print("j:", j, "i:", i)
    if j == 0:
        break
""",
    "【机制】为什么输出里没有 i: 4，而且只有 j: 0 这一轮？",
    ["i==4 时 continue 跳过本轮剩余语句；内层跑完后 j==0 触发外层 break",
     "i==4 时 break 结束了全部循环",
     "range(6) 里没有 4",
     "嵌套循环不能使用 continue"],
    0,
    "continue 只跳过内层当前这一轮（所以缺 i: 4）；内层 6 轮结束后外层判断 j==0 成立，break 跳出外层。",
    "j: 0")


# ======================= 第 6 章 组合数据类型 =======================
add(6, 'test13.py', 'output', """tp = (i*2 for i in range(1, 10) if i%2 == 0)
print(tuple(tp))
print(list(tp))
""",
    "【读结果】两次展开生成器，第二行输出什么？",
    ["[]", "(4, 8, 12, 16)", "重复输出 (4, 8, 12, 16)", "抛出 StopIteration"], 0,
    "tuple(tp) 已经把生成器取空，再 list(tp) 只能得到空列表——生成器只能遍历一次。",
    "[]")

add(6, 'test18.py', 'output', """l1 = [1, 2, 3]
l2 = [10, 20, 30]
it = zip(l1, l2)
dc3 = {k*2: v*2 for k, v in it}
dc4 = {k*2: v*2 for k, v in it}
print(dc3)
print(dc4)
""",
    "【读结果】dc4 为什么是空字典 {}？",
    ["zip 返回的迭代器已被 dc3 的推导式取完", "字典推导式不能连续使用",
     "l1 和 l2 长度不同", "dc4 的键重复被去重了"],
    0,
    "zip 在 Python 3 返回一次性迭代器，第一次推导已耗尽，第二次自然得到空字典。",
    "{}")

add(6, 'test21.py', 'output', """dc = {'语文': 90}
dc1 = dc
dc2 = dc.copy()
dc.update({'美术': 90})
print(dc1)
print(dc2)
""",
    "【读结果】dc1 与 dc2 分别输出什么？",
    ["dc1 含美术，dc2 不含美术", "两者都不含美术", "两者都含美术", "dc1 不含，dc2 含"], 0,
    "dc1 = dc 只是起别名，指向同一个字典；dc2 = dc.copy() 是独立副本，不受后续修改影响。",
    "{'语文': 90}")

add(6, 'test11.py', 'output', """ls1 = [1, 2, 3]
ls2 = [3, 4, 5]
ls4 = [x+y for x in ls1 if x%2 == 0 for y in ls2 if y <= 4]
print(ls4)
""",
    "【读结果】这个带条件的多重推导式结果是？",
    ["[5, 6]", "[4, 5, 6]", "[5]", "[4, 6, 8]"], 0,
    "x 只取偶数 2；y 取 3、4（5 被 y<=4 过滤）；相加得 5 和 6。",
    "[5, 6]")

add(6, 'test16.py', 'concept', """st = {1, 2, 3}
st.discard(99)
print(st)
""",
    "【机制】discard 一个不存在的元素会怎样？",
    ["集合保持不变，正常输出 {1, 2, 3}", "抛出 KeyError", "抛出 TypeError", "集合被清空"], 0,
    "discard 删除不存在的元素不报错；换成 remove(99) 就会抛 KeyError——这是两者的关键区别。",
    "{1, 2, 3}")

add(6, 'test17.py', 'fix', """st = {1, 2, 3}
st.add((4, 5))
st.add([6, 7])
""",
    "【找错】第二句 st.add([6, 7]) 会报什么错？",
    ["TypeError: unhashable type: 'list'", "正常运行，得到 {1,2,3,(4,5),[6,7]}",
     "KeyError: 6", "AttributeError: 'set' object has no attribute 'add'"],
    0,
    "集合元素必须可哈希（不可变）；元组可哈希能加入，列表可变不可哈希，加入时报 TypeError。",
    run=False)

add(6, 'test1.py', 'output', """tp = (10, 25, 16, 8, 32)
print(sorted(tp))
print(list(reversed(tp)))
""",
    "【读结果】sorted 与 list(reversed(...)) 的结果依次是？",
    ["[8, 10, 16, 25, 32] 和 [32, 8, 16, 25, 10]", "[8, 10, 16, 25, 32] 和 [8, 10, 16, 25, 32]",
     "(8, 10, 16, 25, 32) 和 [32, 8, 16, 25, 10]", "[32, 8, 16, 25, 10] 和 [8, 10, 16, 25, 32]"], 0,
    "sorted 返回排好序的新列表；reversed 返回反向迭代器，需 list() 展开才能看到元素。",
    "[8, 10, 16, 25, 32]")

add(6, 'test12.py', 'output', """ls = [1, 2, 3]
ls.append([4, 5])
ls.extend([6, 7])
print(ls)
""",
    "【读结果】append 之后再 extend，列表变成？",
    ["[1, 2, 3, [4, 5], 6, 7]", "[1, 2, 3, 4, 5, 6, 7]", "[1, 2, 3, [4, 5, [6, 7]]]", "[1, 2, 3, 6, 7]"], 0,
    "append 把 [4,5] 整个当成一个元素塞进去；extend 才把 6、7 逐个追加。",
    "[1, 2, 3, [4, 5], 6, 7]")


# ======================= 第 7 章 函数 =======================
add(7, 'test10.py', 'output', """def test1(a, b, c=33, *args, **kwargs):
    print(a, b, c, args, kwargs)

test1(1, 2, 3, 4, 6, e=6)
""",
    "【读结果】混合参数传递后，args 与 kwargs 分别是什么？",
    ["args=(4, 6)，kwargs={'e': 6}", "args=(4,)，kwargs={'e': 6}",
     "args=(3, 4, 6)，kwargs={}", "args=()，kwargs={'e': 6}"],
    0,
    "a=1、b=2、c=3 按位置填满，多出来的 4 和 6 都进 *args；e=6 是关键字参数进 **kwargs。",
    "(4, 6) {'e': 6}")

add(7, 'test5.py', 'output', """def add(x, y, z):
    return x+y, z-y, "python"

x, y, z = add(10, 20, 30)
print(x, y, z)
""",
    "【读结果】return 了三个值并用三个变量接收，输出是？",
    ["30 10 python", "30 20 python", "10 30 python", "TypeError: too many values to unpack"], 0,
    "return x+y, z-y, \"python\" 返回元组 (30,10,'python')，序列解包依次赋给 x、y、z。",
    "30 10 python")

add(7, 'test15.py', 'output', """def gen(n):
    print("开始执行")
    i = 0
    while i < n:
        yield i
        i += 1

g = gen(2)
print("创建完毕")
print(next(g))
""",
    "【机制】这段代码的输出顺序说明什么？",
    ["先“创建完毕”，再“开始执行”，最后 0：生成器函数体在首次取值时才运行",
     "先“开始执行”，再“创建完毕”，最后 0",
     "两行内容都不会输出",
     "调用 gen(2) 时函数体已经跑完"],
    0,
    "调用生成器函数只是造出生成器对象，函数体一行都不执行；第一次 next() 才真正开始运行并停在 yield。",
    "创建完毕")

add(7, 'test16.py', 'fix', """def gen(n):
    i = 0
    while i < n:
        yield i
        i += 1

g = gen(2)
print(next(g), next(g))
print(next(g))
""",
    "【找错】生成器只产 2 个值，第三次 next(g) 会怎样？",
    ["抛出 StopIteration 异常", "输出 2", "输出 0 并重新开始", "陷入死循环"], 0,
    "生成器 yield 完 n 个值就结束，再多取一次必抛 StopIteration；应改用 for 遍历或 try-except。",
    run=False)

add(7, 'test20.py', 'output', """ls = [1, 2, 3, 4, 5]
res = map(lambda x: x*x, ls)
print(next(res))
print([i for i in res])
""",
    "【读结果】map 对象先被 next 取走一个元素，剩下的是什么？",
    ["[4, 9, 16, 25]", "[1, 4, 9, 16, 25]", "[1]", "[]"], 0,
    "map 返回一次性迭代器；next(res) 已取走 1，剩余 4、9、16、25。",
    "[4, 9, 16, 25]")

add(7, 'test17.py', 'concept', """def wrapper(fun):
    print("装饰中")
    def inner():
        print("验证")
        fun()
    return inner

@wrapper
def test():
    print("test")

print("---")
test()
""",
    "【机制】“装饰中”这三个字在什么时候打印？",
    ["定义 test 时（即 @wrapper 生效那一刻）", "调用 test() 时", "import 该模块时", "永远不会打印"], 0,
    "@wrapper 等价于 test = wrapper(test)，装饰发生在函数定义时，所以先打印“装饰中”，再打印“---”，最后才执行 inner。",
    "装饰中")

add(7, 'test12.py', 'output', """n = 10
def outer():
    n = 1
    def inner():
        n = 2
        print(n)
    inner()
    print(n)
outer()
""",
    "【读结果】inner 里的 print 与 outer 里的 print 分别输出？",
    ["2 和 1", "2 和 2", "10 和 10", "1 和 2"], 0,
    "inner 里的 n = 2 创建了新的局部变量（没有 nonlocal），不影响 outer 的 n=1。",
    "2\n1")

add(7, 'test11.py', 'concept', """number = 10
def test():
    print(number)
test()
""",
    "【机制】函数内只读取 number、没有赋值，为什么能拿到 10？",
    ["沿 LEGB 规则向外查找，找到了全局变量 number",
     "因为 number 是内置变量",
     "因为用了 global 声明",
     "会报 NameError"],
    0,
    "函数内只读不写时，Python 依次查局部→闭包→全局→内置命名空间，找到全局的 number=10。",
    "10")


# ======================= 第 8 章 类与对象 =======================
add(8, 'test2.py', 'output', """class Car:
    color = "red"

car = Car()
Car.color = "white"
car.color = "black"
print(Car.color, car.color)
""",
    "【读结果】最后一行输出什么？",
    ["white black", "black black", "white white", "red black"], 0,
    "Car.color='white' 改类属性；car.color='black' 给实例新建了同名实例属性，从此实例属性优先，类属性仍是 white。",
    "white black")

add(8, 'test3.py', 'fix', """class Car:
    def drive(self):
        self.color = "white"

car = Car()
car.drive()
print(Car.color)
""",
    "【找错】最后一行 print(Car.color) 会怎样？",
    ["抛 AttributeError：类对象 Car 上没有 color 属性",
     "输出 white", "输出 None", "输出 red"],
    0,
    "self.color='white' 只给实例加了属性，类上并没有 color，所以用类名访问会报 AttributeError。",
    run=False)

add(8, 'test6.py', 'concept', """class Car:
    color = "black"
    @classmethod
    def stop1(cls):
        cls.color = "red"

car = Car()
car.stop1()
print(Car.color)
""",
    "【机制】类方法里 cls.color = \"red\" 改的是谁？",
    ["类属性，所以 Car.color 也变成 red", "只是 car 这个实例的属性",
     "两个都改", "改不了，会报错"],
    0,
    "cls 代表类本身，cls.属性 = 值 改的是类属性，对所有没有自己同名实例属性的对象都生效。",
    "red")

add(8, 'test7.py', 'fix', """class Car:
    color = "black"
    @staticmethod
    def test():
        print(self.color)
""",
    "【找错】静态方法里写 self.color 会发生什么？",
    ["报 NameError：静态方法没有 self 参数", "正常输出 black",
     "输出 None", "自动把实例传进来"],
    0,
    "静态方法既没有 self 也没有 cls，方法体里根本没有 self 这个名字；要访问类属性得写 Car.color。",
    run=False)

add(8, 'test9.py', 'output', """class Person:
    def __init__(self):
        self.__age = 18
    @property
    def age(self):
        return self.__age
    @age.setter
    def age(self, v):
        self.__age = v + 1

p = Person()
p.age = 25
print(p.age)
""",
    "【读结果】赋值 p.age = 25 之后再读取，输出是？",
    ["26", "25", "18", "AttributeError"], 0,
    "setter 里写的是 self.__age = v + 1，所以实际存进去是 26；@property 让 age 可以像属性一样读写。",
    "26")

add(8, 'test11.py', 'fix', """class Car:
    def __init__(self):
        self.color = "blue"
    def __del__(self):
        print("销毁")

car = Car()
del car
print(car.color)
""",
    "【找错】del car 之后再访问 car.color 会怎样？",
    ["NameError：car 这个名字已经不存在了，同时对象被回收会打印“销毁”",
     "输出 blue", "输出 None", "抛 AttributeError"],
    0,
    "del 删除的是变量名（引用）；对象没有引用后被回收并触发 __del__，之后再使用 car 这个名字就是 NameError。",
    run=False)

add(8, 'test17.py', 'output', """class A:
    def show(self):
        print("A.show()")
class B(A):
    pass
class C(A):
    def show(self):
        print("C.show()")
class D(B, C):
    pass
D().show()
""",
    "【读结果】D().show() 输出什么？",
    ["C.show()", "A.show()", "B.show()", "抛 AttributeError"], 0,
    "MRO 顺序是 D → B → C → A，B 没有定义 show，于是取 C 的 show()。",
    "C.show()")

add(8, 'test24.py', 'output', """class House:
    def play(self):
        print("House play!")
class Car:
    def play(self):
        print("Car play!")
class TouringCar(House, Car):
    pass

TouringCar().play()
""",
    "【读结果】两个父类都有 play，子类这样写会执行哪一个？",
    ["House play!（父类列表中写在前面的优先）", "Car play!",
     "两个都执行", "报错：方法冲突"],
    0,
    "多继承按 MRO 顺序查找同名成员，House 在 Car 前面，所以先找到 House.play()。",
    "House play!")

add(8, 'test23.py', 'fix', """class Dog:
    def __init__(self):
        self.__age = 18
class WolfDog(Dog):
    pass

w = WolfDog()
print(w.__age)
""",
    "【找错】子类实例访问父类的私有属性会怎样？",
    ["AttributeError：子类不继承父类的私有成员", "输出 18", "输出 None", "输出 0"], 0,
    "私有属性名被改写为 _Dog__age，子类实例上只有 _WolfDog__* 的改写形式，所以访问不到。",
    run=False)

add(8, 'test26.py', 'concept', """class Cat:
    def shout(self):
        print("喵喵喵...")
class Dog:
    def shout(self):
        print("汪汪汪...")

def f(obj):
    obj.shout()

f(Cat())
f(Dog())
""",
    "【机制】函数 f 不关心传进来的是什么类型，这体现了什么？",
    ["多态（鸭子类型）：只要对象有 shout 方法就能被调用",
     "继承：Cat 和 Dog 必须继承同一个父类",
     "封装：把方法藏起来",
     "重载：同名函数定义两次"],
    0,
    "Cat 与 Dog 没有继承关系，但都实现了 shout；f 只依赖“有这个方法”，这就是 Python 的多态。",
    "喵喵喵...")

add(8, 'test12.py', 'concept', """class Demo:
    def __new__(cls, *args, **kwargs):
        print("__new__ 执行")
        return super().__new__(cls)
    def __init__(self):
        print("__init__ 执行")

Demo()
""",
    "【机制】实例化 Demo() 时两个方法的执行顺序是？",
    ["先 __new__ 后 __init__", "先 __init__ 后 __new__",
     "只执行 __init__", "只执行 __new__"],
    0,
    "__new__ 负责创建并返回实例，只有它返回了对象，__init__ 才会被调用来初始化。",
    "__new__ 执行")

add(8, 'test5.py', 'concept', """class Car:
    __color = "white"
    _wheels = 4

    def testColor(self):
        print(self.__color)

car = Car()
car.testColor()
print(car._wheels)
""",
    "【机制】为什么 car.__color 在类外访问不到，而 car._wheels 可以？",
    ["双下划线触发了名称改写（_Car__color），单下划线只是约定、语法上仍可访问",
     "双下划线表示常量，单下划线表示变量",
     "两者都应该报错",
     "因为 __color 是实例属性"],
    0,
    "私有属性 __color 被改写成 _Car__color，类外用原名访问会失败；单下划线 _wheels 只是“别乱用”的约定。",
    "4")

json.dump(Q, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("quiz_extra:", len(Q), "题")
from collections import Counter
print("按章:", dict(Counter(q["ch"] for q in Q)))
print("按类型:", dict(Counter(q["kind"] for q in Q)))
