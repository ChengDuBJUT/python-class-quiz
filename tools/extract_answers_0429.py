# -*- coding: utf-8 -*-
"""从《1-12习题答案0429-勘误后.docx》提取权威答案表。

为什么单独写一个脚本：
- 判断题答案在 docx 里是 Wingdings 2 符号节点 <w:sym>，docx→HTML→文本 会整段丢失；
- 勘误版把改动的答案标成了红色（FF0000），红字既是「新答案」也是「批注」，
  需要按 run 记录颜色才能分清。

输出 tools/source/answers_0429.json：
  {"1": {"fill": {"1": ".py", ...}, "choice": ["A","B","C","D","C"],
         "judge": "√√×√√", "red": ["..."]}, ...}

用法：python3 extract_answers_0429.py
"""
import json
import os
import re
import zipfile
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
SYM = {'F050': '√', 'F04F': '×', 'F0FC': '√', 'F0FB': '×'}
RED = {'FF0000', 'C00000', 'FF3333'}

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX = os.path.join(os.path.dirname(BASE), '1-12习题答案0429-勘误后.docx')
OUT = os.path.join(BASE, 'tools', 'source', 'answers_0429.json')

# 勘误版里有 2 处填空答案把「批注」和「答案」写在同一行，需要人工剥离。
# 键为 (章, 题号)，值为 (最终答案, 说明)。
FILL_FIX = {
    (3, 5): ('j / j', '原答案只写了 1 个 j；题干有 2 个空（虚部后缀 j，且 j 不区分大小写），两空都填 j。'),
    (4, 4): ('False', "勘误版原文：「False y'< 'x' ==False会被解析为('y' < 'x') and ('x' == False)」，"
                      '其中后半句是批注，答案只有 False。'),
}

# 题型标题三种写法都有：「1. 填空题」「1填空题」「填空题」（第 8 章）
# 简答/编程题也要认出来，否则正文会被并进上一题型，答案串变长。
TYPE_RE = re.compile(r'^(?:\d+\s*[.．、]?\s*)?(填空题|选择题|判断题|简答题|编程题)\s*[:：]?\s*$')
ANUM_RE = re.compile(r'[（(]\s*(\d+)\s*[）)]')


def paragraphs(path):
    """逐段返回 [(文本, [(字符, 是否红色), ...]), ...]，符号节点还原成 √/×。"""
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read('word/document.xml'))
    body = root.find(W + 'body')
    out = []

    def walk(p):
        chars = []
        for r in p.iter(W + 'r'):
            col = None
            rpr = r.find(W + 'rPr')
            if rpr is not None:
                c = rpr.find(W + 'color')
                if c is not None:
                    col = (c.get(W + 'val') or '').upper()
            for n in r.iter():
                tag = n.tag.split('}')[-1]
                t = None
                if tag == 't':
                    t = n.text or ''
                elif tag == 'sym':
                    t = SYM.get((n.get(W + 'char') or '').upper(), '')
                elif tag == 'tab':
                    t = '\t'
                if t:
                    for ch in t:
                        chars.append((ch, col in RED))
        return chars

    for child in body:
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            cs = walk(child)
            if cs:
                out.append(cs)
        elif tag == 'tbl':
            for p in child.iter(W + 'p'):
                cs = walk(p)
                if cs:
                    out.append(cs)
    return out


def parse(path):
    res = {}
    ch = 0
    in_ans = False
    sec = ''
    for cs in paragraphs(path):
        txt = ''.join(c for c, _ in cs).replace('\xa0', ' ').strip()
        if not txt:
            continue
        m = re.match(r'^第\s*(\d+)\s*章', txt)
        if m:
            ch = int(m.group(1))
            in_ans = False
            sec = ''
            continue
        if txt.startswith('习题答案'):
            in_ans = True
            continue
        mt = TYPE_RE.match(txt)
        if mt:
            sec = mt.group(1)
            continue
        if not (ch and in_ans and sec):
            continue
        d = res.setdefault(ch, {'fill_raw': [], 'choice_raw': [], 'judge_raw': []})
        if sec == '填空题':
            d['fill_raw'].append(txt)
        elif sec == '选择题':
            d['choice_raw'].append(txt)
        elif sec == '判断题':
            d['judge_raw'].append(txt)
        red = ''.join(c for c, r in cs if r).strip()
        if red:
            d.setdefault('red', []).append({'section': sec, 'text': txt, 'red': red})

    out = {}
    for ch, d in sorted(res.items()):
        item = {}
        # 填空：按 （N） 出现顺序切分
        text = '\n'.join(d['fill_raw'])
        marks = list(ANUM_RE.finditer(text))
        fill = {}
        for i, m in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
            val = re.sub(r'^[:：\s]+', '', text[m.end():end].strip())
            if val:
                fill[str(i + 1)] = val
        for (c, n), (val, note) in FILL_FIX.items():
            if c == ch:
                fill[str(n)] = val
                item.setdefault('notes', []).append({'no': n, 'answer': val, 'note': note})
        item['fill'] = fill

        # 选择：去掉「（1）-（5）」后取字母。
        # 勘误版会在答案后跟红字批注（如「CD均正确」「print（c）」），批注里的字母会混进来，
        # 而各章客观题都是 5 道，故只取前 5 个字母。
        t = ' '.join(d['choice_raw'])
        t = re.sub(r'[（(]\s*1\s*[）)]\s*-\s*[（(]\s*\d+\s*[）)]', ' ', t)
        t = re.sub(r'[（(]\s*\d+\s*[）)]', ' ', t)
        item['choice'] = re.findall(r'[A-D]', t)[:5]

        # 判断：对/错 与 √/× 统一成 √/×
        j = ' '.join(d['judge_raw']).replace('对', '√').replace('错', '×')
        item['judge'] = ''.join(re.findall(r'[√×]', j))

        if d.get('red'):
            item['red'] = d['red']
        out[str(ch)] = item
    return out


def main():
    if not os.path.exists(DOCX):
        raise SystemExit('缺少勘误版文档：%s' % DOCX)
    data = parse(DOCX)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('chapters:', sorted(data, key=int))
    for ch in sorted(data, key=int):
        d = data[ch]
        print('ch%-2s 填空%-2d 选择%s 判断%s%s' % (
            ch, len(d['fill']), ''.join(d['choice']), d['judge'],
            '  红批注%d处' % len(d['red']) if d.get('red') else ''))
    print('->', OUT)


if __name__ == '__main__':
    main()
