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
      meta.innerHTML = '<span class="meta-text">pythonProject-2025/chapter' + c.n + '/' + f.name +
        ' · ' + f.code.split('\n').length + ' 行' +
        (f.updated ? ' <span class="badge-new">更新版</span>' : '') +
        '</span><span class="ask-group">' +
        '<button type="button" class="ask-ai" data-ai="deepseek"' +
        ' title="把这段代码和它的真实运行结果一起发给 DeepSeek，让它讲讲怎么理解">🤖 DeepSeek</button>' +
        '<button type="button" class="ask-ai" data-ai="qwen"' +
        ' title="同样的问题换发给通义千问——DeepSeek 额度用完时可以换着用">🤖 千问</button>' +
        '</span>';
      meta.querySelectorAll('.ask-ai').forEach(function (btn) {
        btn.addEventListener('click', function () { askAbout(f, btn.getAttribute('data-ai')); });
      });
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
        '<div class="ce-empty">该文件暂未整理学习卡（目前第 4-11 章更新版代码已全部覆盖）。</div>';
      return '';
    }
    // 考点导读放在代码上方，输出/注释放在代码下方
    if (titleBox) {
      titleBox.innerHTML = f.title
        ? '<div class="ce-title">🎯 这段考什么：' + esc(f.title) + '</div>' : '';
    }
    var h = '<div class="code-extra">';
    // 输出块始终显示：确实没有输出的（如 matplotlib 只出图）也要让人看到「无标准输出」，
    // 而不是以为这一栏坏了
    h += '<div class="ce-block"><div class="ce-label">运行输出';
    if (f.stdin) h += '（运行输入：' + esc(f.stdin.replace(/\n/g, '⏎')) + '）';
    h += '</div><pre class="ce-out">' + esc(f.output || '（无标准输出）') + '</pre>';
    if (f.err) {
      h += '<div class="ce-label ce-label-err">运行时异常（多为故意演示）</div>' +
        '<pre class="ce-out ce-err">' + esc(f.err) + '</pre>';
    }
    // 少数代码会往绝对路径写东西（如 ch11/test1 的 d:\test），采集时改到了临时目录
    if (f.patched) {
      h += '<div class="ce-label">采集说明</div><pre class="ce-out">本站运行时把 ' +
        esc(f.patched) + '，避免在你的磁盘上真的建目录</pre>';
    }
    h += '</div>';
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

  /* ---------- 问 AI：只把「代码 + 真实运行结果」发过去，问一句大白话 ---------- */
  // 两家都支持 ?q= 自动填入；DeepSeek 限额了就换千问
  // autoSend：带 ?q= 打开后，这家是「填进输入框等按 Enter」还是「直接发送并开始回答」
  var AI_TARGETS = [
    { key: 'deepseek', name: 'DeepSeek', bare: 'https://chat.deepseek.com/', autoSend: false },
    { key: 'qwen', name: '千问', bare: 'https://www.qianwen.com/', autoSend: true }
  ];
  // 官网 ?q= 只能稳定吃下约 1.7KB，所以预算压到 2000：
  // 超了就退回「复制全文 + 裸链接」，保证带过去的内容一定是完整的（粘贴即可）
  var AI_BUDGET = 2000;

  function aiTarget(key) {
    for (var i = 0; i < AI_TARGETS.length; i++) {
      if (AI_TARGETS[i].key === key) return AI_TARGETS[i];
    }
    return AI_TARGETS[0];
  }

  function clip(s, max) {
    s = String(s == null ? '' : s);
    if (max <= 0 || s.length <= max) return s;
    return s.slice(0, max) + '\n…（后面还有 ' + (s.length - max) + ' 个字符，已省略）';
  }

  // 刻意不写长模板：一句人话 + 代码 + 输出，就是学生自己会问的话
  function askPrompt(f, capOut) {
    var L = [];
    L.push('这段代码是什么意思？运行结果为什么是这样？帮我讲讲怎么理解。');
    L.push('');
    L.push('```python');
    L.push(String(f.code || '').replace(/\s+$/, ''));
    L.push('```');
    if (f.output || f.err) {
      L.push('');
      if (f.stdin) L.push('（我运行时输入的是：' + f.stdin.replace(/\n/g, ' ↵ ').replace(/ ↵ $/, '') + '）');
      L.push('运行结果是：');
      L.push('```');
      L.push(clip(f.output || '（没有输出）', capOut));
      if (f.err) {
        L.push('');
        L.push('# 另外报了错：');
        L.push(clip(f.err, Math.min(capOut, 500)));
      }
      L.push('```');
    }
    return L.join('\n');
  }

  // 逐级压缩输出：先保代码完整，实在超长才退回「复制 + 裸链接」
  function pickAsk(f) {
    var caps = [4000, 1500, 600, 200];
    var last = '';
    for (var i = 0; i < caps.length; i++) {
      last = askPrompt(f, caps[i]);
      if (encodeURIComponent(last).length + 28 <= AI_BUDGET) {
        return { prompt: last, autoFill: true, clipped: caps[i] < 4000 };
      }
    }
    return { prompt: last, autoFill: false, clipped: true };
  }

  function legacyCopy(text) {
    try {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', 'readonly');
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.select();
      ta.setSelectionRange(0, ta.value.length);
      var ok = document.execCommand('copy');
      document.body.removeChild(ta);
      return ok;
    } catch (e) {
      return false;
    }
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).then(
        function () { return true; }, function () { return legacyCopy(text); });
    }
    return Promise.resolve(legacyCopy(text));
  }

  function toast(msg, bad) {
    var el = document.getElementById('lab-ai-hint');
    if (!el) {
      el = document.createElement('div');
      el.id = 'lab-ai-hint';
      el.className = 'lab-ai-hint';
      el.setAttribute('role', 'status');
      document.body.appendChild(el);
    }
    el.textContent = msg;
    el.classList.toggle('bad', !!bad);
    el.classList.add('show');
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { el.classList.remove('show'); }, 7000);
  }

  function askAbout(f, key) {
    if (!f) return;
    var t = aiTarget(key);
    var built = pickAsk(f);
    // 剪贴板里永远放不截断的全文，URL 里才可能是压缩版
    var full = askPrompt(f, 0);
    var url = t.bare + (built.autoFill ? '?q=' + encodeURIComponent(built.prompt) : '');
    var win = window.open(url, '_blank');
    if (win) { try { win.opener = null; } catch (e) {} }
    copyText(full).then(function (ok) {
      if (!win) { toast('浏览器拦截了新标签页，请允许本站弹窗后重试。', true); return; }
      if (!ok) {
        toast('自动复制被拦住了：在「' + t.name + '」里粘贴不出来时，手动复制页面上的代码即可。', true);
        return;
      }
      if (built.autoFill && t.autoSend) {
        toast('已打开「' + t.name + '」：问题已经直接发出去了，等它回答就行。'
          + (built.clipped ? '（输出太长，发过去的是压缩版；剪贴板里是完整版）' : '')
          + '（如果停在空白输入框，说明没登录，按 Ctrl/⌘ + V 粘贴再发送）');
      } else if (built.autoFill) {
        toast('已打开「' + t.name + '」：代码和运行结果都填进输入框了，按 Enter 发送。'
          + (built.clipped
            ? '（输出太长，填入的是压缩版；按 Ctrl/⌘ + V 可换成完整版）'
            : '（没填入就 Ctrl/⌘ + V 粘贴）'));
      } else {
        toast('这段代码比较长，全文已复制：在「' + t.name + '」输入框里按 Ctrl/⌘ + V 粘贴再发送。');
      }
    });
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
