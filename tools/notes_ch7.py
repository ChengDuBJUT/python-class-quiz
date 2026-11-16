# -*- coding: utf-8 -*-
"""合并 ch7 学习卡到 code_notes.json"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "source", "code_notes.json")

CH7 = {
"ch7/test1.py": dict(
 title="函数也是对象：type、id、文档字符串",
 notes=[
  """def 定义函数后，函数名 add 本身是一个对象（type 为 <class 'function'>）。""",
  """三引号写在函数体第一行是文档字符串（docstring），可用 add.__doc__ 取出。""",
  """print(type(add)) 说明函数是一等对象，可以赋值、传参、返回。""",
  """if __name__ == '__main__': 下的代码只在“直接运行本文件”时执行，被 import 时不执行。""",
 ]),

"ch7/test2.py": dict(
 title="函数重名覆盖、函数可赋值给变量",
 notes=[
  """同名函数 fun 定义了两次，后一个覆盖前一个，所以 fun(2,3) 返回 'ok'。""",
  """add_object = add_return 把函数对象赋给另一个变量，两者指向同一个函数，id 相同。""",
  """由 from test1 import add 可见：被导入模块的顶层代码不会因 import 而重复执行（有 __main__ 保护）。""",
 ],
 pitfall="""Python 没有函数重载，同名 def 只会保留最后一个；想按参数个数区分必须自己写判断或用默认参数。"""),

"ch7/test3.py": dict(
 title="return 返回值的打印顺序",
 notes=[
  """print(test()) 的执行顺序：先进入函数执行 print(666)，函数 return 888，最后才把 888 打印出来。""",
  """所以输出是 666 在前、888 在后。""",
  """没有写 return 的函数返回 None。""",
 ]),

"ch7/test4.py": dict(
 title="函数返回函数自身",
 notes=[
  """test2 内部先打印 a 1，再把 test2 这个函数对象自己 return 出去。""",
  """b = test2() 时执行一次，b 得到函数对象；之后每次 b() 又会打印一次 a 1 并再返回函数。""",
  """每次调用 a 都重新初始化为 0 再 +1，所以永远打印 a 1（局部变量不跨调用保留）。""",
  """for 循环 5 次，每次都多打印一行 a 1 和一行 b <function ...>。""",
 ],
 pitfall="""局部变量 a 在每次调用时都重新创建，所以不会累加；要累加必须用闭包 nonlocal 或全局变量。"""),

"ch7/test5.py": dict(
 title="return 返回多个值与序列解包",
 notes=[
  """return sum,sub,ss 实际返回的是一个元组 (30,10,'python')。""",
  """x,y,z = add(10,20,30) 用序列解包把元组的三个元素分别赋给三个变量。""",
  """所以 x=30、y=10、z=python。""",
 ]),

"ch7/test6.py": dict(
 title="关键字参数与默认参数",
 notes=[
  """connect(ip=..., port=...) 用关键字参数传参，顺序可以打乱，结果一样。""",
  """文件中 connect 定义了两次，第二个带默认值 port=8080，覆盖了第一个。""",
  """所以 connect('192.168.0.1') 只传了 ip，port 取默认值 8080。""",
 ],
 pitfall="""同一文件里重复 def 同名函数，前面的会被后面覆盖——看到两个 connect 别以为都会生效。"""),

"ch7/test7.py": dict(
 title="*args 把多余位置实参打包成元组",
 notes=[
  """形参写成 *args，调用时传入的所有位置实参被打包成一个元组。""",
  """test(10,20,30) 时 len(args)=3，用 args[i] 逐个取出打印。""",
  """test(11,22,33,44,55) 时 args 有 5 个元素，全部打印。""",
 ]),

"ch7/test8.py": dict(
 title="**kwargs 把关键字实参打包成字典",
 notes=[
  """形参写成 **kwargs，所有带键的实参被打包成字典，type(kwargs) 为 dict。""",
  """遍历 dict.keys() 拿到每个键，再用 dict.get(key) 取对应的值。""",
  """调用 test(x=10,y=20) 输出 x/10、y/20；五个键的调用则输出 10 行。""",
 ]),

"ch7/test9.py": dict(
 title="调用时用 * 解包元组",
 notes=[
  """l1 = (11,22,33,44) 是一个元组，直接 test(l1) 只会传一个参数（会报错，已被注释）。""",
  """test(*l1) 在调用时把元组拆成 4 个位置实参，正好对上 a,b,c,d。""",
  """所以输出 11 22 33 44。""",
 ],
 pitfall="""* 放在形参前是“打包”，放在实参前是“解包”，位置不同含义相反。"""),

"ch7/test10.py": dict(
 title="混合参数传递的分配规则",
 notes=[
  """被三引号包住的第一个示例演示：test(*d1) 解包字典得到的是“键”，test(**d1) 得到的才是键值对。""",
  """def test1(a,b,c=33,*args,**kwargs) 的分配顺序：先按位置填 a、b，再填 c，多余位置实参进 args，关键字实参进 kwargs。""",
  """test1(1,2) → c 取默认值 33，args、kwargs 都为空。""",
  """test1(1,2,3,4) → 4 超出固定形参个数，被 *args 收进元组 (4,)。""",
  """test1(1,2,3,4,6,6,6,6,e=6,d=5) → 中间多余的 6 全进 args，e、d 进 kwargs。""",
  """test1(1,2,3,d=3,e=6) → d、e 是关键字参数直接进 kwargs，不影响位置参数。""",
  """最后的 test111(l1) 传的是列表，函数只打印它，不涉及解包。""",
 ],
 pitfall="""位置参数必须写在关键字参数之前；test1(1, e=6) 会报错，因为 b 没有值。"""),

"ch7/test11.py": dict(
 title="全局变量读取、import 的副作用",
 notes=[
  """函数内只读取 number 时，沿 LEGB 找到全局的 10，所以打印 1 10、3 10。""",
  """被注释掉的 global number / number = 0 说明了：函数内一旦给全局名赋值，就必须先声明 global，否则会变成新的局部变量。""",
  """global 语句被注释掉后，test1 只是读取，全局 number 始终是 10（2、4、5 行都是 10）。""",
  """import test10 会执行 test10 的顶层代码，所以输出里突然多出 test10 那 6 行内容。""",
  """test3 中 test10.l1 = [55,66,77,88] 修改的是模块属性，所以函数外的 test10.l1 也跟着变。""",
 ],
 pitfall="""import 一个模块不只是“引入名字”，模块顶层的语句都会被执行一遍——这是输出里多出内容的原因。"""),

"ch7/test12.py": dict(
 title="nonlocal 与变量作用域",
 notes=[
  """test_in 里写了 number = 1，这会在内层创建新的局部变量，内层打印 1+1=2。""",
  """nonlocal number 被注释掉，所以内层的 number 与外层的 number=10 是两个变量。""",
  """外层 print(number) 仍是 10——内层的赋值没有影响外层。""",
 ],
 pitfall="""想让内层改外层局部变量必须写 nonlocal；想让函数改全局变量必须写 global。"""),

"ch7/test13.py": dict(
 title="递归求阶乘 + lambda 匿名函数",
 notes=[
  """func(num) 用递归实现阶乘：num==1 是终止条件，否则 return num*func(num-1)。""",
  """输入 5 时 5! = 120，按 %d!=%d 的格式输出 5!=120。""",
  """lambda a,b,c: a+b*c 定义了匿名函数，f 保存后可用 f(1,2,3) 调用。""",
  """注意运算优先级：先算 b*c 再加 a，所以 1+2*3 = 7，不是 9。""",
 ],
 pitfall="""lambda 的函数体只能是一个表达式，不能写 if 语句块、循环等复杂结构。"""),

"ch7/test14.py": dict(
 title="闭包计数器与 nonlocal",
 notes=[
  """fun1 内部定义 fun2 并返回它，fun2 引用了外层的 local_val，这就是闭包。""",
  """nonlocal local_val 让 fun2 能修改外层变量，每次调用 +1。""",
  """count = fun1() 创建了一个闭包；之后反复 count() 会在同一个 local_val 上累加，得到 1、2、3、4、5。""",
  """而循环里 print(fun1()) 每次都新建一个闭包对象，所以打印的是函数对象地址而不是数值。""",
 ],
 pitfall="""闭包的状态保存在“那一次 fun1() 调用”的局部变量里；重新调用 fun1() 会得到全新的计数器，从 0 开始。"""),

"ch7/test15.py": dict(
 title="列表推导、生成器表达式与 yield 生成器的执行时机",
 notes=[
  """[x*x for x in range(5)] 立刻算出完整列表 [0,1,4,9,16]。""",
  """(x*x for x in range(5)) 是生成器表达式，for 遍历时才逐个产出。""",
  """gen(n) 用 yield 定义生成器函数，每次 yield 暂停并交出一个值，index 每次 +2。""",
  """关键：print('111111, gen!') 在 for 循环真正开始迭代时才输出，说明生成器函数体不会在调用时立即运行。""",
  """index 从 0 开始每次加 2，5 以内得到 0、2、4 三个值。""",
 ],
 pitfall="""调用生成器函数只是“造出生成器对象”，函数体一行都不执行；第一次 next()/for 才真正开始跑。"""),

"ch7/test16.py": dict(
 title="生成器耗尽后抛 StopIteration",
 notes=[
  """gen(3) 依次 yield 0、1、2，共 3 个值。""",
  """第 4 次 next(g) 时生成器已结束，抛 StopIteration——这是文件里的演示错误。""",
  """正确写法是用 for 遍历，或把 next() 包在 try-except 中。""",
 ],
 pitfall="""next() 调用次数不能超过元素个数，多调一次就报 StopIteration。"""),

"ch7/test17.py": dict(
 title="装饰器的基本结构",
 notes=[
  """装饰器本质是“接收函数、返回新函数”的高阶函数。""",
  """@wrapper 等价于 test = wrapper(test)，所以装饰发生在函数定义时，而不是调用时。""",
  """wrapper 内部的 print 在装饰那一刻就执行，因此先输出 1.、<class 'function'>、2.。""",
  """真正调用 test() 时执行的是 inner：先打印验证权限，再调用原函数打印 test。""",
 ]),

"ch7/test18.py": dict(
 title="多个装饰器叠加的执行顺序",
 notes=[
  """@wrapper1 在 @wrapper2 之上，装饰顺序由内向外：先用 wrapper2 装饰 test，再用 wrapper1 装饰其结果。""",
  """所以装饰阶段先打印 wrapper2 的 3.、正在装饰 2，再打印 wrapper1 的 2.、正在装饰 1。""",
  """运行时由外向内：inner1 先执行（正在验证权限 1），再调用 inner2（正在验证权限 2），最后才是真正的 test。""",
  """两个 time.sleep 让装饰过程与运行过程有明显时间间隔，便于观察顺序。""",
 ],
 pitfall="""离函数越近的装饰器越先装饰（越在内层），但执行时越靠外层的包装器越先运行。"""),

"ch7/test19.py": dict(
 title="带参数的装饰器 + functools.wraps + 写日志",
 notes=[
  """logit(logfile) 返回 logging_decorator，logging_decorator 再返回 wrapped_function，三层嵌套是“带参数装饰器”的标准写法。""",
  """@logit() 相当于先调用 logit() 得到装饰器，再用它装饰 myfunc1。""",
  """wrapped_function(*args, **kwargs) 先把调用信息拼成字符串打印并追加写入 out.log，再 return func(*args, **kwargs) 执行原函数。""",
  """@wraps(func) 保留原函数的 __name__ 和文档字符串，否则被装饰后函数名会变成 wrapped_function。""",
  """所以输出先是一行调用日志（含时间、函数名、参数），然后是 myfunc1 的结果 7。""",
 ],
 pitfall="""装饰器里一定要 return 原函数的调用结果，否则被装饰函数就“没有返回值”了。"""),

"ch7/test20.py": dict(
 title="map 返回迭代器，只能消费一次",
 notes=[
  """map(square, ls) 返回 map 对象（迭代器），直接 print 显示 <map object>，不是列表。""",
  """4 次 next(res) 分别取出 1、4、9、16。""",
  """之后再 for i in res，只剩下最后一个元素 25，所以 lm 是 [25]。""",
 ],
 pitfall="""map/filter/zip 在 Python 3 都返回一次性迭代器，取过的元素不会再有；要保留请先 list()。"""),

"ch7/test21.py": dict(
 title="zip 与字典配合：迭代字典得到的是键",
 notes=[
  """被三引号包住的第一段演示 zip 两个序列的情况。""",
  """zip(ls, dn) 把列表元素与字典的“键”配对，得到 (1,31)、(2,32)、(3,33)。""",
  """dn[v] 再用键 v 取出对应的值 2、6、8。""",
  """zip(ls, dc) 同理，配对出的是城市名的键，所以输出 1 北京、2 纽约、3 巴黎。""",
 ],
 pitfall="""直接迭代字典（或 zip 里放字典）拿到的是键，不是键值对；需要值请显式用 dc[key]。"""),

"ch7/test81.py": dict(
 title="*args 与 **kwargs 同时使用",
 notes=[
  """def test(*args, **kwargs) 同时接收任意个位置实参和关键字实参。""",
  """args 是元组，用 len() + 下标遍历；kwargs 是字典，用 keys() + get() 遍历。""",
  """调用 test(1,2,3) 时只有位置实参，所以只输出 1、2、3，kwargs 部分没有输出。""",
  """本文件被前面的 test11 等模块 import，注意区分“单独运行”与“被导入”时的输出差异。""",
 ]),
}

d = json.load(open(P, encoding="utf-8"))
d.update(CH7)
json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("notes total:", len([k for k in d if not k.startswith("_")]))
