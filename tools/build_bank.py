# -*- coding: utf-8 -*-
"""把《Python编程基础与应用习题及答案.docx》导出的文本解析成题库 JSON。

输入:  ../../trial/quiz_lines.txt  (由 editor_sdk doc_convert_to_html 导出后逐行还原)
输出:  ../data/questions.json      (供 questions.js 包装)
       ../tools/diagnostics.txt  (解析体检报告)

注意：考试范围为第 1-12 章，故第 13/14 章不入库。
"""
import re
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'tools', 'source', 'quiz_lines.txt')
if not os.path.exists(SRC):
    SRC = os.path.join(os.path.dirname(BASE), 'trial', 'quiz_lines.txt')
OUT = os.path.join(BASE, 'data', 'questions.json')
DIAG = os.path.join(BASE, 'tools', 'diagnostics.txt')

MAX_CHAPTER = 12

CHAPTER_TITLES = {
    1: '绪论', 2: 'Python基础', 3: '数据类型', 4: '运算符',
    5: '流程控制', 6: '组合数据类型', 7: '函数', 8: '类与对象',
    9: '异常、调试与测试', 10: '文件与数据格式化', 11: '标准库应用编程',
    12: '第三方库应用编程',
}

TYPE_NAME = {
    '填空题': 'blank', '选择题': 'single', '判断题': 'judge',
    '简答题': 'short', '编程题': 'code',
}

# 原教材若干章的判断题答案整段空缺，这里按 Python 语义补齐，并在题目里标注来源。
JUDGE_OVERRIDE = {
    1: ['对', '对', '错', '对', '对'],
    2: ['对', '对', '错', '对', '对'],
    6: ['错', '错', '对', '错', '错'],
    7: ['错', '错', '错', '对', '对'],
    8: ['错', '错', '错', '对', '错'],
    11: ['对', '对', '错', '对', '对'],
    12: ['错', '错', '错', '对', '错'],
}

# 口径容易有分歧的判断题，给出解析说明
JUDGE_NOTE = {
    'ch2-judge-01': '.pyc 字节码与平台无关，由 Python 虚拟机解释执行；教材按此口径判「对」。',
    'ch7-judge-02': 'nonlocal 只能引用外层（非全局）作用域的变量；在函数内修改全局变量应使用 global。',
    'ch8-judge-05': '教材口径：实例方法由对象调用，类方法 / 静态方法才可由类或对象调用。技术上 Class.method(obj) 也能运行，但考试按教材表述判「错」。',
    'ch12-judge-03': 'jieba 是中文分词库，英文分词通常按空格或正则处理，教材未把它列为 jieba 的功能。',
}

# 教材答案明显与题面对不上时的人工校正（题号 -> 参考答案）
CODE_ANSWER_OVERRIDE = {}

CH_RE = re.compile(r'^第\s*(\d+)\s*章\s*(.*)$')
TYPE_RE = re.compile(
    r'^\s*(?:\d+\s*[\.．、]?\s*)?(填空题|选择题|判断题|简答题|编程题)\s*'
    r'[:：]?\s*(?:[（(]\s*略\s*[）)])?\s*$')
Q_RE = re.compile(r'^\s*[（(]\s*(\d+)\s*[）)]\s*(.*)$')
ANUM_RE = re.compile(r'[（(]\s*(\d+)\s*[）)]')
OPT_RE = re.compile(r'(?<![A-Za-z0-9_"\'])([A-D])\s*[\.．、:：]\s*')
PLACEHOLDER_RE = re.compile(r'\(\s*[　]+\s*\)\s*$')


def read_lines():
    with open(SRC, encoding='utf-8') as f:
        return [x.rstrip() for x in f.read().split('\n')]


def split_sections(lines):
    heads = []
    for i, ln in enumerate(lines):
        m = CH_RE.match(ln.strip())
        if m:
            kind = lines[i + 1].strip() if i + 1 < len(lines) else ''
            heads.append((i, int(m.group(1)), 'answer' if '答案' in kind else 'question'))
    out = []
    for k, (idx, ch, kind) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        out.append((ch, kind, lines[idx + 2:end]))
    return out


def split_types(body):
    cur = None
    out = {}
    for ln in body:
        m = TYPE_RE.match(ln.strip())
        if m:
            cur = m.group(1)
            out.setdefault(cur, [])
            continue
        if cur:
            out[cur].append(ln)
    return out


