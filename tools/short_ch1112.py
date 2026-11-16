# -*- coding: utf-8 -*-
"""写入 ch11-12 简答题参考答案到 short_answers.json"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "source", "short_answers.json")

NEW = {
"ch11-short-01": dict(
 origin="ppt", basis="第11章 p5-7",
 answerText="""os 模块为 Python 脚本调用各类操作系统（Unix、Mac OS、DOS 等）的接口提供了统一的封装，使脚本代码与平台无关，从而增强了代码的可移植性。当需要实现某些功能却无法直接使用命令行工具时，就可以导入这个模块。

主要功能可分为属性和方法两部分：

(1) 常用属性（描述当前系统的环境信息）：os.name 记录操作系统名称（Windows 为 nt，Linux/Unix 为 posix）；os.sep 记录路径分隔符（Unix 为 '/'，Windows 为 '\\'）；os.extsep 记录文件名与扩展名的分隔符；os.linesep 记录行分隔符（Unix 为 '\\n'，Windows 为 '\\r\\n'）；os.curdir、os.pardir 分别表示当前目录和父目录；os.defpath 记录系统默认查找路径。

(2) 常用方法（操作文件与目录）：os.getcwd() 返回当前工作目录；os.mkdir() 创建目录（只能建一级）；os.rmdir() 删除目录（不能删非空目录）；os.listdir() 返回指定目录下所有文件名和目录名组成的列表；os.rename() 重命名文件或目录；os.remove() 删除指定文件；os.chmod() 修改访问权限；os.getenv()/os.putenv() 获取和设置环境变量。

此外 os.path 子模块专门负责路径处理，如拼接、拆分、判断文件是否存在等。"""),

"ch11-short-02": dict(
 origin="ppt", basis="第11章 p8-11",
 answerText="""sys 模块是与 Python 解释器交互的一个接口，提供了许多属性和方法，用来与解释器进行信息交互。

(1) 常用属性：sys.version 返回版本信息字符串；sys.platform 返回操作系统平台名称；sys.path 是模块搜索路径（path[0] 是当前脚本程序所在路径）；sys.modules 是已加载模块的字典；sys.argv 是命令行参数（argv[0] 是当前脚本程序路径名）；sys.builtin_module_names 是内建模块名称组成的字符串元组；sys.executable 是解释程序路径；sys.stdin、sys.stdout、sys.stderr 分别是标准输入、标准输出、标准错误流（input() 和 print() 底层就用它们）。

(2) 常用方法：sys.exit([arg]) 在程序中间退出（arg=0 表示正常退出）；sys.getdefaultencoding()/sys.setdefaultencoding() 获取和设置系统默认编码；sys.getfilesystemencoding() 获取文件系统编码（Windows 下返回 'mbcs'）；sys.getrecursionlimit()/sys.setrecursionlimit(n) 获取和修改递归深度限制；sys.getrefcount() 查看对象的引用计数。

借助这些属性和方法，程序可以获得运行环境信息（路径、平台、版本）、接收命令行参数、控制程序退出，从而实现与解释器的交互。"""),

"ch11-short-03": dict(
 origin="ppt", basis="第11章 p54-57、p63-74",
 answerText="""Python 中实现并发执行（多任务）有 3 种方式：多进程、多线程、多协程，分别对应 multiprocessing、threading、asyncio 三个模块。

(1) 多进程：进程是具有一定独立功能的程序在某个数据集合上的一次运行活动，是系统进行资源分配和调度的一个独立单位，也是资源（内存）分配的最小单位。每个进程有独立的内存空间，进程间通过通信机制通信；上下文切换开销较大，但稳定、安全。用 multiprocessing.Process 类创建进程对象（有 name、pid、daemon 等属性，用 start() 启动、join() 等待）。

