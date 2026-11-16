/* 校验 ch8 选择题(5) 选项是否完整、答案判定是否正确；顺带全库扫空选项 */
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: 'new',
    args: ['--no-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1100, height: 900 });
  const url = 'http://127.0.0.1:8765/index.html';
  await page.goto(url, { waitUntil: 'networkidle2' });

  // 1) 全库静态检查：任何单选题都不能有"只有标点没有内容"的选项
  const bankBad = await page.evaluate(() => {
    const bad = [];
    (window.QUESTION_BANK || []).forEach(q => {
      if (!q.options) return;
      q.options.forEach(o => {
        if (!/^[A-Za-z][.、．)]\s*\S/.test(String(o).trim())) {
          bad.push({ id: q.id, opt: JSON.stringify(o) });
        }
      });
    });
    return bad;
  });
  console.log('全库废选项数:', bankBad.length, JSON.stringify(bankBad));

  // 2) 打开第8章单选题，翻到目标题
  await page.evaluate(() => {
    localStorage.clear();
    window.QuizApp.showPractice({ chapter: 8, type: 'single', examOnly: false });
  });
  await new Promise(r => setTimeout(r, 400));

  let found = false;
  for (let i = 0; i < 20; i++) {
    const stem = await page.$eval('.stem', el => el.textContent);
    if (stem.includes('C类继承A类和B类')) { found = true; break; }
    await page.click('#btn-next');
    await new Promise(r => setTimeout(r, 250));
  }
  console.log('找到目标题:', found);

  const opts = await page.$$eval('#opts .opt', els => els.map(e => ({
    letter: e.getAttribute('data-letter'),
    text: e.innerText.trim()
  })));
  console.log('选项数:', opts.length);
  opts.forEach(o => console.log('  ', o.letter, '->', JSON.stringify(o.text)));
  console.log('空选项:', opts.filter(o => !o.text || o.text.replace(/^[A-Za-z][.、．)]/, '').trim() === '').length);

  // 3) 先答错（选 B：class C(A,B) 少冒号）
  await page.click('#opts .opt[data-letter="B"]');
  await page.click('#btn-submit');
  await new Promise(r => setTimeout(r, 400));
  const wrongVerdict = await page.evaluate(() => {
    const el = document.querySelector('.verdict');
    return el ? el.innerText.trim() : '(未找到反馈元素)';
  });
  console.log('选 B 后反馈:', JSON.stringify(wrongVerdict.slice(0, 120)));

  // 4) 再答对（选 C）
  await page.evaluate(() => { localStorage.clear(); });
  await page.reload({ waitUntil: 'networkidle2' });
  await page.evaluate(() => window.QuizApp.showPractice({ chapter: 8, type: 'single', examOnly: false }));
  await new Promise(r => setTimeout(r, 400));
  for (let i = 0; i < 20; i++) {
    const stem = await page.$eval('.stem', el => el.textContent);
    if (stem.includes('C类继承A类和B类')) break;
    await page.click('#btn-next');
    await new Promise(r => setTimeout(r, 250));
  }
  await page.click('#opts .opt[data-letter="C"]');
  await page.click('#btn-submit');
  await new Promise(r => setTimeout(r, 400));
  const rightVerdict = await page.evaluate(() => {
    const el = document.querySelector('.verdict');
    return el ? el.innerText.trim() : '(未找到反馈元素)';
  });
  console.log('选 C 后反馈:', JSON.stringify(rightVerdict.slice(0, 160)));

  // 5) 「不会·看答案」应展示 C 的完整选项文本
  const peeked = await page.evaluate(() => {
    window.QuizApp.peekAnswer();
    return document.body.innerText.includes('class C(A,B):');
  });
  console.log('看答案含完整 C 选项:', peeked);

  await page.screenshot({ path: 'shot-ch8q5-fixed.png' });
  await browser.close();
})().catch(e => { console.error('FAIL', e); process.exit(1); });
