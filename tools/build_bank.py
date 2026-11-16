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
JUDGE_TRUTH = os.path.join(BASE, 'tools', 'source', 'judge_answers.json')
ANSWERS_0429 = os.path.join(BASE, 'tools', 'source', 'answers_0429.json')
SHORT_ANS_PATH = os.path.join(BASE, 'tools', 'source', 'short_answers.json')
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

# 编程题的考试范围：第 1-8 章 + 第 10 章（文件读写必考一道）。
# 第 9 章（异常）、第 11 章（标准库）、第 12 章（第三方库）编程题按考纲不考。
EXAM_CODE_CHAPS = {1, 2, 3, 4, 5, 6, 7, 8, 10}

# 判断题答案：教材用两种印法（Wingdings 符号串 / 对、对、……），符号串经
# docx→HTML→文本转换会整段丢失，所以答案一律以 extract_judge_truth.py 从
# document.xml 直接提取的权威表为准，文本解析结果只用来交叉校验。
def load_judge_truth():
    if not os.path.exists(JUDGE_TRUTH):
        return {}
    with open(JUDGE_TRUTH, encoding='utf-8') as f:
        raw = json.load(f)
    return {int(k): v for k, v in raw.items()}


JUDGE_TRUTH_MAP = load_judge_truth()


def load_answers_0429():
    """教师 0429 勘误版（1-12 章）的权威客观题答案。

    原版里有 2 处填空、6 处选择、3 处判断印错，勘误版已改正；
    勘误版只有 1-12 章，且不含简答/编程题，故只覆盖客观题。
    """
    if not os.path.exists(ANSWERS_0429):
        return {}
    with open(ANSWERS_0429, encoding='utf-8') as f:
        raw = json.load(f)
    return {int(k): v for k, v in raw.items()}


AUTH_0429 = load_answers_0429()


def load_short_answers():
    """简答题参考答案：教材答案区多为「略」，这里用
    ① 教材/习题答案区原文（origin=official）
    ② 依据课件（教材正文 PDF）对应知识点提炼（origin=ppt，带页码可溯源）
    两者合成，键为题目 id。"""
    if not os.path.exists(SHORT_ANS_PATH):
        return {}
    with open(SHORT_ANS_PATH, encoding='utf-8') as f:
        raw = json.load(f)
    return {k: v for k, v in raw.items() if not k.startswith('_')}


SHORT_ANS = load_short_answers()

# 口径容易有分歧、或教材答案与 Python 语义不一致的判断题，给出解析说明
JUDGE_NOTE = {
    'ch2-judge-01': '.pyc 字节码与平台无关，由 Python 虚拟机解释执行；教材按此口径判「对」。',
    'ch7-judge-01': 'def 只是把函数对象绑定到名字，函数体要等到调用时才执行，这句应为「错」。'
                    '原版答案印作「对」，0429 勘误版已改正为「错」。',
    'ch7-judge-02': 'nonlocal 只能引用外层（非全局）作用域的变量；在函数内修改全局变量应使用 global。',
    'ch8-judge-01': 'Python 允许子类重写（override）从父类继承的方法，这正是多态的基础，这句应为「错」。'
                    '原版答案印作「对」，0429 勘误版已改正为「错」。',
    'ch8-judge-05': '教材口径：实例方法由对象调用，类方法 / 静态方法才可由类名直接调用。'
                    'Class.method(obj) 技术上能跑通，但按教材表述这句判「错」（0429 勘误版亦判错）。',
    'ch12-judge-03': '教材答案判「对」：jieba 主要做中文分词，但对英文串也能切分（效果一般）；'
                     '英文分词通常还是用 nltk / spaCy。',
}

