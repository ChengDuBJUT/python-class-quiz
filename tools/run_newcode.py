# -*- coding: utf-8 -*-
"""运行「更新后的chapter」ch4-8 代码，收集真实输出，用于生成代码学习卡。"""
import os, glob, subprocess, sys, json, re

PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(PROJ, "pythonProject-2025")

# 找到「更新后的chapter」目录（避免源码里出现中文变量名带来的编码问题）
UP = None
for name in os.listdir(BASE):
    p = os.path.join(BASE, name)
    if os.path.isdir(p) and name.startswith("\u66f4") and "chapter" in name.lower():
        UP = p
        break
if UP is None:
    for name in os.listdir(BASE):
        p = os.path.join(BASE, name)
        if os.path.isdir(p) and name.startswith("\u66f4"):
            UP = p
            break
print("UP =", UP)

# 需要交互输入的代码，给定测试输入
STDIN = {
    ("ch5", "test1.py"): "3\n",
    ("ch5", "test8.py"): "4\n",
    ("ch4", "test4.py"): "8\n3\n",
    ("ch7", "test13.py"): "5\n",
    ("ch7", "test14.py"): "5\n",
}

env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"

res = {}
for ch in [4, 5, 6, 7, 8]:
    d = os.path.join(UP, "chapter%d" % ch, "chapter%d" % ch)
    paths = glob.glob(os.path.join(d, "*.py"))

    def key(p):
        m = re.search(r"(\d+)", os.path.basename(p))
        return int(m.group(1)) if m else 0

    for p in sorted(paths, key=key):
        name = os.path.basename(p)
        stdin_text = STDIN.get(("ch%d" % ch, name), "")
        try:
            r = subprocess.run(
                [sys.executable, p],
                capture_output=True, text=True, encoding="utf-8",
                env=env, timeout=25, input=stdin_text,
            )
            out, err = r.stdout.rstrip("\n"), r.stderr.strip()[-300:]
        except subprocess.TimeoutExpired:
            out, err = "", "<<TIMEOUT>>"
        res["ch%d/%s" % (ch, name)] = {"out": out, "err": err, "stdin": stdin_text}
        print("[%s] ch%d/%-12s out=%-4d %s" % ("ERR" if err else "OK ", ch, name, len(out), err[:70]))

out_path = os.path.join(PROJ, "python-quiz", "tools", "source", "newcode_runs.json")
json.dump(res, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("-> %s  (%d files)" % (out_path, len(res)))
