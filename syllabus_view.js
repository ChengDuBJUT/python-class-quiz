/* 考纲对照页：把老师公布的考纲和题库实际覆盖对起来。
   数据来自 data/syllabus.js（tools/build_syllabus.py 生成），这里只负责渲染。 */
(function () {
  'use strict';

  var S = window.SYLLABUS;
  if (!S) return;

  var CHAPTER_TITLES = {
    1: '绪论', 2: 'Python基础', 3: '数据类型', 4: '运算符', 5: '流程控制',
    6: '组合数据类型', 7: '函数', 8: '类与对象', 9: '异常、调试与测试',
    10: '文件与数据格式化', 11: '标准库应用编程', 12: '第三方库应用编程'
  };

  var LEVEL = {
    ok: { text: '充足', cls: 'ok' },
    thin: { text: '偏薄', cls: 'thin' },
    gap: { text: '缺口', cls: 'gap' }
  };

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function chLabel(list) {
    return list.map(function (n) { return '第' + n + '章'; }).join(' · ');
  }

  /* ---------- 考试结构 ---------- */
  function renderPaper() {
    var box = document.getElementById('sy-paper');
    if (!box) return;
    var total = 0;
    box.innerHTML = S.paper.map(function (p) {
      total += p.total;
      return '<div class="sy-paper-item">' +
        '<div class="sy-paper-name">' + esc(p.name) + '</div>' +
        '<div class="sy-paper-calc">' + p.n + ' × ' + p.per + ' = <b>' + p.total + '</b> 分</div>' +
        '<div class="sy-paper-note">' + esc(p.note) + '</div></div>';
    }).join('') + '<div class="sy-paper-item sy-paper-sum">' +
      '<div class="sy-paper-name">合计</div>' +
      '<div class="sy-paper-calc"><b>' + total + '</b> 分</div>' +
      '<div class="sy-paper-note">客观 60 + 编程 40 + 附加 10</div></div>';

    var note = document.getElementById('sy-note');
    if (note) note.textContent = S.range.note;
  }

  /* ---------- 范围规则 ---------- */
  function renderRange() {
    var box = document.getElementById('sy-range');
    if (!box) return;
    var rows = [
      ['考试内容', S.range.chapters],
      ['客观题', S.range.objective],
      ['编程题', S.range.code],
      ['编程不考', S.range.codeOut]
    ];
    box.innerHTML = '<h3 class="sy-title">范围与题型</h3><div class="sy-range-grid">' +
      rows.map(function (r) {
        return '<div class="sy-range-row"><span class="sy-range-k">' + esc(r[0]) +
          '</span><span class="sy-range-v">' + esc(r[1]) + '</span></div>';
      }).join('') + '</div>' +
      '<p class="sy-flag">⚠️ 老师说「9–12 章编程不考」，但同一句又写「编程题必考一道文件」——' +
      '文件在第 10 章。两者按字面冲突，本站的处理是：<b>文件读写照常当必考准备</b>' +
      '（做了不会亏），第 9/11/12 章的异常、标准库、第三方库编程按不考处理。' +
      '如果要更保险，考试前跟老师确认一句。</p>';
  }

  /* ---------- 考点覆盖 ---------- */
  function renderTopics() {
    var box = document.getElementById('sy-topics');
    if (!box) return;
    var max = 1;
    S.topics.forEach(function (t) { max = Math.max(max, t.nObj); });

    box.innerHTML = S.topics.map(function (t, i) {
      var lv = LEVEL[t.level] || LEVEL.thin;
      var pct = Math.max(4, Math.round(t.nObj / max * 100));
      var objs = t.nObj + ' 道客观题';
      var codes = t.codeInExam
        ? (t.nCode ? t.nCode + ' 道编程题' : '无编程题')
        : '编程不考';
      return '<div class="sy-topic">' +
        '<div class="sy-topic-rank">' + String(i + 1).padStart(2, '0') + '</div>' +
        '<div class="sy-topic-main">' +
          '<div class="sy-topic-head"><b>' + esc(t.name) + '</b>' +
          '<span class="sy-ch">' + chLabel(t.chapters) + '</span></div>' +
          '<div class="sy-bar"><span style="width:' + pct + '%"></span></div>' +
          '<div class="sy-topic-sub">' + objs + ' · ' + codes + '</div>' +
        '</div>' +
        '<span class="sy-badge ' + lv.cls + '">' + lv.text + '</span>' +
        '<div class="sy-topic-go">' +
          '<button type="button" class="sy-go" data-ch="' + t.chapters[0] + '" data-type="all">刷客观</button>' +
          (t.codeInExam && t.nCode
            ? '<button type="button" class="sy-go ghost" data-ch="' + t.chapters[0] + '" data-type="code">刷编程</button>'
            : '') +
        '</div>' +
      '</div>';
    }).join('');

    box.querySelectorAll('.sy-go').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!window.QuizApp) return;
        window.QuizApp.showPractice({
          chapter: b.getAttribute('data-ch'),
          type: b.getAttribute('data-type'),
          examOnly: true
        });
      });
    });
  }

  /* ---------- 必考编程模板 ---------- */
  function renderTemplates() {
    var box = document.getElementById('sy-templates');
    if (!box) return;
    box.innerHTML = S.templates.map(function (t) {
      return '<div class="sy-tpl">' +
        '<div class="sy-tpl-head"><b>' + esc(t.name) + '</b>' +
        (t.must ? '<span class="sy-must">必考</span>' : '') + '</div>' +
        '<p class="sy-tpl-why">' + esc(t.why) + '</p>' +
        '<pre class="code-block"><code>' + esc(t.code) + '</code></pre>' +
        '<ul class="sy-tpl-points">' + t.points.map(function (p) {
          return '<li>' + esc(p) + '</li>';
        }).join('') + '</ul>' +
        '<div class="sy-tpl-act">' +
          '<button type="button" class="sy-go" data-tpl="' + esc(t.key) + '">去刷这类编程题</button>' +
        '</div>' +
      '</div>';
    }).join('');

    var TPL_CH = { file: 10, recursion: 7, base: 3 };
    box.querySelectorAll('.sy-go').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!window.QuizApp) return;
        window.QuizApp.showPractice({
          chapter: TPL_CH[b.getAttribute('data-tpl')] || 'all',
          type: 'code',
          examOnly: true
        });
      });
    });
  }

  function renderAll() {
    var total = document.getElementById('sy-total');
    if (total) total.textContent = S.total;
    renderPaper();
    renderRange();
    renderTopics();
    renderTemplates();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderAll);
  } else {
    renderAll();
  }

  window.SyllabusView = { renderAll: renderAll };
})();
