# -*- coding: utf-8 -*-
"""在参考站 app.js 的基础上打补丁（保留其已验证的答题/判分/进度逻辑）。"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE, 'app.js')

PATCHES = []

def P(name, old, new, count=1):
    PATCHES.append((name, old, new, count))


P('存储键与题型', """  var STORAGE_KEY = 'mvstats-quiz-v1';
  var TYPE_LABEL = {
    single: '单选',
    multi: '多选（全对才得分）',
    judge: '判断',
    blank: '填空',
    short: '简答',
    case: '案例分析'
  };
  var OBJECTIVE = { single: 1, multi: 1, judge: 1, blank: 1 };""",
"""  var STORAGE_KEY = 'python-basics-quiz-v1';
  var TYPE_LABEL = {
    single: '单选题', blank: '填空题', judge: '判断题',
    short: '简答题', code: '编程题', coderead: '代码自测'
  };
  var OBJECTIVE = { single: 1, judge: 1, blank: 1, coderead: 1 };""")

P('默认状态加考试范围', """      mode: 'all', // all | favorites | wrong | paper
      order: [],""",
"""      mode: 'all', // all | favorites | wrong | paper
      examOnly: false,
      order: [],""")

P('题型计数', """  function countByType() {
    var c = { single: 0, multi: 0, judge: 0, blank: 0, short: 0, case: 0 };""",
"""  function countByType() {
    var c = { single: 0, blank: 0, judge: 0, short: 0, code: 0, coderead: 0 };""")

P('首页统计标签', """    var labels = [
      ['单选', c.single], ['多选', c.multi], ['判断', c.judge],
      ['填空', c.blank], ['简答', c.short], ['案例', c.case]
    ];""",
"""    var labels = [
      ['单选', c.single], ['填空', c.blank], ['判断', c.judge],
      ['简答', c.short], ['编程', c.code], ['代码自测', c.coderead]
    ];""")

P('首页统计加考试范围', """    html += '<div class="stat"><div class="n">' + bank.length + '</div><div class="l">合计</div></div>';""",
"""    html += '<div class="stat exam-stat"><div class="n">' +
      bank.filter(function (q) { return !!q.exam; }).length + '</div><div class="l">考试范围</div></div>';
    html += '<div class="stat"><div class="n">' + bank.length + '</div><div class="l">合计</div></div>';""")

P('题池加范围过滤', """  function basePool() {
    if (state.mode === 'favorites') {
      return bank.filter(function (q) { return isFavorite(q.id); });
    }
    if (state.mode === 'wrong') {
      return bank.filter(function (q) { return state.wrongIds.indexOf(q.id) >= 0; });
    }
    if (state.mode === 'paper' && Array.isArray(state.paperIds) && state.paperIds.length) {
      return state.paperIds.map(function (id) { return bankMap[id]; }).filter(Boolean);
    }
    // all
    return bank.filter(function (q) {
      if (state.chapter !== 'all' && String(q.chapter) !== String(state.chapter)) return false;
      if (state.type !== 'all' && q.type !== state.type) return false;
      return true;
    });
  }""",
"""  function applyScope(list) {
    if (!state.examOnly) return list;
    return list.filter(function (q) { return !!q.exam; });
  }

  function basePool() {
    if (state.mode === 'favorites') {
      return applyScope(bank.filter(function (q) { return isFavorite(q.id); }));
    }
    if (state.mode === 'wrong') {
      return applyScope(bank.filter(function (q) { return state.wrongIds.indexOf(q.id) >= 0; }));
    }
    if (state.mode === 'paper' && Array.isArray(state.paperIds) && state.paperIds.length) {
      return applyScope(state.paperIds.map(function (id) { return bankMap[id]; }).filter(Boolean));
    }
    // all
    return applyScope(bank.filter(function (q) {
      if (state.chapter !== 'all' && String(q.chapter) !== String(state.chapter)) return false;
      if (state.type !== 'all' && q.type !== state.type) return false;
      return true;
    }));
  }""")

P('空状态提示', """        '<p>客观题答错会自动记入；简答/案例可自行「记入错题」。答对后自动移出。</p></div>';""",
"""        '<p>客观题答错会自动记入；简答/编程题可自行「记入错题」。答对后自动移出。</p></div>';""")

P('题头与标签', """    html += '<div class="q-head">';
    html += '<span class="q-type">' + escapeHtml(TYPE_LABEL[q.type] || q.type) +
      ' · 第' + q.chapter + '章</span>';
    html += '<button type="button" class="fav-btn' + (favOn ? ' on' : '') + '" id="btn-fav" aria-pressed="' +
      (favOn ? 'true' : 'false') + '"><span class="heart">' + (favOn ? '♥' : '♡') +
      '</span> ' + (favOn ? '已收藏' : '收藏') + '</button>';
    html += '</div>';
    html += '<p class="stem">' + escapeHtml(q.stem) + '</p>';""",
"""    html += '<div class="q-head"><div class="q-head-left">';
    html += '<span class="q-type">' + escapeHtml(TYPE_LABEL[q.type] || q.type) +
      ' · 第' + q.chapter + '章 ' + escapeHtml(q.chapterTitle || '') + '</span>';
    html += q.exam ? '<span class="exam-tag">考试范围</span>'
                   : '<span class="review-tag">复习拓展</span>';
    html += '</div>';
    html += '<button type="button" class="fav-btn' + (favOn ? ' on' : '') + '" id="btn-fav" aria-pressed="' +
      (favOn ? 'true' : 'false') + '"><span class="heart">' + (favOn ? '♥' : '♡') +
      '</span> ' + (favOn ? '已收藏' : '收藏') + '</button>';
    html += '</div>';
    html += '<div class="stem">' + escapeHtml(q.stem) + '</div>';
    if (q.code) {
      html += '<pre class="code-block">' + escapeHtml(q.code) + '</pre>';
    }""")

P('选项渲染', """    if (q.type === 'single' || q.type === 'multi') {
      html += '<div class="options" id="opts">';
      (q.options || []).forEach(function (opt) {
        var letter = opt.charAt(0);
        var inputType = q.type === 'multi' ? 'checkbox' : 'radio';
        var checked = false;
        if (saved && saved.choice != null) {
          if (q.type === 'multi') checked = (saved.choice || []).indexOf(letter) >= 0;
          else checked = saved.choice === letter;
        }
        html += '<label class="opt' + (checked ? ' selected' : '') + '" data-letter="' + letter + '">' +
          '<input type="' + inputType + '" name="opt" value="' + letter + '"' +
          (checked ? ' checked' : '') + ' />' +
          '<span>' + escapeHtml(opt) + '</span></label>';
      });
      html += '</div>';""",
"""    if (q.type === 'single' || q.type === 'coderead') {
      html += '<div class="options" id="opts">';
      (q.options || []).forEach(function (opt) {
        var letter = opt.charAt(0);
        var checked = saved && saved.choice != null && saved.choice === letter;
        html += '<label class="opt' + (checked ? ' selected' : '') + '" data-letter="' + letter + '">' +
          '<input type="radio" name="opt" value="' + letter + '"' +
          (checked ? ' checked' : '') + ' />' +
          '<span>' + escapeHtml(opt) + '</span></label>';
      });
      html += '</div>';""")

P('主观题输入占位', """      html += '<textarea id="text-input" placeholder="请用自己的话作答">' + escapeHtml(tv) + '</textarea>';""",
"""      html += '<textarea id="text-input" placeholder="' +
        (q.type === 'code' ? '写出你的程序或解题思路（提交后对照参考程序）' : '请用自己的话作答') +
        '">' + escapeHtml(tv) + '</textarea>';""")

P('收集答案-单选', """  function collectResponse(q) {
    if (q.type === 'single') {""",
"""  function collectResponse(q) {
    if (q.type === 'single' || q.type === 'coderead') {""")

P('判分-单选', """  function grade(q, response) {
    if (q.type === 'single') {""",
"""  function grade(q, response) {
    if (q.type === 'single' || q.type === 'coderead') {""")

P('判分-填空期望答案', """      return { correct: ok && got.length > 0, expected: (q.answer || []).join(' / ') };""",
"""      return { correct: ok && got.length > 0, expected: q.answerText || (q.answer || []).join(' / ') };""")

P('主观题判分分支', """    if (q.type === 'short' || q.type === 'case') {""",
"""    if (q.type === 'short' || q.type === 'code') {""", 1)

P('参考答案展示', """      html += '<div class="side-by-side">';
      html += '<div class="box"><strong>你的作答</strong><br>' + escapeHtml(record.text || '（未作答）') + '</div>';
      html += '<div class="box"><strong>参考答案</strong><br>' +
        escapeHtml(typeof q.answer === 'string' ? q.answer : JSON.stringify(q.answer)) + '</div>';
      html += '</div>';
      if (q.type === 'short' && q.pptQuote) {
        html += '<div class="box"><div class="quote-label">课件原话</div>' + escapeHtml(q.pptQuote) + '</div>';
      }
      var inWrong = state.wrongIds.indexOf(q.id) >= 0;
      html += '<div class="self-mark" id="self-mark">';
      html += '<span class="hint">主观题不自动判分，可自行记入错题本：</span>';""",
"""      html += '<div class="side-by-side">';
      html += '<div class="box"><strong>你的作答</strong><br>' + escapeHtml(record.text || '（未作答）') + '</div>';
      html += '<div class="box"><strong>参考' + (q.type === 'code' ? '程序' : '答案') + '</strong><br>' +
        (q.type === 'code'
          ? '<pre class="code-block small">' + escapeHtml(String(q.answer || '')) + '</pre>'
          : escapeHtml(typeof q.answer === 'string' ? q.answer : JSON.stringify(q.answer))) + '</div>';
      html += '</div>';
      var inWrong = state.wrongIds.indexOf(q.id) >= 0;
      html += '<div class="self-mark" id="self-mark">';
      html += '<span class="hint">主观题不自动判分，可自行记入错题本：</span>';""")

P('选项高亮', """      if (q.type === 'single' || q.type === 'multi') {
        var correctSet = q.type === 'multi' ? q.answer : [q.answer];""",
"""      if (q.type === 'single' || q.type === 'coderead') {
        var correctSet = [q.answer];""")

P('解析与来源', """    if (q.explanation) {
      html += '<div class="box"><strong>解析</strong><br>' + escapeHtml(q.explanation) + '</div>';
    }
    html += '<p class="src">来源：' + escapeHtml(q.sourceFile) + ' · ' + escapeHtml(q.sourceLocator) + '</p>';""",
"""    if (q.explanation) {
      html += '<div class="box"><strong>解析</strong><br>' + escapeHtml(q.explanation) + '</div>';
    }
    if (q.answerNote) {
      html += '<div class="box note-box"><strong>提示</strong><br>' + escapeHtml(q.answerNote) + '</div>';
    }
    html += '<p class="src">来源：' + escapeHtml(q.sourceKind || '') + ' · ' +
      escapeHtml(q.sourceFile) + ' · ' + escapeHtml(q.sourceLocator) + '</p>';""")

P('提交-空答案校验', """    if ((q.type === 'short' || q.type === 'case') && !String(response || '').trim()) {""",
"""    if ((q.type === 'short' || q.type === 'code') && !String(response || '').trim()) {""")

P('提交-记录', """      choice: (q.type === 'single' || q.type === 'multi' || q.type === 'judge') ? response : null,
      text: (q.type === 'blank' || q.type === 'short' || q.type === 'case') ? response : null,""",
"""      choice: (q.type === 'single' || q.type === 'coderead' || q.type === 'judge') ? response : null,
      text: (q.type === 'blank' || q.type === 'short' || q.type === 'code') ? response : null,""")

P('练习页同步范围筛选', """    document.getElementById('filter-type').value = state.type;
    document.getElementById('toggle-shuffle').checked = !!state.shuffle;""",
"""    document.getElementById('filter-type').value = state.type;
    var fs = document.getElementById('filter-scope');
    if (fs) fs.value = state.examOnly ? 'exam' : 'all';
    document.getElementById('toggle-shuffle').checked = !!state.shuffle;""")

P('组卷池加范围', """  function paperPool() {
    var chapters = getPaperChapterFilter();
    var type = document.getElementById('paper-type').value;
    return bank.filter(function (q) {
      if (chapters !== 'all') {
        if (chapters.indexOf(String(q.chapter)) < 0) return false;
      }
      if (type !== 'all' && q.type !== type) return false;
      return true;
    });
  }""",
"""  function paperPool() {
    var chapters = getPaperChapterFilter();
    var type = document.getElementById('paper-type').value;
    var scopeEl = document.getElementById('paper-scope');
    var scope = scopeEl ? scopeEl.value : 'all';
    return bank.filter(function (q) {
      if (scope === 'exam' && !q.exam) return false;
      if (chapters !== 'all') {
        if (chapters.indexOf(String(q.chapter)) < 0) return false;
      }
      if (type !== 'all' && q.type !== type) return false;
      return true;
    });
  }""")

P('筛选事件', """  document.getElementById('toggle-shuffle').addEventListener('change', function (e) {""",
"""  var scopeSel = document.getElementById('filter-scope');
  if (scopeSel) {
    scopeSel.addEventListener('change', function (e) {
      state.examOnly = e.target.value === 'exam';
      state.order = [];
      rebuildFilter(true);
      renderQuestion();
    });
  }
  var examQuick = document.getElementById('btn-exam-only');
  if (examQuick) {
    examQuick.addEventListener('click', function () {
      state.mode = 'all';
      state.examOnly = true;
      state.chapter = 'all';
      state.type = 'all';
      state.order = [];
      state.sessionEnded = false;
      saveState();
      showPractice();
    });
  }
  document.getElementById('toggle-shuffle').addEventListener('change', function (e) {""")

P('组卷范围事件', """  document.getElementById('paper-type').addEventListener('change', updatePaperPoolHint);""",
"""  document.getElementById('paper-type').addEventListener('change', updatePaperPoolHint);
  var paperScope = document.getElementById('paper-scope');
  if (paperScope) paperScope.addEventListener('change', updatePaperPoolHint);""")

P('暴露接口给代码复习模块', """  renderHomeStats();
  syncModeChips();
})();""",
"""  window.QuizApp = {
    showHome: showHome,
    showPractice: function (opts) {
      if (opts) {
        if (opts.chapter != null) state.chapter = String(opts.chapter);
        if (opts.type != null) state.type = opts.type;
        if (opts.examOnly != null) state.examOnly = !!opts.examOnly;
        state.mode = 'all';
        state.order = [];
        state.sessionEnded = false;
        saveState();
      }
      showPractice();
    },
    getState: function () { return state; }
  };

  renderHomeStats();
  syncModeChips();
})();""")


def main():
    src = open(PATH, encoding='utf-8').read()
    for name, old, new, count in PATCHES:
        found = src.count(old)
        if found != count:
            print('FAIL [%s] 期望 %d 处，实际 %d 处' % (name, count, found))
            print('  old snippet:', repr(old[:100]))
            sys.exit(1)
        src = src.replace(old, new, count)
        print('OK  ', name)
    open(PATH, 'w', encoding='utf-8').write(src)
    print('patched ->', PATH, len(src), 'chars')


if __name__ == '__main__':
    main()
