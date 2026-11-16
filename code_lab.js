/* 代码复习模块：pythonProject-2025 第 1-12 章示例代码 + 知识点清单 */
(function () {
  'use strict';

  var STORE = 'python-basics-quiz-lab-v1';
  var chapters = (window.CODE_LAB && window.CODE_LAB) || [];
  var current = 1;
  var currentFile = 0;
  var checked = loadChecked();

  function loadChecked() {
    try {
      var d = JSON.parse(localStorage.getItem(STORE) || '{}');
      return (d && typeof d === 'object') ? d : {};
    } catch (e) { return {}; }
  }
  function saveChecked() {
    try { localStorage.setItem(STORE, JSON.stringify(checked)); } catch (e) {}
  }
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function chapter(n) {
    for (var i = 0; i < chapters.length; i++) if (chapters[i].n === n) return chapters[i];
    return null;
  }
  function key(n, i) { return n + ':' + i; }

  /* ---------- 顶部导航 ---------- */
  var navBtns = document.querySelectorAll('#top-nav .nav-btn');
  function setView(view) {
    var lab = document.getElementById('code-lab');
    var home = document.getElementById('home');
    var practice = document.getElementById('practice');
    navBtns.forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-view') === view);
    });
    var wrap = document.querySelector('.wrap');
    if (wrap) wrap.classList.toggle('wide', view === 'lab');
    if (view === 'lab') {
      home.classList.add('hidden');
      practice.classList.add('hidden');
      lab.classList.remove('hidden');
      renderAll();
    } else {
      lab.classList.add('hidden');
      if (window.QuizApp) window.QuizApp.showHome();
      else { home.classList.remove('hidden'); practice.classList.add('hidden'); }
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
  navBtns.forEach(function (b) {
    b.addEventListener('click', function () { setView(b.getAttribute('data-view')); });
  });
  var goLab = document.getElementById('btn-go-lab');
  if (goLab) goLab.addEventListener('click', function () { setView('lab'); });

  /* ---------- 章节列表 ---------- */
  function renderChapterList() {
    var box = document.getElementById('lab-chapter-list');
    var html = chapters.map(function (c) {
      var done = c.points.filter(function (_, i) { return checked[key(c.n, i)]; }).length;
      var examTag = c.n <= 8
        ? '<span class="lab-mini exam">考代码</span>'
        : '<span class="lab-mini">复习</span>';
      return '<button type="button" class="lab-ch' + (c.n === current ? ' active' : '') +
        '" data-ch="' + c.n + '">' +
        '<span class="lab-ch-n">第' + c.n + '章</span>' +
        '<span class="lab-ch-t">' + esc(c.title) + '</span>' +
        '<span class="lab-ch-meta">' + c.files.length + ' 文件 · ' + done + '/' + c.points.length + ' 要点</span>' +
        examTag + '</button>';
    }).join('');
    box.innerHTML = html;
    box.querySelectorAll('.lab-ch').forEach(function (b) {
      b.addEventListener('click', function () {
        current = parseInt(b.getAttribute('data-ch'), 10);
        currentFile = 0;
        renderAll();
      });
    });
  }

  /* ---------- 知识点清单 ---------- */
  function renderPoints() {
    var c = chapter(current);
    if (!c) return;
    var box = document.getElementById('lab-point-list');
    box.innerHTML = c.points.map(function (p, i) {
      var on = !!checked[key(c.n, i)];
      return '<label class="lab-point' + (on ? ' done' : '') + '">' +
        '<input type="checkbox" data-i="' + i + '"' + (on ? ' checked' : '') + ' />' +
        '<span>' + esc(p) + '</span></label>';
    }).join('');
    box.querySelectorAll('input').forEach(function (el) {
      el.addEventListener('change', function () {
        var i = parseInt(el.getAttribute('data-i'), 10);
        checked[key(current, i)] = el.checked;
        saveChecked();
        renderPoints();
        renderChapterList();
      });
    });
    var total = 0, done = 0;
    chapters.forEach(function (ch) {
      total += ch.points.length;
      ch.points.forEach(function (_, i) { if (checked[key(ch.n, i)]) done++; });
    });
    var pg = document.getElementById('lab-progress');
    if (pg) pg.textContent = '本章 ' + c.points.filter(function (_, i) { return checked[key(c.n, i)]; }).length +
      '/' + c.points.length + ' · 全部 ' + done + '/' + total;
  }

  /* ---------- 文件与代码 ---------- */
  var TOKEN_RE = /("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(#.*)|\b(def|class|return|if|elif|else|for|while|in|import|from|as|try|except|finally|raise|with|lambda|None|True|False|and|or|not|is|pass|break|continue|global|nonlocal|match|case|self|print)\b|\b(\d+(?:\.\d+)?)\b/g;

  function highlight(code) {
    // 单次扫描着色：字符串 / 注释 / 关键字 / 数字，避免对已生成的 HTML 二次替换
    return code.split('\n').map(function (line, idx) {
      var out = '', last = 0, m;
      TOKEN_RE.lastIndex = 0;
      while ((m = TOKEN_RE.exec(line)) !== null) {
        out += esc(line.slice(last, m.index));
        var t = m[0];
        if (m[1]) out += '<span class="tok-str">' + esc(t) + '</span>';
        else if (m[2]) out += '<span class="tok-cmt">' + esc(t) + '</span>';
        else if (m[3]) out += '<span class="tok-kw">' + esc(t) + '</span>';
        else out += '<span class="tok-num">' + esc(t) + '</span>';
        last = m.index + t.length;
      }
      out += esc(line.slice(last));
      return '<span class="ln">' + String(idx + 1).padStart(3, ' ') + '</span>' + out + '\n';
    }).join('');
  }

  function renderFiles() {
    var c = chapter(current);
    if (!c) return;
    var tabs = document.getElementById('lab-file-tabs');
    var cnt = document.getElementById('lab-file-count');
    var meta = document.getElementById('lab-file-meta');
    var view = document.querySelector('#lab-code-view code');
    if (cnt) cnt.textContent = '共 ' + c.files.length + ' 个 .py 文件';
    tabs.innerHTML = c.files.map(function (f, i) {
      return '<button type="button" class="lab-file' + (i === currentFile ? ' active' : '') +
        '" data-i="' + i + '">' + esc(f.name) + '</button>';
    }).join('');
    tabs.querySelectorAll('.lab-file').forEach(function (b) {
      b.addEventListener('click', function () {
        currentFile = parseInt(b.getAttribute('data-i'), 10);
        renderFiles();
      });
    });
    var f = c.files[currentFile];
    var extra = document.getElementById('lab-file-extra');
    if (!f) {
      if (meta) meta.textContent = '本章暂无示例文件';
      if (view) view.innerHTML = '';
      if (extra) extra.innerHTML = '';
      return;
    }
    if (meta) {
      meta.innerHTML = 'pythonProject-2025/chapter' + c.n + '/' + f.name +
        ' · ' + f.code.split('\n').length + ' 行' +
        (f.updated ? ' <span class="badge-new">更新版</span>' : '');
    }
    if (view) view.innerHTML = highlight(f.code || '# 空文件');
    if (extra) extra.innerHTML = renderExtra(f);
  }

  /* 每个文件的「考什么 / 运行输出 / 关键注释 / 易错点」学习卡 */
  function renderExtra(f) {
    var titleBox = document.getElementById('lab-file-title');
    var extraBox = document.getElementById('lab-file-extra');
    if (!f.title && !f.output && !f.notes) {
      if (titleBox) titleBox.innerHTML = '';
      if (extraBox) extraBox.innerHTML =
        '<div class="ce-empty">该文件暂未整理学习卡（目前第 4-8 章更新版代码已全部覆盖）。</div>';
      return '';
    }
    // 考点导读放在代码上方，输出/注释放在代码下方
    if (titleBox) {
      titleBox.innerHTML = f.title
        ? '<div class="ce-title">🎯 这段考什么：' + esc(f.title) + '</div>' : '';
    }
    var h = '<div class="code-extra">';
    if (f.output || f.err) {
      h += '<div class="ce-block"><div class="ce-label">运行输出';
      if (f.stdin) h += '（运行输入：' + esc(f.stdin.replace(/\n/g, '⏎')) + '）';
      h += '</div><pre class="ce-out">' + esc(f.output || '（无标准输出）') + '</pre>';
      if (f.err) {
        h += '<div class="ce-label ce-label-err">运行时异常（多为故意演示）</div>' +
          '<pre class="ce-out ce-err">' + esc(f.err) + '</pre>';
      }
      h += '</div>';
    }
    if (f.notes && f.notes.length) {
      h += '<div class="ce-block"><div class="ce-label">关键注释</div><ol class="ce-notes">';
      f.notes.forEach(function (n) { h += '<li>' + esc(n) + '</li>'; });
      h += '</ol></div>';
    }
    if (f.pitfall) {
      h += '<div class="ce-pitfall"><strong>易错点</strong>' + esc(f.pitfall) + '</div>';
    }
    h += '</div>';
    return h;
  }

  function renderAll() {
    renderChapterList();
    renderPoints();
    renderFiles();
  }

  /* ---------- 跳转练习 ---------- */
  function practice(type) {
    if (!window.QuizApp) return;
    setView('quiz');
    window.QuizApp.showPractice({ chapter: current, type: type, examOnly: false });
  }
  var bp = document.getElementById('btn-lab-practice');
  var br = document.getElementById('btn-lab-readquiz');
  if (bp) bp.addEventListener('click', function () { practice('code'); });
  if (br) br.addEventListener('click', function () { practice('coderead'); });

  renderChapterList();
})();
