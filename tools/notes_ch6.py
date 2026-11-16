# -*- coding: utf-8 -*-
"""合并 ch6 学习卡到 code_notes.json"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "source", "code_notes.json")

CH6 = {
"ch6/test1.py": dict(
 title="元组的聚合函数、迭代器对象与集合的可哈希限制",
 notes=[
  """max/min/sum/len 直接作用于元组：(10,25,16,8,32) 得最大值 32、最小值 8、和 91、长度 5。""",
  """sorted(tp) 返回排好序的新列表 [8,10,16,25,32]，原元组 tp 不变（元组本身不可变）。""",
  """reversed(tp) 返回的是 reversed 迭代器对象，直接 print 显示 <reversed object>，要 list() 才能看到 [32,8,16,25,10]。""",
  """enumerate(tp) 返回枚举对象，list() 后得到 [(0,10),(1,25),...]；for index,value in enumerate(tp) 可同时拿到下标和值。""",
  """set1.add(3)、add(4) 之后把 b 改成 5，集合仍是 {3,4}——集合里存的是加入那一刻的值副本。""",
  """l1 = list([a,b]) 同样是值拷贝，之后 a=5 不会改变 l1，仍为 [3,5]。""",
  """set1.add(l1) 抛 TypeError: unhashable type: 'list'——列表是可变类型、不可哈希，不能放进集合（也不能当字典键）。""",
 ],
 pitfall="""集合/字典的键必须是可哈希（不可变）的对象；列表、字典、集合都放不进去，元组可以（只要其元素也都可哈希）。"""),

"ch6/test2.py": dict(
 title="iter() 生成迭代器、next() 逐个取值",
 notes=[
  """for i in l 是最常用的遍历方式，背后自动完成 iter() 与 next()。""",
  """iter(l) 把可迭代对象转成迭代器，type 显示 <class 'list_iterator'>。""",
  """next(x) 每次取出一个元素；这里正好调用 4 次，所以依次输出 1、2、3、4。""",
  """若再多调一次 next() 就会抛 StopIteration。""",
 ]),

"ch6/test3.py": dict(
 title="while True + StopIteration 手动遍历迭代器",
 notes=[
  """iter(l) 得到迭代器 d，每次 next(d) 取下一个元素。""",
  """取完 5 个元素后再 next(d) 会抛 StopIteration，被 except 捕获后打印 iteration finished! 并 break。""",
  """这就是 for 循环的底层机制：不断 next() 直到 StopIteration。""",
 ]),

"ch6/test4.py": dict(
 title="自定义可迭代类：__iter__ 与 __next__",
 notes=[
  """__iter__ 返回迭代器自身并把计数 n 重置为 0，使对象可被 for 遍历或 iter() 转换。""",
  """__next__ 返回当前 n 并自增；当 n 超过 max 时 raise StopIteration 结束迭代。""",
  """max=5 时 if self.n <= self.max 成立 6 次，所以输出 e: 0 到 e: 5。""",
  """while True 循环结束后又调了一次 next(myIter)，此时已越界，抛出的 StopIteration 无人捕获——这是老师故意留下的演示错误。""",
 ],
 pitfall="""__next__ 必须用 raise StopIteration 表示结束；越界后再 next() 一定报错，别在循环外用。"""),

"ch6/test5.py": dict(
 title="跨文件导入自定义类",
 notes=[
  """from test4 import MyIterable 把同目录下另一个模块里的类导入使用。""",
  """两个 .py 文件在同一目录时可直接按模块名（去掉 .py）导入。""",
  """for i in numbers 会自动调用 __iter__ 和 __next__，max=3 时输出 0、1、2、3 共 4 行。""",
 ]),

"ch6/test7.py": dict(
 title="字符串查找、替换与对齐",
 notes=[
  """三引号里是 find() 三种签名的说明，被当成注释，不执行。""",
  """str.replace('t','s') 返回新字符串 bjus，原字符串 str 仍是 bjut——字符串不可变。""",
  """ljust(10,'s') 左对齐并用 s 补到总宽 10 位，得 bjutssssss。""",
  """isdigit() 判断是否全为数字，成立才转 float，1234567 变成 1234567.0。""",
  """find 返回首次出现的下标（找不到返回 -1），rfind 从右往左找，count 统计出现次数。""",
  """find('.',7) 从下标 7 开始找；find('.',7,-3) 在 [7, 长度-3) 区间内找，所以 n2、n3 都是 8。""",
  """replace('u','o',2) 的第三个参数限制最多替换 2 次，只把前两个 u 换成 o。""",
 ]),

"ch6/test8.py": dict(
 title="replace / split / join 与大小写转换链",
 notes=[
  """replace('hello','HELLO',1) 只替换第一个 hello。""",
  """sr1.split() 不传参数时按任意空白切分，得到 5 个单词的列表。""",
  """'-how '.join(sr2) 用分隔符把列表元素连接成一个字符串。""",
  """lower 全小写、capitalize 首字母大写、title 每个单词首字母大写、upper 全大写，四种转换逐级叠加。""",
  """这些方法都返回新字符串，原字符串始终不变。""",
 ],
 pitfall="""capitalize 只把整串的第一个字符大写，title 才把每个单词首字母都大写。"""),

"ch6/test9.py": dict(
 title="strip / lstrip / rstrip 去除首尾字符",
 notes=[
  """strip('x') 去掉首尾所有的 x，中间的不动。""",
  """lstrip('y') 只去左边，rstrip('z') 只去右边。""",
  """strip() 不带参数时去掉首尾空白（空格、换行、制表符）。""",
  """参数是“字符集合”而不是子串：strip('xyz') 会去掉首尾任意 x、y、z 字符。""",
 ]),

"ch6/test10.py": dict(
 title="三种对齐：ljust / rjust / center",
 notes=[
  """ljust(40,'*') 左对齐、右侧补 * 到总宽 40。""",
  """rjust(40,'$') 右对齐、左侧补 $。""",
  """center(40,'%') 居中、两边补 %；长度差为奇数时左边会比右边少一个。""",
 ],
 pitfall="""宽度参数是“补到总宽多少列”，不是“补几个字符”，字符串本身已占去一部分宽度。"""),

"ch6/test11.py": dict(
 title="列表推导式全解（含嵌套、条件、zip）",
 notes=[
  """remove(3) 按值删除；pop(2) 按下标删除并返回被删元素。""",
  """[x for x in range(1,5)] 得 [1,2,3,4]。""",
  """[i*2 for i in range(1,10) if i%2==0] 先筛偶数再乘 2，得 [4,8,12,16]。""",
  """[i+1 if i%2==0 else i*2 for i in (1,2,3,4)] 是推导式里的三目：偶数 +1、奇数 ×2，得 [2,3,6,5]。""",
  """[x+y for x in ls1 for y in ls2] 是双重 for，相当于嵌套循环，共 9 个元素，顺序 x 优先。""",
  """[x+y for (x,y) in zip(ls1,ls2)] 用 zip 按位置配对，得 [4,6,8]。""",
  """print(zip(...)) 显示 <zip object>，zip 返回迭代器，要用 list() 才能看到内容。""",
  """多重推导式里的 if 归属于离它最近的那层 for。""",
 ],
 pitfall="""嵌套 for 推导式中元素顺序是“外层慢、内层快”；zip 则是按位置一一配对，两者结果完全不同。"""),

"ch6/test12.py": dict(
 title="列表的增删方法",
 notes=[
  """append 把参数当成一个整体追加到末尾。""",
  """extend 把另一个序列的元素逐个追加进来。""",
  """insert(3,4) 在下标 3 处插入 4，后面的元素依次后移。""",
  """remove('5s') 按值删除第一次出现的元素。""",
  """pop(1) 按下标删除并返回该元素；pop() 不传参时删除最后一个。""",
  """同一列表里混放整数和字符串是允许的，Python 列表不要求元素类型一致。""",
 ],
 pitfall="""append([7,8]) 只会把列表整体塞成一个元素；要合并两个列表请用 extend 或 +。"""),

"ch6/test13.py": dict(
 title="生成器表达式（圆括号）与“只能消费一次”",
 notes=[
  """(i*2 for i in ...) 用圆括号是生成器表达式，返回 generator 对象，需 tuple()/list() 才展开。""",
  """tuple(tp1) 展开得 (4,8,12,16)。""",
  """tp2 被 while True 循环用 next() 逐个取完（e is 2、3、6、5），取完后抛 StopIteration 并打印结束提示。""",
  """关键：生成器耗尽后再 list(tp2) 得到空列表 []——生成器只能遍历一次。""",
 ],
 pitfall="""生成器/迭代器是“一次性”的，用过就空；要重复使用必须先 list() 存成列表。"""),

"ch6/test14.py": dict(
 title="集合推导式",
 notes=[
  """{i*2 for i in range(1,10) if i%2==0} 得 {4,8,12,16}。""",
  """{i+1 if i%2==0 else i*2 for i in [1,2,3,4]} 得 {2,3,5,6}。""",
  """集合自动去重且无序，打印顺序不保证与生成顺序一致。""",
 ]),

"ch6/test15.py": dict(
 title="集合增删与 copy 的意义",
 notes=[
  """add 加入单个元素，update 批量加入。""",
  """pop() 随机弹出一个元素并返回（这里弹出 1）。""",
  """st1 = st.copy() 得到独立副本，之后 st1.add(7) 不影响原集合 st。""",
  """注释里那句 st1=st 是反面对照：直接赋值只是起别名，改一个另一个跟着变。""",
 ]),

"ch6/test16.py": dict(
 title="集合的运算方法与判断方法",
 notes=[
  """intersection 交集、union 并集、difference 差集。""",
  """intersection_update 把交集写回 set1，于是 set1 变成 {3,4}。""",
  """symmetric_difference_update 求对称差并写回，set1 变成 {5,6}。""",
  """isdisjoint 判断是否无交集（False 说明有交集）；issubset 判断子集；issuperset 判断超集。""",
  """remove(4) 删除指定元素，不存在会报错；discard(2) 删除指定元素，不存在不报错。""",
  """clear() 清空集合，结果是 set()。""",
 ],
 pitfall="""remove 删不存在的元素会 KeyError，discard 不会——这是两者的唯一实质区别。"""),

"ch6/test17.py": dict(
 title="可哈希性：为什么元组能进集合、列表不能",
 notes=[
  """重复 add(1)、add(3) 集合内容不变，说明集合会自动去重。""",
  """frozenset 是不可变的“冻结集合”，可哈希，因此能作为元素放进集合。""",
  """st.add(tp1) 中元组 (1,2) 可哈希能加入；列表 li1 不可哈希，所以那一行被注释掉了。""",
  """li1.insert 前后 id 相同，说明列表是原地修改；原地可变就不能哈希。""",
  """对字符串 str 调用 capitalize 后赋回原名变量，id 变了——字符串不可变，相当于新建对象。""",
  """两个内容相同的字符串哈希值相同，说明 hash 由内容决定。""",
  """dc.__hash__ 打印的是方法对象本身，因为字典不可哈希，不能进集合。""",
 ],
 pitfall="""可哈希的前提是不可变；看 id 是否变化就能判断一个操作是原地修改还是产生了新对象。"""),

"ch6/test18.py": dict(
 title="字典推导式与 zip 迭代器只能消费一次",
 notes=[
  """{i:i**2 for i in range(1,10) if i%2==1} 只取奇数作键，值为其平方。""",
  """{i:i**2 if i%2==1 else i*2 for i in range(1,6)} 是值部分的三目：奇数平方、偶数乘 2。""",
  """zip(l1,l2) 返回迭代器，dc3 遍历完它之后已被耗尽。""",
  """紧接着 dc4 用同一个 iterable 推导，得到空字典 {}。""",
  """dc5 重新写了一次 zip(l1,l2) 才取到数据，筛出偶数键得 {4:40,8:80}。""",
  """对 dict 反复调用 iter(dc5) 每次都从第一个键开始，所以 next 反复打印 4。""",
 ],
 pitfall="""zip 对象是一次性迭代器，不能重复遍历；而对字典本身 iter() 每次都能得到新的迭代器。"""),

"ch6/test19.py": dict(
 title="split 拆分 + 字典推导式构造字典",
 notes=[
  """strings.split('/') 按斜杠切成 5 段。""",
  """每段再 split('=') 得到 [键, 值]，用 [0]、[1] 分别取键和值。""",
  """{k:v for ...} 把所有键值对一次性组装成字典。""",
  """注意值是字符串 '1' 而非整数 1，需要时用 int() 转换。""",
 ]),

"ch6/test20.py": dict(
 title="字典的常用视图：keys / values / items",
 notes=[
  """dict.fromkeys(course, 60) 用列表元素作键、统一给同一个默认值，批量建字典。""",
  """get('语文') 按键取值，键不存在时返回 None，比 dc['键'] 安全。""",
  """keys() / values() / items() 返回视图对象，打印形如 dict_keys([...])。""",
  """for key in dc.keys() 遍历键；for k,v in dc.items() 同时遍历键和值。""",
  """视图随字典动态更新；这里没做修改，所以两次遍历结果相同。""",
 ],
 pitfall="""dict_keys 不是列表，要 list() 转换；dc['不存在的键'] 会 KeyError，get 只返回 None。"""),

"ch6/test21.py": dict(
 title="字典的 update / setdefault / copy / pop / popitem",
 notes=[
  """update({'语文':90}) 会覆盖同名键的值，传入新键则相当于新增。""",
  """setdefault('语文',96)：键已存在，返回原值 90，不修改。""",
  """setdefault('体育',90)：键不存在，插入并返回 90。""",
  """dc1 = dc 只是起别名，之后 dc 更新，dc1 跟着变。""",
  """dc2 = dc.copy() 是独立副本，dc 后来加 '美术' 时 dc2 里没有。""",
  """pop('语文') 按键删除并返回值；popitem() 删除并返回最后一个键值对。""",
 ],
 pitfall="""dc1 = dc 与 dc2 = dc.copy() 结果完全不同，试卷常把这两行放一起考。"""),
}

d = json.load(open(P, encoding="utf-8"))
d.update(CH6)
json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("notes total:", len([k for k in d if not k.startswith("_")]))