(2) 多线程：线程是进程的一个实体，是 CPU 调度和分配的基本单位，比进程更小。线程本身基本不拥有系统资源，可与同一进程内的其他线程共享进程的全部资源；线程间通信主要通过共享内存，切换速度快、开销少，但不够稳定、容易丢失数据。用 threading.Thread 创建线程。

(3) 多协程：协程是用户态的轻量级线程，调度完全由用户控制，拥有自己的寄存器上下文和栈；切换时没有内核切换开销，可以不加锁地访问全局变量，因此切换非常快。用 asyncio 模块的 async/await、事件循环（loop）与任务（task）实现。

选择依据：先判断程序属于 CPU 密集型还是 I/O 密集型。CPU 密集型（科学计算、机器学习等偏重计算的程序）选多进程；I/O 密集型（如爬虫这类频繁输入输出的程序）选多线程或多协程。"""),

"ch11-short-04": dict(
 origin="ppt", basis="第11章 p74-76",
 answerText="""socket 模块的作用是：通过 TCP/IP 协议族中的 TCP 和 UDP 实现计算机之间的网络通信。

(1) 通信协议：TCP 是流协议，在客户机与服务器之间建立持续的开放连接，连接存续期内字节可经该连接写出并保证顺序正确，但字节流内部没有结构，需高层协议自己分隔数据记录；UDP 是数据报协议，不需要建立连接，只在地址之间传输报文，其包是自分隔的（每个数据报明确标明起止位置），但不保证按顺序到达、甚至不保证能到达，优点是效率高。

(2) socket（套接字）本身是操作系统内核中的一个数据结构，几乎是所有网络通信的基础。网络通信最终实现的是计算机进程间的通信：网络中每个节点都有 IP 地址，通信时先确定 IP 地址，再用端口号与进程一一对应，由 IP 地址加端口号确定一次通信的一端，即一个 socket 对象。

(3) 编程接口：通过 socket 对象的相关方法（如 connect() 连接、bind() 绑定、listen() 监听、accept() 接受连接、send()/recv() 收发数据、close() 关闭）完成通信连接和数据传输，从而编写客户端与服务器端程序。"""),

"ch11-short-05": dict(
 origin="ppt", basis="第11章 标准库列表中提及 sqlite3（课件未展开此小节，操作步骤按 Python 官方标准用法整理）",
 answerText="""sqlite3 是 Python 内置的轻量级关系型数据库模块，无需单独安装服务器，数据保存在单个文件中即可使用 SQL 进行增删改查。基本操作步骤如下：

(1) 导入模块并连接数据库：import sqlite3；conn = sqlite3.connect('test.db')。数据库文件不存在时会自动创建，返回一个连接对象。

(2) 创建游标：cur = conn.cursor()。游标用于执行 SQL 语句并获取结果。

(3) 执行 SQL：cur.execute(sql) 执行一条语句，如建表 CREATE TABLE、插入 INSERT、更新 UPDATE、删除 DELETE、查询 SELECT；批量执行可用 cur.executemany(sql, 序列)。SQL 中可用 ? 作占位符并通过参数元组传值，避免拼接字符串带来的注入风险。

(4) 提交事务：执行增、删、改后必须调用 conn.commit() 才会真正写入数据库；失败时可用 conn.rollback() 回滚。

(5) 获取查询结果：cur.fetchone() 取一行、cur.fetchmany(n) 取 n 行、cur.fetchall() 取全部行；也可直接迭代游标。

(6) 释放资源：cur.close() 关闭游标，conn.close() 关闭连接（也可用 with 语句自动管理）。

说明：本课程课件仅把 sqlite3 列在标准库清单中，未展开讲解，以上为 Python 标准用法，考试若考到按此流程作答即可。"""),

"ch12-short-01": dict(
 origin="ppt", basis="第12章 p3-19",
 answerText="""随着开源运动的兴起，大量专业人士通过开源库发布各领域的研究与开发成果，形成了庞大的编程计算生态；Python 语言能把不同语言、不同特点、不同使用方式的代码统一起来，从诞生之初就致力于开源开放，建立起了全球最大的编程计算生态。

