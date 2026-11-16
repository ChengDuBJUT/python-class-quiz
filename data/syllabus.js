/* 自动生成，请勿手改。重建：python tools/build_syllabus.py */
window.SYLLABUS = {
  "updated": "2026-11-16",
  "paper": [
    {
      "name": "选择题",
      "n": 40,
      "per": 1,
      "total": 40,
      "note": "判断题并入，统一出选择题"
    },
    {
      "name": "填空题",
      "n": 10,
      "per": 2,
      "total": 20,
      "note": "简答题并入，统一出填空题"
    },
    {
      "name": "编程题",
      "n": 8,
      "per": 5,
      "total": 40,
      "note": "必考：文件读写 1 道、递归 1 道、数制转换"
    },
    {
      "name": "附加题",
      "n": 1,
      "per": 10,
      "total": 10,
      "note": "难度高，拉开分差"
    }
  ],
  "range": {
    "chapters": "第 1–12 章（含课件 PPT、课后练习题）",
    "objective": "选择 40 + 填空 10 = 60 分，覆盖全 12 章",
    "code": "编程 8×5 = 40 分，第 1–8 章 + 第 10 章（文件）",
    "codeOut": "第 9、11、12 章编程不考",
    "note": "判断/简答不再单独出题：判断题按选择题考、简答题按填空题考，所以题库里的判断题、简答题同样是考试范围。"
  },
  "topics": [
    {
      "key": "feature",
      "name": "Python 特性",
      "chapters": [
        1
      ],
      "nObj": 22,
      "nCode": 5,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "encoding",
      "name": "编码方式",
      "chapters": [
        2,
        3
      ],
      "nObj": 11,
      "nCode": 0,
      "level": "thin",
      "codeInExam": true
    },
    {
      "key": "dtype",
      "name": "数据类型",
      "chapters": [
        3,
        6
      ],
      "nObj": 46,
      "nCode": 16,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "control",
      "name": "控制结构",
      "chapters": [
        5
      ],
      "nObj": 20,
      "nCode": 5,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "output",
      "name": "输出",
      "chapters": [
        2,
        3,
        6
      ],
      "nObj": 5,
      "nCode": 21,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "logic",
      "name": "判断逻辑",
      "chapters": [
        4,
        5
      ],
      "nObj": 40,
      "nCode": 10,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "func",
      "name": "函数",
      "chapters": [
        7
      ],
      "nObj": 33,
      "nCode": 11,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "scope",
      "name": "变量（局部/全局）",
      "chapters": [
        7,
        2
      ],
      "nObj": 15,
      "nCode": 0,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "oop",
      "name": "面向对象特征",
      "chapters": [
        8
      ],
      "nObj": 30,
      "nCode": 5,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "clsmethod",
      "name": "类方法",
      "chapters": [
        8
      ],
      "nObj": 12,
      "nCode": 0,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "objmethod",
      "name": "对象方法",
      "chapters": [
        8
      ],
      "nObj": 12,
      "nCode": 5,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "exception",
      "name": "异常",
      "chapters": [
        9
      ],
      "nObj": 24,
      "nCode": 5,
      "level": "ok",
      "codeInExam": false
    },
    {
      "key": "recursion",
      "name": "函数嵌套递归",
      "chapters": [
        7
      ],
      "nObj": 8,
      "nCode": 7,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "file",
      "name": "文件读取关闭",
      "chapters": [
        10
      ],
      "nObj": 23,
      "nCode": 10,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "import",
      "name": "导入模块",
      "chapters": [
        1,
        2,
        11
      ],
      "nObj": 21,
      "nCode": 12,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "indent",
      "name": "缩进",
      "chapters": [
        2
      ],
      "nObj": 6,
      "nCode": 0,
      "level": "thin",
      "codeInExam": true
    },
    {
      "key": "namespace",
      "name": "命名空间",
      "chapters": [
        2,
        7,
        8
      ],
      "nObj": 10,
      "nCode": 0,
      "level": "thin",
      "codeInExam": true
    },
    {
      "key": "object",
      "name": "对象",
      "chapters": [
        2,
        8
      ],
      "nObj": 28,
      "nCode": 6,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "state",
      "name": "状态",
      "chapters": [
        2,
        8
      ],
      "nObj": 17,
      "nCode": 5,
      "level": "ok",
      "codeInExam": true
    },
    {
      "key": "base",
      "name": "数制转换",
      "chapters": [
        3
      ],
      "nObj": 8,
      "nCode": 5,
      "level": "ok",
      "codeInExam": true
    }
  ],
  "templates": [
    {
      "key": "file",
      "name": "文件读写",
      "must": true,
      "why": "考纲原文「编程题必考一道文件」。分值 5 分，但它是唯一能稳定拿分的模板题——四个动作（打开 → 读/写 → 处理 → 关闭）背下来就能套。",
      "code": "with open(\"test.txt\", \"r\", encoding=\"utf-8\") as f:\n    text = f.read()          # 全部读成字符串\n    # f.readline()   读一行\n    # f.readlines()  读全部行 → 列表\nprint(text)\n\nwith open(\"out.txt\", \"w\", encoding=\"utf-8\") as f:\n    f.write(\"要写的内容\\n\")  # 写字符串，换行要自己加\n",
      "points": [
        "模式：r 只读（文件必须存在）/ w 清空重写 / a 追加末尾",
        "with 会自动 close，不写 with 就必须手动 f.close()",
        "read(n) 读 n 个字符；readlines() 返回列表且每行带 \\n，要 strip()",
        "write() 只能写字符串，写数字要先 str()；写 CSV 用 \",\".join(row) + \"\\n\"",
        "中文一定要写 encoding=\"utf-8\"，Windows 默认 GBK 会乱码"
      ]
    },
    {
      "key": "recursion",
      "name": "递归",
      "must": true,
      "why": "考纲原文「编程题必考一道递归」。判分主要看有没有写对出口和递推式，再加一句\"参数每次都朝出口靠近\"就完整了。",
      "code": "def fact(n):\n    if n == 1:                  # ① 终止条件（递归出口）\n        return 1\n    return n * fact(n - 1)      # ② 递推：把问题缩小一层\n\nprint(fact(5))                  # 120\n",
      "points": [
        "三件套：出口 + 递推式 + 参数向出口收敛，缺一样就不是递归",
        "常见变式：阶乘、1..n 求和、斐波那契、汉诺塔、快排、字符串反转",
        "没有出口 → RecursionError: maximum recursion depth exceeded",
        "Python 默认递归深度约 1000 层，规模大要改循环或加记忆化"
      ]
    },
    {
      "key": "base",
      "name": "数制转换",
      "must": true,
      "why": "考纲原文「…以及数进制的转换」。两种写法都要会：调内置函数（一行解决）和手写\"除基取余\"（考算法思路时用）。",
      "code": "n = 26\nprint(bin(n), oct(n), hex(n))   # 0b11010 0o32 0x1a\nprint(bin(n)[2:])               # 11010  （切掉 0b 前缀）\nprint(int(\"11010\", 2))          # 26     （按二进制解释字符串）\n\ndef to_base(n, base):           # 手写：除基取余\n    digits = \"0123456789ABCDEF\"\n    if n < base:\n        return digits[n]\n    return to_base(n // base, base) + digits[n % base]\n",
      "points": [
        "bin/oct/hex 返回的是带前缀的字符串，不能直接参与算术运算",
        "int(字符串, 进制) 是反方向：int(\"2F\", 16) = 47",
        "除基取余 = 反复 %基数 得余数、//基数 缩小，余数要倒着读",
        "十六进制里 A~F 代表 10~15"
      ]
    }
  ],
  "stats": {
    "blank": 79,
    "single": 94,
    "judge": 60,
    "short": 60,
    "code": 79
  },
  "total": 372
};
