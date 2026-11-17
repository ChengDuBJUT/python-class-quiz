const puppeteer = require('puppeteer');
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true, args: ['--no-sandbox']
  });
  const p = await b.newPage();
  await p.setViewport({ width: 1280, height: 1000, deviceScaleFactor: 1.3 });
  const errs = [];
  p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await p.goto('http://127.0.0.1:8765/index.html', { waitUntil: 'networkidle0' });
  await sleep(500);

  // ---- 1. 按考纲组卷 ----
  await p.evaluate(() => document.getElementById('chip-paper').click());
  await sleep(300);
  await p.evaluate(() => document.getElementById('btn-start-syllabus').click());
  await sleep(700);
  const paper = await p.evaluate(() => {
    const st = window.QuizApp.getState();
    const bank = window.QUESTION_BANK;
    const qs = st.paperIds.map(id => bank.find(q => q.id === id));
    const byType = qs.reduce((a, q) => (a[q.type] = (a[q.type] || 0) + 1, a), {});
    const codes = qs.filter(q => q.type === 'code' && !q.hard).map(q =>
      q.stem + ' ' + (q.code || '') + ' ' + (q.options || []).join(' '));
    const hit = tokens => codes.filter(t => tokens.some(k => t.indexOf(k) >= 0)).length;
    return {
      n: st.paperIds.length, name: st.paperName, byType,
      first: qs[0].type, at40: qs[39].type, at50: qs[49].type, at58: qs[57].type, last: qs[58].type,
      allExam: qs.every(q => q.exam),
      file: hit(['文件', 'open(', 'read', 'write', 'csv', '.txt']),
      rec: hit(['递归', '阶乘', '斐波那契', '汉诺塔']),
      base: hit(['进制', '二进制', '八进制', '十六进制']),
      progress: document.getElementById('progress-text').innerText,
      tag: (document.querySelector('.paper-tag') || {}).innerText || ''
    };
  });
  console.log('组卷：', paper.n, '题 |', paper.name, '| 题型', JSON.stringify(paper.byType));
  console.log('分块 1/40/50/58/59 =', paper.first, paper.at40, paper.at50, paper.at58, paper.last);
  console.log('全部考试范围:', paper.allExam, '| 文件/递归/数制命中:', paper.file, paper.rec, paper.base);
  console.log('进度:', paper.progress, '| 卷标:', paper.tag);

  // ---- 2. 笔记 ----
  await p.evaluate(() => document.getElementById('toggle-notes').click());
  await sleep(400);
  const noteShown = await p.evaluate(() => !!document.getElementById('note-input'));
  console.log('打开笔记开关后有输入框:', noteShown);

  const NOTE = '坑：这里要用 else 分支，不是 elif；下次别再写错。';
  await p.type('#note-input', NOTE);
  await sleep(600);
  const saved1 = await p.evaluate(() => ({
    status: document.getElementById('note-status').innerText,
    stored: JSON.parse(localStorage.getItem('python-basics-quiz-notes-v1') || '{}'),
    exportLabel: document.getElementById('btn-notes-export').innerText
  }));
  console.log('输入后状态:', saved1.status, '| 导出按钮:', saved1.exportLabel,
    '| 已存笔记数:', Object.keys(saved1.stored).length);

  // 翻到下一题再回来：面板默认收起，但重新点开内容还在
  await p.evaluate(() => document.getElementById('btn-next').click());
  await sleep(300);
  const on2 = await p.evaluate(() => !document.getElementById('note-input'));
  await p.evaluate(() => document.getElementById('btn-prev').click());
  await sleep(300);
  const back1 = await p.evaluate(() => !document.getElementById('note-input'));
  console.log('换题后自动收起:', on2, '| 切回后仍收起:', back1);
  await p.evaluate(() => document.getElementById('toggle-notes').click());
  await sleep(300);
  const reOpen = await p.evaluate(() => (document.getElementById('note-input') || {}).value || '');
  console.log('重新点开带出原笔记:', reOpen === NOTE);

  // 刷新页面：默认收起，笔记内容不丢
  await p.reload({ waitUntil: 'networkidle0' });
  await sleep(500);
  await p.evaluate(() => { document.getElementById('btn-enter').click(); });
  await sleep(500);
  const afterReload = await p.evaluate(() => ({
    pressed: document.getElementById('toggle-notes').getAttribute('aria-pressed'),
    noInput: !document.getElementById('note-input'),
    mode: window.QuizApp.getState().mode
  }));
  console.log('刷新后 默认关:', afterReload.pressed === 'false' && afterReload.noInput, '| mode:', afterReload.mode);
  await p.evaluate(() => document.getElementById('toggle-notes').click());
  await sleep(300);
  const reloadNote = await p.evaluate(() => (document.getElementById('note-input') || {}).value || '');
  console.log('刷新后点开 笔记仍在:', reloadNote === NOTE);

  // 再点一次开关：输入框消失，但笔记数据仍在
  await p.evaluate(() => document.getElementById('toggle-notes').click());
  await sleep(300);
  const off = await p.evaluate(() => ({
    noInput: !document.getElementById('note-input'),
    storedCount: Object.keys(JSON.parse(localStorage.getItem('python-basics-quiz-notes-v1') || '{}')).length
  }));
  console.log('关掉开关 输入框消失:', off.noInput, '| 笔记仍保存:', off.storedCount);

  // 容量
  const cap = await p.evaluate(() => {
    const raw = localStorage.getItem('python-basics-quiz-notes-v1') || '';
    return { chars: raw.length, keys: Object.keys(localStorage) };
  });
  console.log('笔记存储字符数:', cap.chars, '| keys:', cap.keys.join(', '));

  console.log('控制台错误:', errs.length ? errs.slice(0, 4) : '无');
  await b.close();
})();