(1) 规模：Python 拥有十几万个第三方库，其基本信息可通过 Python 官网或 GitHub 搜索到，几乎覆盖了信息技术的所有领域。一个人不可能熟悉所有库，只需记住名称，解决问题时再深入研究。

(2) 常用应用领域及代表库：
· 网络爬虫：requests（网络请求）、BeautifulSoup（网页解析）、Scrapy/Pyspider（爬虫框架）；
· 数据分析：NumPy（科学计算基础包）、SciPy（数学科学工程计算）、Pandas（高性能数据结构与分析工具）；
· 数据可视化：Matplotlib（pyplot 绘图）、TVTK（三维可视化）等；
· Web 开发：Django（最流行的 Web 框架）、Tornado（Web 框架兼异步网络库）、Flask（微型框架）；
· 其他：自然语言处理、办公自动化、音视频处理、图像处理、图形艺术、游戏开发（Pygame、Panda3D）、硬件开发（rospy、Pingo）、经济金融（TA-Lib、Quantopian）、社会网络分析（NetworkX）等。

(3) 意义：这种生态使开发者可以“站在他人肩上”，通过 import 复用成熟代码，大幅降低开发难度、提高效率。"""),

"ch12-short-02": dict(
 origin="ppt", basis="第12章 p24-26",
 answerText="""1. NumPy 简介：NumPy（Numerical Python）是 Python 的一种开源数值计算扩展库，可用来存储和处理大型矩阵，比 Python 自身的嵌套列表结构高效得多；它支持大量的多维度数组与矩阵运算，并针对数组运算提供了大量数学函数库。它是数据分析“三剑客”之一，侧重于科学计算（Pandas 侧重数据分析，Matplotlib 侧重可视化）。

2. NumPy 的数据结构：NumPy 中最重要的对象是 ndarray，即 N 维数组类型对象（也称 array 对象）。它描述相同类型元素的集合，可使用基于 0 的索引访问元素；ndarray 中每个元素在内存中占用相同大小的块，每个元素都是数据类型对象（dtype）的对象，NumPy 支持的数据类型比 Python 内置类型多得多。

ndarray 具有矢量算术能力、复杂的广播能力和高维数组处理能力，进行复杂科学计算时还会自动并行计算，运算效率远高于纯 Python 代码。

3. 常用属性：ndim（秩，即轴的数量/维度数）、shape（数组维度，矩阵为 n 行 m 列）、size（元素总个数，等于 shape 的 n*m）、dtype（元素类型）、itemsize（每个元素占用的字节数）、flags（内存信息）、real/imag（元素的实部/虚部）、data（数据缓冲区）、T（转置）。

4. 常用操作：用 np.array(列表) 创建数组，另有 arange、zeros、ones、reshape 等；支持 max/min/mean/sum 等聚合运算并可用 axis 指定按行或按列计算。"""),

"ch12-short-03": dict(
 origin="ppt", basis="第12章 p56-58",
 answerText="""使用 pyplot 模块绘制基本图形的一般步骤与语法如下：

(1) 导入模块：import matplotlib.pyplot as plt（常同时导入 numpy 用于生成数据）。

(2) 创建画布对象：fig = plt.figure(num=None, figsize=None, dpi=None, facecolor=None, edgecolor=None, frameon=True)。参数含义：num 为图像编号或名称（数字是编号、字符串是名称）；figsize 指定 figure 的宽和高，单位为英寸；dpi 指定分辨率，即每英寸多少像素，缺省为 80；facecolor 为背景颜色；edgecolor 为边框颜色；frameon 表示是否显示边框。

(3) 绘制图形：
· 直接用 pyplot：plt.plot([1,2,3,4], [1,2,3,4])，可加 color、linestyle、marker 等参数，另有 bar()、scatter()、pie() 等；
· 或用 axes 方式：ax = fig.add_subplot(1,1,1) 取得子图对象后 ax.plot(x, y)，适合在一个画布中绘制多个子图。

