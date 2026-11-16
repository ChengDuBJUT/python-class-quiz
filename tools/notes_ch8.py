# -*- coding: utf-8 -*-
"""合并 ch8 学习卡到 code_notes.json"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "source", "code_notes.json")

CH8 = {
"ch8/test1.py": dict(
 title="类属性与实例方法的最小示例",
 notes=[
  """color="red" 写在类里、方法外，是类属性，所有实例共享。""",
  """car.color 先在实例上找，找不到就去类里找，所以得到 red。""",
  """car.drive() 调用实例方法，self 自动绑定为 car，所以方法体里能直接用 self。""",
  """输出顺序：先打印 red，再打印 行驶。""",
 ]),

"ch8/test2.py": dict(
 title="类属性与实例属性的赋值差异（最常考）",
 notes=[
  """初始时 Car.color 是 red，实例 car.color 读取类属性也是 red。""",
  """Car.color='white' 改的是类属性，所有还没自己定义 color 的实例读到的都变成 white。""",
  """car.color='black' 是给实例新建了一个同名实例属性，从此 car.color 走自己的，与类属性无关。""",
  """所以第 5 行 Car.color 仍是 white，第 6 行 car.color 变成 black。""",
 ],
 pitfall="""实例.属性 = 值 只会创建/修改实例属性，不会改动类属性；要改类属性必须写 类名.属性 = 值 或在类方法里用 cls。"""),

"ch8/test3.py": dict(
 title="self.color 只存在于实例上",
 notes=[
  """drive 里 self.color='white' 给实例加了一个属性，不是给类加。""",
  """所以 car.color 和 car.print_color() 都能拿到 white。""",
  """但 Car.color 在类上根本不存在，最后一行抛 AttributeError——这是老师故意留的演示错误。""",
 ],
 pitfall="""self.xxx = 值 只影响当前实例；类名.xxx 访问不到实例属性。"""),

"ch8/test4.py": dict(
 title="实例属性被方法改写、动态添加属性、用类名显式传 self",
 notes=[
  """car.drive() 把 self.color 设为 white；随后 car.color='red' 覆盖为 red；再调 drive 又回到 white。""",
  """car.wheels=4 说明 Python 允许随时给对象动态添加属性，不必在类里预先声明。""",
  """Car.drive(car) 是用“类名.方法名(实例)”的方式调用，等价于 car.drive()，self 由括号里的 car 提供。""",
  """Car.drive(car) 会重新把 color 设为 white，所以倒数第二行又打印 white。""",
  """print(Car.drive(car)) 打印的是方法的返回值；drive 没有 return，所以输出 None。""",
 ]),

"ch8/test5.py": dict(
 title="私有属性、单下划线约定、__dict__ 与 __doc__",
 notes=[
  """__color 双下划线开头是私有属性，名字被改写为 _Car__color，类外不能直接用 car.__color 访问。""",
  """_wheels 单下划线开头只是“约定为内部使用”，语法上仍可从外部访问，所以 car._wheels 得 4。""",
  """car.testColor() 与 Car.testColor(car) 等价，都是把实例作为 self 传入。""",
  """print(car.testColor()) 打印返回值，方法没有 return，输出 None。""",
  """car.__dict__ 只包含实例属性，这里是 {'size': 100}——__color 和 _wheels 都是类属性，不在其中。""",
  """car.__doc__ 是 None：三引号写在了类属性之后，不是类的第一行，所以不算类的文档字符串。""",
 ],
 pitfall="""双下划线是“名称改写”而非真正的私有，用 _Car__color 仍可访问；单下划线纯属约定。"""),

"ch8/test6.py": dict(
 title="类方法改类属性，影响所有实例",
 notes=[
  """@classmethod 修饰的 stop1 第一个参数是 cls（代表类本身），里面 cls.color='red' 改的是类属性。""",
  """改完之后，所有还没有自己 color 实例属性的对象读到的都是 red。""",
  """stop2 是普通实例方法，self.color='green' 只给 car1 建了实例属性，不影响类。""",
  """car2、car3 没有经过 stop2 前读到 red（类属性），执行 stop2 后各自变成 green。""",
  """所以每个分支都是先打印当前颜色，再打印修改后的颜色。""",
 ],
 pitfall="""cls.color = 改的是类属性（全局生效），self.color = 改的是实例属性（只影响自己）。"""),

"ch8/test7.py": dict(
 title="静态方法既没有 self 也没有 cls",
 notes=[
  """@staticmethod 修饰的 test 没有 self/cls，就是一个写在类里的普通函数。""",
  """它访问颜色时只能写 Car.color（硬编码类名），不能写 self.color。""",
  """静态方法用 对象.方法() 或 类.方法() 都能调用，效果一样。""",
  """drive 是实例方法，self.color='red' 只影响 car 这个实例。""",
  """所以三次调用 test 打印的 Car.color 始终是 black，不会因 drive 而改变。""",
 ],
 pitfall="""静态方法拿不到实例，无法访问实例属性；想访问实例属性必须定义成实例方法。"""),

"ch8/test8.py": dict(
 title="@property 把方法变成只读属性",
 notes=[
  """__age 先作为类属性定义为 10，__init__ 里又给实例设了私有属性 __age=18。""",
  """@property 把 age1 变成“读取属性”，访问时写 person.age1，不加括号。""",
  """age1 有一个带默认值的参数 x=1，返回 self.__age + x，所以结果是 18+1 = 19。""",
  """被注释的三行说明：只定义了 getter 时，给属性赋值会报 AttributeError（只读）。""",
 ],
 pitfall="""加了 @property 后必须用 person.age1 访问，写 person.age1() 会报 'int' object is not callable。"""),

"ch8/test9.py": dict(
 title="@property + @setter 实现可读可写的受控属性",
 notes=[
  """@property 定义 getter，返回私有属性 __age。""",
  """@age.setter 定义 setter，注意装饰器名要与属性名一致，且方法名也叫 age。""",
  """setter 里写 self.__age = age+1，所以 person.age = 25 实际存进去的是 26。""",
  """因此第一次打印 18，赋值后再打印 26。""",
 ],
 pitfall="""setter 里不要写成 self.age = age，那会递归调用 setter 导致无限递归。"""),

"ch8/test10.py": dict(
 title="私有方法只能通过类内部调用",
 notes=[
  """__drive 双下划线开头是私有方法，类外 car.__drive() 会报 AttributeError。""",
  """公有方法 test 内部写 self.__drive()，在类内部可以正常调用私有方法。""",
  """所以外部只调 car.test() 就能间接执行私有方法，输出 行驶。""",
  """构造方法接收 color 参数，所以实例化时必须传 'red'。""",
 ]),

"ch8/test11.py": dict(
 title="构造方法与析构方法的调用时机",
 notes=[
  """创建对象时自动执行 __init__，打印“对象被创建”并设置 color。""",
  """type(car) 显示 <class '__main__.Car'>，说明对象属于当前模块的 Car 类。""",
  """del car 删除引用后，对象被回收，自动执行 __del__，打印“对象被销毁”。""",
  """del 之后再 print(car.color) 会 NameError——car 这个名字已经不存在了。""",
 ],
 pitfall="""del 删的是“变量名（引用）”而不是对象本身；对象在没有任何引用时才被回收并触发 __del__。"""),

"ch8/test12.py": dict(
 title="__new__ 与 __init__ 的先后顺序",
 notes=[
  """实例化 Demo() 时先调用 __new__ 创建对象，再调用 __init__ 初始化。""",
  """所以先打印“此处是 __new__()方法的执行...”，再打印“此处是 __init__()方法的执行...”。""",
  """__new__ 收到的 args、kwargs 是空元组和空字典，因为实例化时没传参。""",
  """__new__ 必须 return super().__new__(cls) 把对象交出去，否则 __init__ 不会执行。""",
 ]),

"ch8/test13.py": dict(
 title="方法重定义与动态加属性",
 notes=[
  """类里 area 定义了两次，后一个覆盖前一个（Python 不支持方法重载）。""",
  """length、width 在类里被注释掉了，通过 r.length, r.width = 13, 8 动态加到实例上。""",
  """area() 返回 self.length * self.width = 13*8 = 104。""",
 ],
 pitfall="""同一个类里重复定义同名方法，只有最后一个有效——和函数重名覆盖是同一回事。"""),

"ch8/test14.py": dict(
 title="单例模式：用 __new__ 保证只创建一个实例",
 notes=[
  """__new__ 里判断 cls.instance 是否为空，为空才创建，否则直接返回已有实例——这就是单例。""",
  """两次 MusicPlayer() 打印的对象地址完全相同，说明拿到的是同一个对象。""",
  """init_flag 保证“初始化音乐播放器”只打印一次，即使重复实例化也不会重复初始化。""",
  """del player1 后对象仍有 player2 引用所以不销毁；“销毁”在程序结束时才打印。""",
 ],
 pitfall="""单例要在 __new__ 里控制对象创建；__init__ 每次实例化都会执行，需要额外标志位防止重复初始化。"""),

"ch8/test15.py": dict(
 title="用 type() 动态创建类",
 notes=[
  """type(类名, 父类元组, 属性字典) 是动态创建类的标准写法。""",
  """这里类名写成 MyClass0，父类是 (object,)，属性字典把 say、say2、name、color 一次性塞进去。""",
  """创建出的类可以正常实例化并调用方法、读取属性。""",
  """type(myobj) 显示 <class '__main__.MyClass0'>，说明类的名字是字典第一个参数决定的。""",
 ]),

"ch8/test16.py": dict(
 title="自定义元类，在类创建时动态改属性",
 notes=[
  """继承 type 定义元类，重写 __new__ 即可在“类被创建”的那一刻修改它的属性。""",
  """attrs['name']='李红' 把类属性 name 强制改成李红；attrs['say']=say 给类动态添加方法。""",
  """class MyClass(object, metaclass=MyMetaclass) 指定用这个元类来创建 MyClass。""",
  """所以 myobj.name 得李红，say1 是类里自己定义的 hello，say 是元类塞进来的我爱Python。""",
 ],
 pitfall="""元类改的是“类”的创建过程，影响所有用它的类；日常开发极少用到，多用于框架。"""),

"ch8/test17.py": dict(
 title="多继承的 MRO（方法解析顺序）",
 notes=[
  """class D(B, C) 同时继承 B 和 C，B、C 都继承 A。""",
  """D.__mro__ 与 D.mro() 展示查找顺序：D → B → C → A → object（C3 线性化）。""",
  """调用 x.show() 时按 MRO 顺序找，B 里没有 show，C 里有，所以执行 C.show()。""",
  """这正是“菱形继承”问题的解决方式：Python 用 MRO 保证每个类只出现一次且顺序确定。""",
 ],
 pitfall="""多继承同签名方法时，取 MRO 中靠前的那个类的方法，而不是“父类里定义的那个”。"""),

"ch8/test18.py": dict(
 title="元类重写 __instancecheck__ 定制 isinstance 行为",
 notes=[
  """元类里定义 __instancecheck__，会改变 isinstance 对这个类实例的判断逻辑。""",
  """isinstance(demo, Demo) 走的是元类的 __instancecheck__，里面又调用了真正的 isinstance。""",
  """isinstance(Demo, MyMetaclass) 为 True，说明 Demo 这个类本身是 MyMetaclass 的实例。""",
  """后两行手动调用 __instancecheck__，所以会额外打印 __instancecheck__call。""",
 ]),

"ch8/test19.py": dict(
 title="抽象基类 ABC 与 @abstractmethod",
 notes=[
  """继承 ABC 的类就是抽象基类，用 @abstractmethod 标记的方法必须由子类实现。""",
  """抽象基类本身不能实例化，否则报 TypeError。""",
  """ConcreteClass 实现了 abstract_method 和 abstract_property，可以正常实例化并调用。""",
  """被注释的 IncompleteClass 没有实现抽象方法，实例化时会报错——这是抽象类的约束作用。""",
 ]),

"ch8/test20.py": dict(
 title="用 register() 注册虚拟子类",
 notes=[
  """VirtualSubclass 并没有继承 AbstractBaseClass，但通过 .register() 注册成了虚拟子类。""",
  """注册后 issubclass 和 isinstance 都返回 True。""",
  """这只是“声明式”的关联，不会真的继承父类的方法，抽象方法仍需自己实现。""",
  """虚拟子类常用于“这个类已经存在、不方便改继承关系”的场景。""",
 ]),

"ch8/test21.py": dict(
 title="属性名不一致导致的 AttributeError",
 notes=[
  """__init__ 里设的是私有属性 self.__age=18，实际名字被改写成 _Person__age。""",
  """而 get_age 读的是 self.age（不是 __age），两者根本不是同一个属性。""",
  """第一次 print(person.get_age()) 时 age 还没被创建，于是抛 AttributeError。""",
  """set_age 里写的是 self.age=new_age，所以要先调用 set_age 才会有 age 这个属性。""",
 ],
 pitfall="""__age 与 age 是两个完全不同的属性；getter/setter 里必须用同一个名字，否则就会出现这种“读不到”的错误。"""),

"ch8/test22.py": dict(
 title="子类自动继承父类的公有成员",
 notes=[
  """WolfDog(Dog) 只写了 pass，但因为继承，自动拥有父类的 __init__ 和 walk。""",
  """实例化时 WolfDog("gray") 调用的是父类的 __init__，把 color 设为 gray。""",
  """wolfdog.color 能读到 gray，wolfdog.walk() 能执行“狗跳”。""",
 ]),

"ch8/test23.py": dict(
 title="子类不会继承父类的私有成员",
 notes=[
  """父类里 __age、__test 是私有成员，名字被改写为 _Dog__age、_Dog__test。""",
  """子类 WolfDog 的实例上不存在 __age（改写后是 _WolfDog__age，根本没创建过）。""",
  """所以 print(wolfdog.__age) 直接抛 AttributeError——这就是本文件注释说的“子类不会拥有父类的私有成员”。""",
  """若要在子类使用，应通过父类的公有方法间接访问，或改成单下划线 _age。""",
 ],
 pitfall="""私有成员的名称改写带类名，父类的 __x 变成 _Dog__x，子类里的 __x 会变成 _WolfDog__x，二者不通。"""),

"ch8/test24.py": dict(
 title="多继承时同名方法取哪一个",
 notes=[
  """TouringCar(House, Car) 同时继承 House 和 Car。""",
  """live 只在 House 里有，drive 只在 Car 里有，都可以正常调用。""",
  """play 在两个父类里都有：按 MRO 顺序，House 在前，所以执行 House.play()。""",
  """输出“House play!”而不是“Car play!”，这就是多继承同名成员的解析规则。""",
 ],
 pitfall="""父类列表里写在前面的优先，这是 MRO 的直接体现，考卷常把两个父类顺序调换来设陷阱。"""),

"ch8/test25.py": dict(
 title="子类方法重写（override）",
 notes=[
  """子类 Chinese 重新定义了 say_hello，覆盖父类 Person 的同名方法。""",
  """调用 chinese.say_hello() 时优先用子类自己的版本，输出“吃了吗”。""",
  """若子类没有重写，则沿用父类的“打招呼”。""",
 ]),

"ch8/test26.py": dict(
 title="多态的经典写法：同一接口不同实现",
 notes=[
  """Cat 和 Dog 各自实现 shout，二者没有继承关系。""",
  """函数 shout(obj) 只关心“传进来的对象有 shout 方法”，不关心它是什么类型。""",
  """传 cat 就“喵喵喵”，传 dog 就“汪汪汪”，这就是多态（鸭子类型）。""",
  """Python 的多态靠“方法名一致”实现，不要求继承同一个父类。""",
 ]),
}

d = json.load(open(P, encoding="utf-8"))
d.update(CH8)
json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("notes total:", len([k for k in d if not k.startswith("_")]))