def split_questions(block):
    cur = None
    out = []
    for ln in block:
        if not ln.strip():
            if cur is not None:
                out[-1][1].append('')
            continue
        m = Q_RE.match(ln)
        if m:
            cur = int(m.group(1))
            out.append([cur, [m.group(2)]])
        elif cur is not None:
            out[-1][1].append(ln)
    for n, ls in out:
        while ls and not ls[-1].strip():
            ls.pop()
    return out


def clean(s):
    s = s.replace('\u00a0', ' ').replace('\u3000', ' ')
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()


def join_stem(ls, strip_placeholder=False):
    parts = []
    for x in ls:
        x = x.replace('\u00a0', ' ').replace('\t', '    ')
        if strip_placeholder:
            x = PLACEHOLDER_RE.sub('', x)
        parts.append(x.rstrip())
    while parts and not parts[0].strip():
        parts.pop(0)
    while parts and not parts[-1].strip():
        parts.pop()
    txt = '\n'.join(parts)
    txt = re.sub(r'\n{3,}', '\n\n', txt)
    return txt.strip()


def parse_options(raw):
    matches = list(OPT_RE.finditer(raw))
    start = None
    for i, m in enumerate(matches):
        if m.group(1) == 'A':
            start = i
            break
    if start is None:
        return clean(raw), []
    seq = matches[start:]
    stem = raw[:seq[0].start()]
    opts = []
    for i, m in enumerate(seq):
        end = seq[i + 1].start() if i + 1 < len(seq) else len(raw)
        txt = re.sub(r'\s*\n\s*', '\n', raw[m.end():end].strip())
        txt = '\n'.join(x.rstrip() for x in txt.split('\n')).strip()
        opts.append(txt)
    # 教材偶有重复字母（如第6章(2)出现两个 B），按出现顺序强制 A/B/C/D
    opts = [chr(ord('A') + i) + '. ' + t for i, t in enumerate(opts)]
    return join_stem(stem.split('\n')), opts


def parse_answer_letters(block, n):
    txt = ' '.join(clean(x) for x in block)
    txt = re.sub(r'[（(]\s*\d+\s*[）)]', ' ', txt)   # 去掉 "（1）-（5）" 之类编号
    letters = re.findall(r'[A-D]', txt)
    return letters[:n] if len(letters) >= n else None


def parse_answer_judge(block, n):
    txt = ' '.join(clean(x) for x in block)
    vals = re.findall(r'(对|错|正确|错误|√|×|T|F|Y|N)', txt)
    vals = [('对' if v in ('对', '正确', '√', 'T', 'Y') else '错') for v in vals]
    return vals[:n] if len(vals) >= n else None


def parse_numbered_answers(block):
    """按出现顺序切分 （N） 答案。

    教材第 2/13/14 章答案编号是错乱的（(1)(2)(1)(1)(2)…），
    但顺序与题号一致，因此一律按出现次序而非印刷编号对应。
    """
    text = '\n'.join(block)
    marks = list(ANUM_RE.finditer(text))
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        val = re.sub(r'^[:：\s]+', '', text[m.end():end].strip())
        out.append(val)
    return {i + 1: v for i, v in enumerate(out)}


def parse_code_answers(block):
    """编程题参考答案：同样按出现顺序切分，段内保留代码缩进。"""
    buckets = []
    cur = None
    for ln in block:
        m = Q_RE.match(ln)
        m2 = None if m else re.match(
            r'^\s*(\d+)\s*[\.．、]\s*参考(?:程序|代码|答案)\s*[:：]?\s*(.*)$', ln)
        if m or m2:
            if m:
                tail = m.group(2).strip()
            else:
                tail = m2.group(2).strip()
            tail = re.sub(r'^参考(?:程序|代码|答案)\s*[:：]?\s*', '', tail)
            buckets.append([])
            cur = buckets[-1]
            if tail and tail not in ('：', ':'):
                cur.append(tail)
            continue
        if cur is not None:
            cur.append(ln)
    out = {}
    for i, b in enumerate(buckets):
        while b and not b[0].strip():
            b.pop(0)
        while b and not b[-1].strip():
            b.pop()
        out[i + 1] = '\n'.join(b).strip()
    return out


def blank_variants(s):
    """为填空题生成可接受的等价写法，便于自动判分。"""
    out = []
    def add(x):
        x = x.strip()
        if x and x not in out:
            out.append(x)
    add(s)
    add(s.replace(' ', '').replace('\u3000', ''))
    add(s.lower())
    add(s.replace('（', '(').replace('）', ')'))
    compact = re.sub(r'[，,、；;。\s]+', '', s)
    add(compact)
    parts = [p for p in re.split(r'[，,、；;或/]+', s) if p.strip()]
    if len(parts) > 1:
        add(' '.join(p.strip() for p in parts))
        add(','.join(p.strip() for p in parts))
        add('；'.join(p.strip() for p in parts))
    if '()' in s:
        add(s.replace('()', ''))
    if s.startswith('.'):
        add(s[1:])
    for q in ["'", '"', '‘', '’', '“', '”']:
        if q in s:
            add(s.replace(q, ''))
    return out


