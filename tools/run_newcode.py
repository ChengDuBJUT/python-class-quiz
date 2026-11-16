# -*- coding: utf-8 -*-
"""跑全部 12 章的示例代码，收集真实输出，用于生成代码学习卡。

第 4-8 章取「更新后的chapter」，其余章取原目录；每章兼容
`chapterN/chapterN/*.py` 与 `chapterN/*.py` 两种结构。

几个必要的处理：
- turtle 程序没有控制台输出，用临时 stub（记录绘图指令）跑，得到"绘图轨迹"
- matplotlib 程序切 Agg 后端，避免 plt.show() 阻塞
- 需要键盘输入的按 STDIN 表喂输入
- 每个文件在独立临时目录里跑，避免 polluting 课程目录（如 chapter10 会写 demo.csv）
- PYTHONPATH 带上 PROJ，让 `import chapter7.xxx` 这类跨章导入能解析
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

UPDATED = {4, 5, 6, 7, 8}

STDIN = {
    ("ch4", "test4.py"): "8\n3\n",
    ("ch5", "test1.py"): "3\n",
    ("ch5", "test8.py"): "4\n",
    ("ch7", "test13.py"): "5\n",
    ("ch7", "test14.py"): "5\n",
    ("ch3", "test3.py"): "张三\n18\n90\n",
    ("ch3", "test14.py"): "1\n",
    ("ch9", "test4.py"): "张三\n",
    ("ch9", "test5.py"): "2\n3\n",
    ("ch9", "test7.py"): "5\n",
    ("ch9", "test11.py"): "张三\n",
    ("ch9", "test13.py"): "7\n",
    ("ch11", "test3.py"): "hello.txt\n",
    ("ch12", "test8.py"): "张三\n",
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
        path = [PROJ, d]
        if "turtle" in src:
            path.insert(0, TURTLE_STUB)   # 让 stub 抢在真实 turtle 之前
        path.append(TURTLE_STUB)          # ipywidgets 等缺失库的兜底
        env["PYTHONPATH"] = os.pathsep.join(path)

        work = tempfile.mkdtemp(prefix="run_%s_" % ch)
        try:
            r = subprocess.run(
                [PY, p], capture_output=True, text=True, encoding="utf-8",
                errors="replace", env=env, timeout=40, input=stdin_text, cwd=work,
            )
            out, err = r.stdout.rstrip("\n"), r.stderr.strip()[-300:]
        except subprocess.TimeoutExpired:
            out, err = "", "<<TIMEOUT>>"
        finally:
            shutil.rmtree(work, ignore_errors=True)

        res[key] = {"out": out, "err": err, "stdin": stdin_text, "py": PY}
        flag = "ERR" if err else "OK "
        tail = err.splitlines()[-1][:70] if err else ""
        print("[%s] ch%-2d %-12s out=%-4d %s" % (flag, ch, name, len(out), tail))

out_path = os.path.join(PROJ, "python-quiz", "tools", "source", "newcode_runs.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("-> %s  (%d files)" % (out_path, len(res)))
