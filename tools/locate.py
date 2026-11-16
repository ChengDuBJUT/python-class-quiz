# -*- coding: utf-8 -*-
"""为每道简答题在对应章节课件里定位最相关的页，供人工/模型组织答案。

用法:
  python locate.py            # 输出每题 top3 候选页页码
  python locate.py --dump 2   # 输出第2章每题候选页的原文全文
  python locate.py --dump-all > all.txt
"""
import re, sys, os, glob, json

HERE = os.path.dirname(os.path.abspath(__file__))
TXT = os.path.join(HERE, "source", "ppt_txt")

# 简答题题干（与题库一致）
STEMS = json.load(open(os.path.join(HERE, "source", "short_stems.json"), encoding="utf-8"))

STOP = set("""简述 请 说明 介绍 什么 哪些 几个 几种 如何 怎么 怎样 为什 么样 的 了 是 有 和 与 及 或
以及 分别 简单 主要 一般 中 在 对 请写 出 列举 说出 应该 可以 需要 一个 我们 你 他 它 这 那
Python python 中 时 要 会 能 所 其 该 各 种 类 用法 作用 功能 含义 特点 规则 方法 方式 过程""".split())

CJK = re.compile(r"[\u4e00-\u9fff]+")
EN = re.compile(r"[A-Za-z_][A-Za-z0-9_\.]*")
PAGE_RE = re.compile(r"===== \[ch(\d+) p(\d+)\] =====")


def load_pages(ch):
    path = os.path.join(TXT, f"ch{ch}.txt")
    if not os.path.exists(path):
        return []
    raw = open(path, encoding="utf-8").read()
    parts = PAGE_RE.split(raw)
    pages = []
    # parts: ['', ch, p, text, ch, p, text, ...]
    for i in range(1, len(parts), 3):
        pages.append((int(parts[i + 1]), parts[i + 2]))
    return pages


def grams(text):
    """中文 2-gram + 英文词 + 中文 3-gram"""
    g = set()
    for run in CJK.findall(text):
        for n in (2, 3):
            for i in range(len(run) - n + 1):
                w = run[i:i + n]
                if w in STOP:
                    continue
                if all(c in "的了是在和与及或请简述说明" for c in w):
                    continue
                g.add(w)
    for w in EN.findall(text):
        w = w.lower()
        if len(w) >= 2 and w not in ("py", "python"):
            g.add(w)
    return g


def score(stem, page_text):
    gs = grams(stem)
    if not gs:
        return 0.0
    hit = 0
    for g in gs:
        if g in page_text:
            hit += len(g)  # 长 gram 命中权重更高
    # 归一：避免长页占优
    return hit / (1 + 0.02 * len(page_text) ** 0.5)


def locate_all():
    out = {}
    cache = {}
    for q in STEMS:
        ch = int(re.search(r"ch(\d+)-", q["id"]).group(1))
        if ch not in cache:
            cache[ch] = load_pages(ch)
        pages = cache[ch]
        ranked = sorted(pages, key=lambda pp: -score(q["stem"], pp[1]))[:3]
        out[q["id"]] = [(p, round(score(q["stem"], t), 2)) for p, t in ranked]
    return out


def main():
    res = locate_all()
    win = 0
    if "--window" in sys.argv:
        win = int(sys.argv[sys.argv.index("--window") + 1])
    if "--pages" in sys.argv:
        spec = sys.argv[sys.argv.index("--pages") + 1]  # e.g. 1:48-52
        ch, rng = spec.split(":")
        a, b = (int(x) for x in rng.split("-"))
        pages = dict(load_pages(int(ch)))
        for p in range(a, b + 1):
            print(f"\n----- [ch{ch} p{p}] -----")
            print(pages.get(p, "").strip())
        return
    if "--dump" in sys.argv:
        ch = int(sys.argv[sys.argv.index("--dump") + 1])
        pages = dict(load_pages(ch))
        for q in STEMS:
            if not q["id"].startswith(f"ch{ch}-"):
                continue
            print("\n" + "#" * 70)
            print(f"# {q['id']}  {q['stem']}")
            print("# 候选页:", [p for p, _ in res[q["id"]]])
            print("#" * 70)
            want = []
            for p, _ in res[q["id"]]:
                for k in range(p - win, p + win + 1):
                    if k not in want:
                        want.append(k)
            for p in sorted(want):
                print(f"\n----- [ch{ch} p{p}] -----")
                print(pages.get(p, "").strip())
        return
    if "--dump-all" in sys.argv:
        for ch in range(1, 13):
            pages = dict(load_pages(ch))
            for q in STEMS:
                if not q["id"].startswith(f"ch{ch}-"):
                    continue
                print("\n" + "#" * 70)
                print(f"# {q['id']}  {q['stem']}")
                print("# 候选页:", [p for p, _ in res[q["id"]]])
                print("#" * 70)
                for p, _ in res[q["id"]]:
                    print(f"\n----- [ch{ch} p{p}] -----")
                    print(pages.get(p, "").strip())
        return
    for q in STEMS:
        print(q["id"], "|", q["stem"])
        print("   ->", res[q["id"]])


if __name__ == "__main__":
    main()
