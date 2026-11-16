// 验证 ch9-11 换上老师第二批更新版代码后的站点状态
const puppeteer = require('puppeteer');
const BASE = 'http://127.0.0.1:8765/index.html';
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true,
    args: ['--no-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 1000 });
  const errs = [];
  page.on('pageerror', e => errs.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await page.goto(BASE, { waitUntil: 'networkidle0' });
  await sleep(400);

  const stats = await page.evaluate(() => {
    const lab = window.CODE_LAB;
    const files = lab.reduce((a, c) => a + c.files.length, 0);
    const updated = lab.filter(c => c.updated).map(c => c.n);
    const updFiles = lab.filter(c => c.updated).reduce((a, c) => a + c.files.length, 0);
    const noNotes = [];
    lab.forEach(c => c.files.forEach(f => { if (!f.title || !f.notes || !f.notes.length) noNotes.push(c.n + '/' + f.name); }));
    const cr = window.QUESTION_BANK.filter(q => q.type === 'coderead');
    const kinds = {};
    cr.forEach(q => { kinds[q.kind || 'none'] = (kinds[q.kind || 'none'] || 0) + 1; });
    return {
      files, updatedChaps: updated, updFiles, noNotes,
      ch9: lab.find(c => c.n === 9).files.map(f => f.name),
      ch10: lab.find(c => c.n === 10).files.map(f => f.name),
      ch11: lab.find(c => c.n === 11).files.map(f => f.name),
      coderead: cr.length, kinds,
      verified: cr.filter(q => q.verified).length,
      patched: lab.flatMap(c => c.files.filter(f => f.patched).map(f => c.n + '/' + f.name)),
    };
  });
  console.log('文件总数:', stats.files, '| 更新版章:', stats.updatedChaps.join(','), '| 更新版文件:', stats.updFiles);
  console.log('ch9:', stats.ch9.join(' '));
  console.log('ch10:', stats.ch10.join(' '));
  console.log('ch11:', stats.ch11.join(' '));
  console.log('缺学习卡:', stats.noNotes.length ? stats.noNotes : '无');
  console.log('代码自测:', stats.coderead, JSON.stringify(stats.kinds), '已核验', stats.verified);
  console.log('采集说明(patched):', stats.patched);

  // 逐个打开 ch9-11 每个文件，确认学习卡与输出都渲染出来
  const problems = [];
  for (const ch of [9, 10, 11]) {
    const names = await page.evaluate(n => window.CODE_LAB.find(c => c.n === n).files.map(f => f.name), ch);
    for (const name of names) {
      await page.evaluate((n, nm) => {
        document.querySelectorAll('.lab-ch').forEach(b => { if (+b.getAttribute('data-ch') === n) b.click(); });
        const idx = window.CODE_LAB.find(c => c.n === n).files.findIndex(f => f.name === nm);
        const btns = document.querySelectorAll('.lab-file');
        if (btns[idx]) btns[idx].click();
      }, ch, name);
      await sleep(90);
      const r = await page.evaluate(() => {
        const t = document.getElementById('lab-file-title');
        const e = document.getElementById('lab-file-extra');
        return {
          title: (t && t.innerText) || '',
          hasOut: !!(e && e.querySelector('.ce-out')),
          outText: (e && e.querySelector('.ce-out') ? e.querySelector('.ce-out').innerText : ''),
          notes: (e ? e.querySelectorAll('.ce-notes li').length : 0),
          code: (document.querySelector('.lab-view') || {}).innerText || '',
        };
      });
      if (!r.title.includes('这段考什么')) problems.push(ch + '/' + name + ' 缺考点标题');
      if (!r.hasOut) problems.push(ch + '/' + name + ' 缺运行输出块');
      if (!r.notes) problems.push(ch + '/' + name + ' 缺关键注释');
      if (r.code.length < 20) problems.push(ch + '/' + name + ' 代码没渲染');
    }
  }
  console.log('逐文件检查问题:', problems.length ? problems : '无');

  // 抽查三条关键输出
  const spot = await page.evaluate(() => {
    const get = (n, nm) => {
      const f = window.CODE_LAB.find(c => c.n === n).files.find(x => x.name === nm);
      return { out: (f.output || '').slice(0, 160), err: (f.err || '').slice(0, 80) };
    };
    return {
      ch9t6: get(9, 'test6.py'),
      ch10t10: get(10, 'test10.py'),
      ch11t1: get(11, 'test1.py'),
    };
  });
  console.log('ch9/test6 输出:', JSON.stringify(spot.ch9t6));
  console.log('ch10/test10 输出:', JSON.stringify(spot.ch10t10));
  console.log('ch11/test1 输出:', JSON.stringify(spot.ch11t1));

  // 代码自测：ch9-11 新题能否正常作答
  const quizCheck = await page.evaluate(() => {
    const items = window.QUESTION_BANK.filter(q => q.type === 'coderead' && [9, 10, 11].includes(q.chapter));
    return items.map(q => ({ id: q.id, ch: q.chapter, ans: q.answer, stem: q.stem.slice(0, 26), opts: q.options.length }));
  });
  console.log('ch9-11 自测题:', JSON.stringify(quizCheck, null, 0));

  await page.screenshot({ path: 'shot-ch9-11-updated.png' });
  console.log('控制台错误:', errs.length ? errs : '无');
  await browser.close();
})().catch(e => { console.error('FAIL', e); process.exit(1); });