def main():
    lines = read_lines()
    sections = split_sections(lines)
    qs, ans = {}, {}
    for ch, kind, body in sections:
        if ch > MAX_CHAPTER:
            continue
        store = ans if kind == 'answer' else qs
        store.setdefault(ch, {})
        for tcn, blk in split_types(body).items():
            store[ch][tcn] = blk

    diag = []
    bank = []
    for ch in sorted(qs):
        for tcn, blk in qs[ch].items():
            qlist = split_questions(blk)
            ablk = ans.get(ch, {}).get(tcn, [])
            if tcn == '选择题':
                letters = parse_answer_letters(ablk, len(qlist))
            elif tcn == '判断题':
                judges = parse_answer_judge(ablk, len(qlist))
                used_override = judges is None
                if used_override:
                    judges = JUDGE_OVERRIDE.get(ch)
            elif tcn == '编程题':
                codeans = parse_code_answers(ablk)
            else:
                numans = parse_numbered_answers(ablk)

            diag.append('第%d章 %s: 题数=%d' % (ch, tcn, len(qlist)))
            if tcn == '选择题':
                diag.append('   答案: %s' % (letters,))
            elif tcn == '判断题':
                diag.append('   答案: %s%s' % (judges, ' [人工补齐]' if used_override else ''))
            elif tcn == '编程题':
                diag.append('   参考答案段数: %d' % len(codeans))
            else:
                diag.append('   答案段数: %d' % len(numans))

            for num, ls in qlist:
                qid = 'ch%d-%s-%02d' % (ch, TYPE_NAME[tcn], num)
                raw = join_stem(ls, strip_placeholder=(tcn == '判断题'))
                exam = (tcn in ('选择题', '填空题') and ch <= 12) or \
                       (tcn == '编程题' and ch <= 8)
                item = {
                    'id': qid,
                    'chapter': ch,
                    'chapterTitle': CHAPTER_TITLES.get(ch, ''),
                    'type': TYPE_NAME[tcn],
                    'exam': exam,
                    'sourceKind': '教材习题',
                    'sourceFile': 'Python编程基础与应用习题及答案.docx',
                    'sourceLocator': '第%d章 习题 %s (%d)' % (ch, tcn, num),
                }
                if tcn == '选择题':
                    stem, opts = parse_options(raw)
                    item['stem'] = stem
                    item['options'] = opts
                    item['answer'] = letters[num - 1] if letters and num <= len(letters) else None
                    if not opts:
                        diag.append('   !! %s 未解析出选项' % qid)
                elif tcn == '判断题':
                    item['stem'] = raw
                    item['answer'] = ('对' if judges[num - 1] == '对' else '错') \
                        if judges and num <= len(judges) else None
                    if used_override:
                        item['answerNote'] = '教材本节未印出判断题答案，此答案按 Python 语义与教材口径补齐，建议与任课教师核对。'
                    if qid in JUDGE_NOTE:
                        item['explanation'] = JUDGE_NOTE[qid]
                elif tcn == '填空题':
                    item['stem'] = raw
                    a = numans.get(num, '').strip()
                    item['answer'] = blank_variants(a) if a else []
                    item['answerText'] = a
                    blanks = len(re.findall(r'_{3,}', raw))
                    if blanks > 1:
                        item['explanation'] = ('本题共 %d 个空，请按题目顺序把各空答案写在同一行，'
                                               '用空格、逗号或分号分隔。' % blanks)
                    if not a:
                        diag.append('   !! %s 缺答案' % qid)
                elif tcn == '简答题':
                    item['stem'] = raw
                    a = numans.get(num, '').strip()
                    item['answer'] = a if a and a != '略' else '（教材未给出参考答案，请对照课件自行作答）'
                else:
                    item['stem'] = raw
                    item['answer'] = CODE_ANSWER_OVERRIDE.get(qid, codeans.get(num, ''))
                    if not item['answer']:
                        item['answer'] = '（教材未给出本题参考程序）'
                bank.append(item)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)
    with open(DIAG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(diag))
    print('questions:', len(bank), '->', OUT)


if __name__ == '__main__':
    main()