# 0429 勘误版改动过的题目，逐题写清「原来印什么、为什么改」
ERRATA_NOTE = {
    'ch3-blank-05': '题干有两个空（虚部后缀、且该后缀不区分大小写），两个空都填 j，'
                    '可写成「j / j」或「j，j」。原答案只印了 1 个 j，0429 勘误版补成 j—j。',
    'ch4-blank-04': "Python 的比较运算符支持链式写法：'y'<'x' == False 等价于 "
                    "('y'<'x') and ('x'==False)，即 False and False，结果是 False。"
                    '原版答案印作 True，0429 勘误版已改为 False。',
    'ch2-single-04': 'Python 先把源程序编译成字节码，再由 Python 虚拟机解释执行，'
                     '所以「包含了提前编译的解释执行」是正确描述。原答案序列印作 B 并标红，'
                     '同页红字批注给出 A 并说明理由，本题按批注采用 A；建议考前与老师确认。',
    'ch5-single-03': '勘误版批注：本题 C、D 两个选项的文字完全相同（都是 1,2,3,4,5,），'
                     '教材也注明 CD 答案一样、CD 均正确。',
    'ch5-single-04': '勘误版批注：本题题干可能漏印了 print(c)。按现有代码，'
                     '条件 a>b 不成立，走 else 分支执行 print(a+b)，输出 3。',
    'ch7-single-04': '关键字参数按「形参=实参」传递，即 func(a=1, b=2)。'
                     'C 的 func(a=b=1) 是非法写法，原版答案印作 C，0429 勘误版已改为 B。',
    'ch8-single-04': '只能由对象调用的是对象方法（实例方法）。'
                     '类方法、静态方法都能用类名调用；析构方法由系统在对象销毁时自动调用。'
                     '原版答案印作 D，0429 勘误版已改为 B。',
    'ch9-single-01': 'raise 的三种写法是：raise 异常类名、raise 异常对象、raise（不带参数），'
                     '没有「raise 方法名」这种用法。原版答案印作 A，0429 勘误版已改为 C。',
    'ch9-single-03': 'except 子句不写异常类型时才捕获所有异常（D 正确）；'
                     'try 只是划定受监控的语句，真正捕获异常的是 except。'
                     '原版答案印作 C，0429 勘误版已改为 D。',
    'ch12-single-03': 'Matplotlib 的常用色彩模式是 RGB / RGBA、灰度（gray）等，'
                      '「全真模式」不是它的色彩模式（CMYK 主要用于印刷）。'
                      '原版答案印作 A，0429 勘误版已改为 B。',
}