(4) 设置与修饰：plt.title() 设标题、plt.xlabel()/plt.ylabel() 设坐标轴标签、plt.legend() 显示图例、plt.grid() 显示网格。

(5) 显示或保存：plt.show() 显示图形；plt.savefig('a.png') 保存为图片文件。

核心三步可概括为：创建画布（figure）→ 绘制图形（plot）→ 显示（show）。"""),

"ch12-short-04": dict(
 origin="ppt", basis="第12章 p15（Web 框架库表）、p4-19（各类框架库）",
 answerText="""软件开发框架是为某一类软件开发提供基础结构与通用功能的“半成品”代码库：框架负责程序的骨架、流程控制和通用机制，开发者只需按约定填充业务逻辑，从而避免重复造轮子、统一开发规范、提高开发效率。

按应用领域，常见的 Python 开发框架可分为：

(1) Web 框架：用于 Web 程序开发。Django 是 Python 界最流行的 Web 框架（全栈、功能完备，自带 ORM、后台管理）；Tornado 既是 Web 框架又是异步网络库，适合高并发；Flask 是微型框架，轻量灵活，适合中小型项目与快速原型。

(2) 网络爬虫框架：Scrapy、Pyspider 等，提供请求调度、解析、去重、存储的完整流程。

(3) 深度学习框架：TensorFlow（谷歌开源）、PyTorch 等，提供张量与自动求导等能力。

(4) 游戏开发框架：Pygame（一组用于编写游戏的模块）、Panda3D（3D 游戏引擎）、RenPy（视觉小说引擎）、Harfang3D（支持 3D、VR）。

(5) 图形界面框架：跨平台的 GUI 框架（如 PyQt、Tkinter 等）。

(6) 测试与其他专用框架：unittest、pytest（测试框架），以及各垂直领域（金融、硬件、社会网络分析）的专用框架。

使用框架的一般思路是：选型（按项目规模与需求选全栈或微型框架）→ 按框架约定组织目录与代码 → 在框架提供的扩展点上编写业务逻辑 → 借助框架内置的中间件、模板、ORM 等能力完成开发与部署。"""),

"ch12-short-05": dict(
 origin="ppt", basis="第12章 p35-36",
 answerText="""1. Pandas 简介：Pandas 是 Python 的一个扩展程序库，是一个强大的用于分析结构化数据的工具集，其使用基础是 NumPy（由 NumPy 提供高性能的矩阵运算）。它纳入了大量库和标准数据模型，并提供了高效操作大型数据集所需的工具。

2. 功能：可以从各种文件格式（CSV、JSON、SQL、Microsoft Excel 等）导入数据；可对数据进行归并、再成形、选择等运算操作；还具备数据清洗和数据特征加工等功能，被广泛应用于学术、金融、统计学等数据分析领域。

3. Pandas 的数据结构：主要数据结构是 Series（一维数据）与 DataFrame（二维数据），二者足以处理金融、统计、社会科学、工程等领域中的大多数典型用例。
· Series 对象：类似于一维数组的对象，由一组数据（各种 NumPy 数据类型）及一组与之相关的数据标签（即索引）组成；仅有一组数据也可产生简单的 Series 对象。
· DataFrame 对象：Pandas 中的表格型数据结构，包含一组有序的列，每列可以是不同的值类型（数值、字符串、布尔型等）；DataFrame 既有行索引也有列索引，可以看作由 Series 组成的字典。

4. 与 NumPy 的关系与分工：NumPy 侧重科学计算、提供 ndarray 多维数组；Pandas 建立在其之上，侧重结构化数据的处理与分析，用带标签的 Series/DataFrame 弥补了 ndarray 缺少行列标签的不足。"""),
}

d = json.load(open(P, encoding="utf-8"))
d.update(NEW)
json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("short answers:", len([k for k in d if not k.startswith("_")]))
