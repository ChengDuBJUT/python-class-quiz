# -*- coding: utf-8 -*-
"""从教材 docx 的 WordprocessingML 里精确提取每章判断题答案。

背景：教材判断题答案有两种印法——
  1. 符号字体（Wingdings 2）：`（1）-（5）√√×√√`，其中 √/× 是 <w:sym char="F050"/F04F>，
     经 docx→HTML→文本转换会整段丢失，看上去像"没印答案"；
  2. 纯文字：`对、对、对、对、错`。
两种都要认，所以直接读 document.xml，不经过任何中间转换。

输出 tools/source/judge_answers.json：{"1": "√√×√√", ..., "14": "×√×××√√"}
"""
import json
import os
import re
import zipfile
from xml.etree import ElementTree as ET

TOOLS = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TOOLS)
DOCX = os.path.join(os.path.dirname(BASE), 'Python编程基础与应用习题及答案.docx')
OUT = os.path.join(TOOLS, 'source', 'judge_answers.json')

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
# Wingdings 2：P(0x50)=√  O(0x4F)=×；个别文档会用 F0FC/F0FB
SYM_MAP = {'F050': '√', 'F04F': '×', 'F0FC': '√', 'F0FB': '×'}

RANGE_RE = re.compile(r'^[（(]\s*1\s*[）)]\s*[-－—~～]\s*[（(]\s*(\d+)\s*[）)]\s*([√×]+)$')
WORDS_RE = re.compile(r'^[对错](?:[、，,][对错])+$')
CH_RE = re.compile(r'^第\s*(\d+)\s*章')


def para_text(p):
    out = []
    for n in p.iter():
        tag = n.tag.split('}')[-1]
        if tag == 't':
            out.append(n.text or '')
        elif tag == 'sym':
            ch = (n.get(W + 'char') or '').upper()
            out.append(SYM_MAP.get(ch, ''))
        elif tag == 'tab':
            out.append('\t')
        elif tag in ('br', 'cr'):
            out.append('\n')
    return ''.join(out).replace('\xa0', ' ').strip()


def main():
    with zipfile.ZipFile(DOCX) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    body = root.find(W + 'body')

    truth = {}
    dup = {}
    chapter = 0
    for p in body.iter(W + 'p'):          # 含表格内段落，按文档顺序
        s = para_text(p)
        if not s:
            continue
        m = CH_RE.match(s)
        if m:
            chapter = int(m.group(1))
            continue
        if not chapter:
            continue
        m = RANGE_RE.match(s)
        if m:
            n, marks = int(m.group(1)), m.group(2)
            if len(marks) != n:
                print('!! 第%d章 判断题答案个数(%d)与题号范围(1-%d)不符: %s'
                      % (chapter, len(marks), n, marks))
            if chapter in truth and truth[chapter] != marks:
                dup[chapter] = (truth[chapter], marks)
            truth.setdefault(chapter, marks)
            continue
        if WORDS_RE.match(s):
            toks = [t for t in re.split(r'[、，,]', s) if t in ('对', '错')]
            marks = ''.join('√' if t == '对' else '×' for t in toks)
            if chapter in truth and truth[chapter] != marks:
                dup[chapter] = (truth[chapter], marks)
            truth.setdefault(chapter, marks)

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(truth, f, ensure_ascii=False, indent=2, sort_keys=True)

    print('提取到 %d 章判断题答案 → %s' % (len(truth), OUT))
    for c in sorted(truth, key=int):
        print('  第%-2s章  %s (%d)' % (c, truth[c], len(truth[c])))
    for c, (a, b) in dup.items():
        print('!! 第%s章 出现两种不同答案: %s vs %s（已取前者）' % (c, a, b))


if __name__ == '__main__':
    main()