# 0429 勘误版里答案序列与红字批注互相矛盾的一题：序列仍印 B（并标红），
# 同页批注写「4.python源程序的执行方式——A 包含了提前编译解释执行」。
# 按批注采用 A，解析里注明分歧。
CHOICE_OVERRIDE = {
    'ch2-single-04': 'A',
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


# docx 原文里的印误，抽取时统一纠正（原书第9章 选择题(4) 的选项 B 印成了 excepy）
TYPO_FIX = {
    'excepy': 'except',
}


def fix_typo(txt):
    for bad_s, good_s in TYPO_FIX.items():
        txt = re.sub(r'(?<![A-Za-z_])' + bad_s + r'(?![A-Za-z_])', good_s, txt)
    return txt


def parse_options(raw):
    raw = fix_typo(raw)
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
    # 抽空的片段一律丢掉：docx 里有些选项会被行内分隔符（", " / "and "）切碎，
    # 留下只有标点的空串（第8章选择题(5) 曾经因此多出 B、F 两个空选项，答案字母也错位）。
    opts = [t for t in opts if re.sub(r'[\s\.．、:：]', '', t)]
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
            letters = judges = numans = codeans = None
            if tcn == '选择题':
                letters = parse_answer_letters(ablk, len(qlist))
            elif tcn == '判断题':
                parsed = parse_answer_judge(ablk, len(qlist))
                truth = JUDGE_TRUTH_MAP.get(ch)
                if truth:
                    judges = ['对' if c == '√' else '错' for c in truth]
                    if parsed and parsed != judges:
                        diag.append('   !! 第%d章 判断题：文本解析 %s 与教材原文 %s 不一致，以原文为准'
                                    % (ch, ''.join(parsed), truth))
                    if len(judges) < len(qlist):
                        diag.append('   !! 第%d章 判断题：答案 %d 个，题目 %d 道'
                                    % (ch, len(judges), len(qlist)))
                else:
                    judges = parsed
                    if not judges:
                        diag.append('   !! 第%d章 判断题：教材与文本均未取到答案' % ch)
            elif tcn == '编程题':
                codeans = parse_code_answers(ablk)
            else:
                numans = parse_numbered_answers(ablk)

            # —— 教师 0429 勘误版优先（1-12 章客观题）——
            auth = AUTH_0429.get(ch, {})
            if tcn == '选择题' and auth.get('choice'):
                auth_letters = auth['choice']
                if letters and letters != auth_letters:
                    diag.append('   !! 第%d章 选择题：原版 %s → 勘误版 %s'
                                % (ch, ''.join(letters), ''.join(auth_letters)))
                letters = auth_letters
            elif tcn == '判断题' and auth.get('judge'):
                auth_judges = ['对' if c == '√' else '错' for c in auth['judge']]
                if judges and judges != auth_judges:
                    diag.append('   !! 第%d章 判断题：原版 %s → 勘误版 %s'
                                % (ch, ''.join(judges), auth['judge']))
                judges = auth_judges
            elif tcn == '填空题' and auth.get('fill'):
                # 第 2、11 章的填空答案在原文里就缺了 (3)-(5) 的编号，解析出来只有 2 段，
                # 这种情况下无法逐题对齐，跳过覆盖（否则会把 (3)(4)(5) 的答案并进 (2)）。
                if len(auth['fill']) >= len(qlist):
                    for k in sorted(auth['fill'], key=int):
                        n = int(k)
                        old = (numans or {}).get(n, '').strip()
                        new = auth['fill'][k].strip()
                        if old != new:
                            diag.append('   !! 第%d章 填空(%d)：原版 %r → 勘误版 %r' % (ch, n, old, new))
                            numans[n] = new
                else:
                    diag.append('   !! 第%d章 填空题：勘误版只解析出 %d 段（题 %d 道），无法逐题对齐，保持原解析'
                                % (ch, len(auth['fill']), len(qlist)))

            diag.append('第%d章 %s: 题数=%d' % (ch, tcn, len(qlist)))
            if tcn == '选择题':
                diag.append('   答案: %s' % (letters,))
            elif tcn == '判断题':
                diag.append('   答案: %s%s' % (judges, ' [教材原文]' if JUDGE_TRUTH_MAP.get(ch) else ''))
            elif tcn == '编程题':
                diag.append('   参考答案段数: %d' % len(codeans))
            else:
                diag.append('   答案段数: %d' % len(numans))

            for num, ls in qlist:
                qid = 'ch%d-%s-%02d' % (ch, TYPE_NAME[tcn], num)
                raw = join_stem(ls, strip_placeholder=(tcn == '判断题'))
                # 2026-11 老师公布的新考纲：范围 1-12 章；
                # 简答题并入填空题、判断题并入选择题 → 四类都是考试题型；
                # 编程题只考第 1-8 章 + 第 10 章（明确"必考一道文件"），
                # 第 9/11/12 章编程不考（这 22 道留作复习拓展）。
                exam = tcn in ('选择题', '判断题', '填空题', '简答题') or \
                       (tcn == '编程题' and ch in EXAM_CODE_CHAPS)
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
                    item['answer'] = CHOICE_OVERRIDE.get(
                        qid,
                        letters[num - 1] if letters and num <= len(letters) else None)
                    if not opts:
                        diag.append('   !! %s 未解析出选项' % qid)
                elif tcn == '判断题':
                    item['stem'] = raw
                    item['answer'] = ('对' if judges[num - 1] == '对' else '错') \
                        if judges and num <= len(judges) else None
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
                    extra = SHORT_ANS.get(qid)
                    if extra and extra.get('answerText'):
                        item['answer'] = extra['answerText']
                        if extra.get('basis'):
                            item['basis'] = extra['basis']
                        if extra.get('origin'):
                            item['answerOrigin'] = extra['origin']
                    else:
                        item['answer'] = a if a and a != '略' else '（教材未给出参考答案）'
                else:
                    item['stem'] = raw
                    item['answer'] = CODE_ANSWER_OVERRIDE.get(qid, codeans.get(num, ''))
                    if not item['answer']:
                        item['answer'] = '（教材未给出本题参考程序）'
                note = ERRATA_NOTE.get(qid)
                if note:
                    item['explanation'] = ('%s\n%s' % (item['explanation'], note)
                                           if item.get('explanation') else note)
                bank.append(item)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)
    with open(DIAG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(diag))
    print('questions:', len(bank), '->', OUT)


if __name__ == '__main__':
    main()
