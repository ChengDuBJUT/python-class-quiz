const puppeteer = require('puppeteer');
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true, args: ['--no-sandbox']
  });
  const p = await b.newPage();
  await p.setViewport({ width: 1280, height: 1000 });
  const errs = [];
  p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });

  await p.goto('http://127.0.0.1:8765/index.html', { waitUntil: 'networkidle0' });
  await sleep(400);

  // ---- 1. 数据层 ----
  const data = await p.evaluate(() => {
    const S = window.SYLLABUS, Q = window.QUESTION_BANK;
    return {
      hasSy: !!S,
      themes: S ? S.topics.length : 0,
      total: S ? S.total : 0,
      bank: Q.length,
      exCount: Q.filter(q => q.id.startsWith('ex-')).length,
      exBase: (Q.find(q => q.id === 'ex-base-01') || {}),
      exCode: (Q.find(q => q.id === 'ex-base-p1') || {}),
      examJudge: Q.filter(q => q.type === 'judge' && q.exam).length,
      examShort: Q.filter(q => q.type === 'short' && q.exam).length,
      examCode9: Q.filter(q => q.type === 'code' && q.exam && [9, 11, 12].includes(q.chapter)).length,
      examCode10: Q.filter(q => q.type === 'code' && q.exam && q.chapter === 10).length,
      typo: Q.filter(q => (q.options || []).some(o => /excepy/.test(o))).length,
      typoOk: (Q.find(q => q.id === 'ch9-single-04') || {}).options,
      codeWithOut: Q.filter(q => q.type === 'code' && q.output).length
    };
  });
  console.log('SYLLABUS 就绪:', data.hasSy, '| 考点数:', data.themes, '| 总题量:', data.total);
  console.log('题库:', data.bank, '| 补充题:', data.exCount, '| 带运行输出的编程题:', data.codeWithOut);
  console.log('判断 exam:', data.examJudge, '| 简答 exam:', data.examShort);
  console.log('ch9/11/12 编程 exam（应为0）:', data.examCode9, '| ch10 编程 exam:', data.examCode10);
  console.log('excepy 残留:', data.typo, '| ch9-single-04 选项:', JSON.stringify(data.typoOk));
  console.log('ex-base-01 答案:', data.exBase.answer, '| ex-base-p1 输出:', JSON.stringify(data.exCode.output));

  // ---- 2. 考纲页渲染 ----
  await p.evaluate(() => document.getElementById('nav-syllabus').click());
  await sleep(500);
  const view = await p.evaluate(() => {
    const paper = document.querySelectorAll('#sy-paper .sy-paper-item');
    const topics = document.querySelectorAll('#sy-topics .sy-topic');
    const tpl = document.querySelectorAll('#sy-templates .sy-tpl');
    const badges = {};
    document.querySelectorAll('#sy-topics .sy-badge').forEach(x => {
      badges[x.className.replace('sy-badge ', '')] = (badges[x.className.replace('sy-badge ', '')] || 0) + 1;
    });
    return {
      visible: !document.getElementById('syllabus').classList.contains('hidden'),
      paper: paper.length,
      sum: (document.querySelector('.sy-paper-sum .sy-paper-calc') || {}).innerText || '',
      total: (document.getElementById('sy-total') || {}).innerText,
      topics: topics.length,
      tpl: tpl.length,
      badges,
      firstTopic: (topics[0] || {}).innerText || '',
      flag: (document.querySelector('.sy-flag') || {}).innerText.slice(0, 40) || ''
    };
  });
  console.log('\n[考纲页] 可见:', view.visible, '| 结构卡:', view.paper, '| 合计:', view.sum.replace(/\s+/g, ' '));
  console.log('总题量显示:', view.total, '| 考点行:', view.topics, '| 模板:', view.tpl);
  console.log('徽章分布:', JSON.stringify(view.badges));
  console.log('首行:', view.firstTopic.replace(/\s+/g, ' '));
  console.log('冲突提示:', view.flag.replace(/\s+/g, ' '));

  await p.screenshot({ path: 'shot-syllabus.png', fullPage: false });

  // ---- 3. 点「刷编程」跳转 ----
  const jumped = await p.evaluate(async () => {
    const btn = [...document.querySelectorAll('#sy-topics .sy-topic')]
      .find(r => r.innerText.includes('数制转换'))
      .querySelector('.sy-go.ghost');
    btn.click();
    await new Promise(r => setTimeout(r, 300));
    return {
      practiceVisible: !document.getElementById('practice').classList.contains('hidden'),
      ch: document.getElementById('filter-ch').value,
      type: document.getElementById('filter-type').value,
      progress: (document.getElementById('progress-text') || {}).innerText || ''
    };
  });
  console.log('\n[跳转] 练习页可见:', jumped.practiceVisible, '| 章节:', jumped.ch, '| 题型:', jumped.type, '|', jumped.progress);

  // ---- 4. 判断题提示 + 编程题运行结果 ----
  const judgeTip = await p.evaluate(async () => {
    location.hash = '';
    const st = window.QuizApp.getState();
    st.chapter = '9'; st.type = 'judge'; st.mode = 'all'; st.examOnly = false; st.keyword = null;
    window.QuizApp.showPractice();
    await new Promise(r => setTimeout(r, 250));
    const note = document.querySelector('.form-note');
    return { note: note ? note.innerText : null, qtype: (document.querySelector('.type-tag, .q-tag, .stem-tag') || {}).innerText || '(判断题)' };
  });
  console.log('\n[判断题] 类型:', judgeTip.qtype, '| 提示:', (judgeTip.note || '无').slice(0, 40));

  const codeRun = await p.evaluate(async () => {
    const st = window.QuizApp.getState();
    st.chapter = '3'; st.type = 'code'; st.mode = 'all'; st.examOnly = true; st.keyword = null;
    window.QuizApp.showPractice();
    await new Promise(r => setTimeout(r, 250));
    // 找到 ex-base-p1 那一题：翻页直到出现
    let found = null;
    for (let i = 0; i < 30; i++) {
      const t = (document.querySelector('.stem') || {}).innerText || '';
      if (t.includes('二进制、八进制和十六进制')) { found = i; break; }
      document.getElementById('btn-next').click();
      await new Promise(r => setTimeout(r, 60));
    }
    if (found === null) return { ok: false };
    document.getElementById('btn-peek').click();
    await new Promise(r => setTimeout(r, 250));
    const boxes = [...document.querySelectorAll('#reveal .box')].map(x => x.innerText.replace(/\s+/g, ' '));
    return { ok: true, boxes };
  });
  console.log('[编程题] 看答案后的区块:', codeRun.ok ? codeRun.boxes.length : '未找到');
  if (codeRun.ok) console.log('  含运行结果:', codeRun.boxes.some(b => b.includes('运行结果')), '|',
    (codeRun.boxes.find(b => b.includes('运行结果')) || '').slice(0, 70));

  await p.screenshot({ path: 'shot-exam-code.png', fullPage: false });
  console.log('\n控制台错误:', errs.length ? errs.slice(0, 5) : '无');
  await b.close();
})();
