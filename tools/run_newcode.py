# -*- coding: utf-8 -*-
"""跑全部 12 章的示例代码，收集真实输出，用于生成代码学习卡。

第 4-11 章取「更新后的chapter」（老师陆续发过 4-8 与 9-11 两批更新），
其余章取原目录；每章兼容 `chapterN/chapterN/*.py` 与 `chapterN/*.py` 两种结构。

几个必要的处理：
- turtle 程序没有控制台输出，用临时 stub（记录绘图指令）跑，得到"绘图轨迹"
- matplotlib 程序切 Agg 后端，避免 plt.show() 阻塞
- 需要键盘输入的按 STDIN 表喂输入
- 每个文件在独立临时目录里跑，避免 polluting 课程目录（如 chapter10 会写 demo.csv）
- PYTHONPATH 带上 PROJ，让 `import chapter7.xxx` 这类跨章导入能解析
- 少数代码会往绝对路径写东西（如 ch11/test1 的 d:\\test），按 PATCH 表改写到临时目录
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(PROJ, "pythonProject-2025")
PY = r"E:\anaconda\envs\leaf_gcn\python.exe"
if not os.path.exists(PY):
    PY = sys.executable
TURTLE_STUB = os.path.join(tempfile.gettempdir(), "turtle_stub")

UP = None
for name in os.listdir(BASE):
    p = os.path.join(BASE, name)
    if os.path.isdir(p) and name.startswith("\u66f4") and "chapter" in name.lower():
        UP = p
        break
print("PY =", PY)
print("UP =", UP)

UPDATED = {4, 5, 6, 7, 8, 9, 10, 11}

# 少量代码直接操作绝对路径，跑一遍会在用户机器上留下目录（甚至泄露目录内容）。
# 这里把它们改写到各自的临时工作目录，语义完全一样，输出里的路径也本来就是临时的。
#   key -> [(原文, 替换成什么)]，占位符 {work} = 该文件的临时工作目录
PATCH = {
    ("ch11", "test1.py"): [(r"d:\test", "{work}\\dtest")],
}

STDIN = {
    ("ch4", "test4.py"): "8\n3\n",
    ("ch5", "test1.py"): "3\n",
    ("ch5", "test8.py"): "4\n",
    ("ch7", "test13.py"): "5\n",
    ("ch7", "test14.py"): "5\n",
    ("ch3", "test3.py"): "张三\n18\n90\n",
    ("ch3", "test14.py"): "1\n",
    ("ch9", "test3.py"): "10\n2\n",
    ("ch9", "test4.py"): "10\n0\n",      # 演示 ZeroDivisionError 被捕获
    ("ch9", "test5.py"): "张三\n2\n",     # 演示 except 元组同时接住 ValueError
    ("ch9", "test6.py"): "10\n2\n",      # 正常路径 + finally
    ("ch9", "test7.py"): "10\n2\n",      # 走 else 而不是 except
    ("ch9", "test8.py"): "10\n0\n",      # except + finally 都走
    ("ch9", "test11.py"): "10\n0\n",     # 触发 assert
    ("ch9", "test12.py"): "123\n",       # 密码太短 -> 自定义异常
    ("ch9", "test13.py"): "3\n10\n0\n",  # 异常沿 mul -> div 调用链传播
    ("ch11", "test3.py"): "hello\nhi\nworld\nbye\n",   # 每轮 readline + input，要 4 行
    ("ch12", "test8.py"): "20\n",
}


def chapter_files(ch):
    root = UP if (ch in UPDATED and UP) else BASE
    for d in (os.path.join(root, "chapter%d" % ch, "chapter%d" % ch),
              os.path.join(root, "chapter%d" % ch)):
        paths = glob.glob(os.path.join(d, "*.py"))
        if paths:
            return d, paths
    return None, []


def order(p):
    m = re.search(r"(\d+)", os.path.basename(p))
    return int(m.group(1)) if m else 0


res = {}
for ch in range(1, 13):
    d, paths = chapter_files(ch)
    if not paths:
        print("!! ch%d no files" % ch)
        continue
    for p in sorted(paths, key=order):
        name = os.path.basename(p)
        key = "ch%d/%s" % (ch, name)
        src = open(p, encoding="utf-8", errors="replace").read()
        stdin_text = STDIN.get((key.split("/")[0], name), "")

        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        env["MPLBACKEND"] = "Agg"
        # BASE 要在 sys.path 里：ch9/test3 用 `from chapter7.test19 import logit`
        path = [BASE, PROJ, d]
        if "turtle" in src:
            path.insert(0, TURTLE_STUB)   # 让 stub 抢在真实 turtle 之前
        path.append(TURTLE_STUB)          # ipywidgets 等缺失库的兜底
        env["PYTHONPATH"] = os.pathsep.join(path)

        work = tempfile.mkdtemp(prefix="run_%s_" % ch)
        # 章目录里自带的 .txt/.csv 是示例代码要读的数据，先搬进工作目录，
        # 否则 ch10 的 test7-test11 读不到 test.txt / demo.csv
        for data in glob.glob(os.path.join(d, "*.txt")) + glob.glob(os.path.join(d, "*.csv")):
            try:
                shutil.copy2(data, os.path.join(work, os.path.basename(data)))
            except OSError:
                pass
        # 绝对路径改写：在 work 目录里放一份改过的副本再跑，原始课件文件不动
        run_path, patched = p, ""
        for old, new in PATCH.get((key.split("/")[0], name), []):
            if patched:
                break
            if old in src:
                dst = os.path.join(work, "_patched_" + name)
                with open(dst, "w", encoding="utf-8") as fh:
                    fh.write(src.replace(old, new.replace("{work}", work)))
                run_path = dst
                patched = old + " -> " + new.replace("{work}", "<临时目录>")
                print("   PATCH %s: %s" % (key, patched))
        try:
            r = subprocess.run(
                [PY, run_path], capture_output=True, text=True, encoding="utf-8",
                errors="replace", env=env, timeout=40, input=stdin_text, cwd=work,
            )
            out = r.stdout.rstrip("\n")
            # stderr 里不全是错误：DeprecationWarning、jieba 的加载日志都会走这里。
            # 只有带 Traceback 头的才算真异常，其余当「运行提示」单独存。
            if "Traceback (most recent call last)" in r.stderr:
                err, warn = r.stderr.strip()[-900:], ""
            else:
                err, warn = "", r.stderr.strip()[-300:]
        except subprocess.TimeoutExpired:
            out, err, warn = "", "<<TIMEOUT>>", ""
        finally:
            shutil.rmtree(work, ignore_errors=True)

        res[key] = {"out": out, "err": err, "warn": warn, "stdin": stdin_text, "py": PY}
        if patched:
            res[key]["patched"] = patched
        flag = "ERR" if err else "OK "
        tail = err.splitlines()[-1][:70] if err else ""
        print("[%s] ch%-2d %-12s out=%-4d %s" % (flag, ch, name, len(out), tail))

out_path = os.path.join(PROJ, "python-quiz", "tools", "source", "newcode_runs.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("-> %s  (%d files)" % (out_path, len(res)))
