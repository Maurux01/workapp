/* Workapp static frontend — no server. Live jobs via CORS-open public APIs. */
'use strict';

const STR = {
  es: {
    tagline: 'La forma inteligente de conseguir trabajo',
    note: 'Funciona 100% en tu navegador: ofertas remotas en vivo + tu CV nunca sale de aquí.',
    navHome: 'Inicio', navResults: 'Resultados',
    keyword: 'Palabra clave', location: 'Ubicación', search: 'Buscar', searching: 'Buscando…',
    jobType: 'Tipo de jornada', modality: 'Modalidad',
    full_time: 'Tiempo completo', part_time: 'Medio tiempo', freelance: 'Freelance', internship: 'Pasantía',
    remote: 'Remoto', onsite: 'Presencial', hybrid: 'Híbrido',
    hideSpam: 'Ocultar posible fraude', uploadCv: 'Subir CV (PDF)', analyze: 'Analizar CV',
    analyzing: 'Analizando…', cvReady: 'CV analizado', noCv: 'Sube tu PDF para medir compatibilidad.',
    results: 'Resultados', in: 'en', found: 'ofertas', match: 'compatibilidad',
    verified: 'Verificada', possibleScam: 'Posible fraude', risk: 'riesgo',
    skills: 'Habilidades', experience: 'Experiencia', viewOffer: 'Ver oferta',
    noResults: 'Sin resultados. Prueba otra palabra clave.', typeKeyword: 'Escribe una palabra clave.',
    pdfNeed: 'Elige un PDF primero.', cvFail: 'No se pudo leer el PDF.',
    sources: 'Fuentes en vivo', footer: 'Ofertas remotas en vivo de Remotive, RemoteOK, Arbeitnow, We Work Remotely y Hacker News. Tu CV se procesa solo en tu navegador.',
  },
  en: {
    tagline: 'The smart way to get a job',
    note: 'Runs 100% in your browser: live remote jobs + your CV never leaves here.',
    navHome: 'Home', navResults: 'Results',
    keyword: 'Keyword', location: 'Location', search: 'Search', searching: 'Searching…',
    jobType: 'Job type', modality: 'Workplace',
    full_time: 'Full-time', part_time: 'Part-time', freelance: 'Freelance', internship: 'Internship',
    remote: 'Remote', onsite: 'On-site', hybrid: 'Hybrid',
    hideSpam: 'Hide possible scams', uploadCv: 'Upload CV (PDF)', analyze: 'Analyze CV',
    analyzing: 'Analyzing…', cvReady: 'CV analyzed', noCv: 'Upload your PDF to measure match.',
    results: 'Results', in: 'in', found: 'jobs', match: 'match',
    verified: 'Verified', possibleScam: 'Possible scam', risk: 'risk',
    skills: 'Skills', experience: 'Experience', viewOffer: 'View job',
    noResults: 'No results. Try another keyword.', typeKeyword: 'Type a keyword.',
    pdfNeed: 'Pick a PDF first.', cvFail: 'Could not read the PDF.',
    sources: 'Live sources', footer: 'Live remote jobs from Remotive, RemoteOK, Arbeitnow, We Work Remotely and Hacker News. Your CV is processed only in your browser.',
  }
};
const JT = ['full_time', 'part_time', 'freelance', 'internship'];
const MOD = ['remote', 'onsite', 'hybrid'];
const SKILLS = ['python','javascript','java','typescript','php','html','css','sql','mongodb','postgresql','mysql','redis','docker','kubernetes','aws','azure','gcp','linux','git','react','angular','vue','django','flask','fastapi','node.js','express','pandas','numpy','tensorflow','pytorch','machine learning','data analysis','excel','power bi','tableau','figma','agile','scrum'];
const BLOCKED = ['varesdev'];
const GHOST = ['talent pool','bolsa de talento','banco de talentos','siempre estamos contratando','always hiring','join our database','futuras oportunidades','future opportunities','candidate pool','ongoing recruitment'];
const SUSPICIOUS = ['get rich quick','hazte rico','no experience needed','earn $$$','gana $$$','crypto','mlm','multinivel','whatsapp only','solo whatsapp','pay for training','fee required'];
const FREE_MAIL = ['gmail.com','yahoo.com','hotmail.com','outlook.com','live.com'];

const state = { lang: 'es', cv: null, jobs: [], q: '', loc: '' };
const $ = (id) => document.getElementById(id);
const T = (k) => (STR[state.lang] && STR[state.lang][k]) || STR.es[k] || k;
const esc = (s) => String(s || '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const stripHtml = (s) => String(s || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();

function setLang(l) {
  state.lang = (l === 'en') ? 'en' : 'es';
  document.documentElement.lang = state.lang;
  document.title = 'Workapp — ' + T('tagline');
  $('navHome').textContent = T('navHome');
  $('navResults').textContent = T('navResults');
  $('heroSub').textContent = T('tagline');
  $('heroNote').textContent = T('note');
  $('lblKeyword').textContent = T('keyword');
  $('lblLocation').textContent = T('location');
  $('legType').textContent = T('jobType');
  $('legMod').textContent = T('modality');
  $('lblHideSpam').textContent = T('hideSpam');
  $('btnSearch').textContent = T('search');
  $('lblUpload').textContent = T('uploadCv');
  $('btnAnalyze').textContent = T('analyze');
  $('cvStatus').textContent = state.cv ? cvLine(state.cv) : T('noCv');
  $('footer').textContent = T('footer');
  $('langEs').classList.toggle('active', state.lang === 'es');
  $('langEn').classList.toggle('active', state.lang === 'en');
  $('boxTypes').innerHTML = JT.map((k) => '<label class="chk"><input type="checkbox" data-jt="' + k + '"> ' + esc(T(k)) + '</label>').join('');
  $('boxMods').innerHTML = MOD.map((k) => '<label class="chk"><input type="checkbox" data-mod="' + k + '"> ' + esc(T(k)) + '</label>').join('');
  if (state.jobs.length) render(state.jobs);
  else $('resTitle').textContent = '';
}

function showError(msg) {
  const e = $('error');
  if (!msg) { e.classList.add('hidden'); e.textContent = ''; return; }
  e.textContent = msg; e.classList.remove('hidden');
}

/* ---------- fetchers (all CORS-open) ---------- */
function norm(o) {
  const blob = ((o.title || '') + ' ' + (o.description || '')).toLowerCase();
  const has = (...ws) => ws.some((w) => blob.includes(w));
  let jt = 'unknown';
  if (has('freelance', 'freelancer', 'contract', 'por proyecto', 'autónomo')) jt = 'full_time' === jt ? jt : 'freelance';
  if (has('part-time', 'part time', 'medio tiempo')) jt = 'part_time';
  if (has('intern', 'pasant', 'practicante', 'becario', 'trainee')) jt = 'internship';
  if (jt === 'unknown' && has('full-time', 'full time', 'tiempo completo')) jt = 'full_time';
  let md = 'unknown';
  if (has('remot', 'home office', 'work from home', 'teletrabajo')) md = 'remote';
  else if (has('híbrido', 'hibrido', 'hybrid')) md = 'hybrid';
  else if (has('presencial', 'on-site', 'on site')) md = 'onsite';
  return { title: o.title || '', company: o.company || '', location: o.location || '',
    description: o.description || o.title || '', url: o.url || '', source: o.source || '',
    job_type: o.job_type && o.job_type !== 'unknown' ? o.job_type : jt,
    modality: o.modality && o.modality !== 'unknown' ? o.modality : md };
}

async function fetchRemotive(kw, n) {
  const r = await fetch('https://remotive.com/api/remote-jobs?search=' + encodeURIComponent(kw) + '&limit=' + n);
  const d = await r.json();
  const map = { full_time: 'full_time', part_time: 'part_time', contract: 'freelance', freelance: 'freelance' };
  return (d.jobs || []).map((j) => norm({ title: j.title, company: j.company_name,
    location: j.candidate_required_location || 'Remote', description: stripHtml(j.description).slice(0, 2000),
    url: j.url, source: 'remotive', job_type: map[(j.job_type || '').toLowerCase()] || 'unknown', modality: 'remote' }));
}

async function fetchRemoteOK(kw, n) {
  const r = await fetch('https://remoteok.com/api');
  const d = await r.json();
  const k = kw.toLowerCase(), out = [];
  for (const j of d) {
    if (!j || !j.position) continue;
    const blob = (j.position + ' ' + (j.tags || []).join(' ') + ' ' + (j.company || '')).toLowerCase();
    if (k && !blob.includes(k)) continue;
    out.push(norm({ title: j.position, company: j.company, location: j.location || 'Remote',
      description: stripHtml(j.description).slice(0, 2000) || j.position, url: j.url,
      source: 'remoteok', modality: 'remote' }));
    if (out.length >= n) break;
  }
  return out;
}

async function fetchArbeitnow(kw, n) {
  const r = await fetch('https://www.arbeitnow.com/api/job-board-api');
  const d = await r.json();
  const k = kw.toLowerCase(), out = [];
  for (const j of (d.data || [])) {
    if (!j.remote) continue;
    const blob = (j.title + ' ' + (j.tags || []).join(' ') + ' ' + (j.company_name || '')).toLowerCase();
    if (k && !blob.includes(k)) continue;
    out.push(norm({ title: j.title, company: j.company_name, location: j.location || 'Remote',
      description: stripHtml(j.description).slice(0, 2000) || j.title, url: j.url,
      source: 'arbeitnow', modality: 'remote' }));
    if (out.length >= n) break;
  }
  return out;
}

async function fetchWWR(kw, n) {
  const r = await fetch('https://weworkremotely.com/remote-jobs.rss');
  const xml = new DOMParser().parseFromString(await r.text(), 'application/xml');
  const k = kw.toLowerCase(), out = [];
  for (const it of xml.querySelectorAll('item')) {
    const tx = (s) => (it.querySelector(s) || {}).textContent || '';
    const title = tx('title').trim(), desc = stripHtml(tx('description'));
    if (k && !(title + ' ' + desc).toLowerCase().includes(k)) continue;
    if (!title) continue;
    out.push(norm({ title, company: '', location: 'Remote', description: desc.slice(0, 2000) || title,
      url: tx('link').trim(), source: 'weworkremotely', modality: 'remote' }));
    if (out.length >= n) break;
  }
  return out;
}

async function fetchHN(kw, n) {
  const s = await (await fetch('https://hn.algolia.com/api/v1/search?query=Who%20is%20hiring&tags=story&hitsPerPage=10')).json();
  const hit = (s.hits || []).find((h) => (h.title || '').includes('Who is hiring'));
  if (!hit) return [];
  const thread = await (await fetch('https://hn.algolia.com/api/v1/items/' + hit.objectID)).json();
  const k = kw.toLowerCase(), out = [];
  for (const c of (thread.children || [])) {
    const text = stripHtml(c.text || '');
    if (k && !text.toLowerCase().includes(k)) continue;
    if (!text) continue;
    out.push(norm({ title: text.split('\n')[0].slice(0, 150), company: c.author || '',
      location: 'Remote', description: text.slice(0, 2000),
      url: 'https://news.ycombinator.com/item?id=' + c.id,
      source: 'hnhiring', job_type: 'freelance', modality: 'remote' }));
    if (out.length >= n) break;
  }
  return out;
}

/* ---------- spam / ghost / match (same rules as desktop) ---------- */
function spamDetect(j) {
  let score = 0; const reasons = [];
  const desc = (j.description || '').toLowerCase();
  const comp = (j.company || '').toLowerCase();
  for (const b of BLOCKED) if (comp.includes(b)) { score += 99; reasons.push('blocked:' + b); }
  for (const g of GHOST) if (desc.includes(g)) { score += 3; reasons.push('ghost'); break; }
  for (const s of SUSPICIOUS) if (desc.includes(s)) { score += 2; reasons.push('spam-kw'); break; }
  if (!j.company) { score += 3; reasons.push('no-company'); }
  if (desc.split(/\s+/).length < 10) { score += 2; reasons.push('short'); }
  return { is_spam: score >= 5, risk_score: score, reasons };
}

function matchCv(cv, j) {
  if (!cv) return null;
  const cvSkills = new Set(cv.skills.map((s) => s.toLowerCase()));
  const text = ((j.title || '') + ' ' + (j.description || '')).toLowerCase();
  const matched = [...cvSkills].filter((s) => text.includes(s));
  return { score: Math.min(100, Math.round(matched.length * 15)), matched };
}

/* ---------- CV via pdf.js ---------- */
async function analyzeCv(file) {
  const buf = await file.arrayBuffer();
  const pdf = await window.pdfjsLib.getDocument({ data: buf }).promise;
  let text = '';
  for (let p = 1; p <= Math.min(pdf.numPages, 6); p++) {
    const page = await pdf.getPage(p);
    const tc = await page.getTextContent();
    text += tc.items.map((i) => i.str).join(' ') + '\n';
  }
  const low = text.toLowerCase();
  const emails = low.match(/[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+/g) || [];
  const skills = SKILLS.filter((s) => low.includes(s));
  const m = low.match(/(\d+)\+?\s*(years|años|anos)/);
  return { email: emails[0] || '', skills,
    experience: m ? m[1] + '+ years' : '—', text: text.slice(0, 6000) };
}
function cvLine(cv) {
  return T('cvReady') + ': ' + cv.email + ' · ' + T('experience') + ': ' + cv.experience + ' · ' + cv.skills.slice(0, 10).join(', ');
}

/* ---------- search + render ---------- */
function cacheGet(key) {
  try {
    const c = JSON.parse(localStorage.getItem('workapp_' + key) || 'null');
    if (c && Date.now() - c.ts < 24 * 3600 * 1000) return c.jobs;
  } catch (e) { /* ignore */ }
  return null;
}
function cacheSet(key, jobs) {
  try { localStorage.setItem('workapp_' + key, JSON.stringify({ ts: Date.now(), jobs })); }
  catch (e) { /* ignore */ }
}

async function search() {
  const kw = $('inKeyword').value.trim();
  const loc = $('inLocation').value.trim() || 'Colombia';
  if (!kw) { showError(T('typeKeyword')); return; }
  showError(null);
  const jt = [...document.querySelectorAll('[data-jt]:checked')].map((c) => c.dataset.jt);
  const md = [...document.querySelectorAll('[data-mod]:checked')].map((c) => c.dataset.mod);
  const hide = $('inHideSpam').checked;
  const btn = $('btnSearch');
  btn.disabled = true;
  btn.innerHTML = '<span class="spin"></span>' + esc(T('searching'));
  state.q = kw; state.loc = loc;
  try {
    const key = [kw, loc, jt.sort().join(','), md.sort().join(',')].join('|');
    let jobs = cacheGet(key);
    if (!jobs) {
      const res = await Promise.allSettled([
        fetchRemotive(kw, 20), fetchRemoteOK(kw, 20), fetchArbeitnow(kw, 20),
        fetchWWR(kw, 20), fetchHN(kw, 20)]);
      jobs = [];
      for (const r of res) if (r.status === 'fulfilled') jobs.push(...r.value);
      // dedupe
      const seen = new Set();
      jobs = jobs.filter((j) => {
        const k = (j.title + '|' + j.company + '|' + j.url).toLowerCase();
        if (seen.has(k)) return false;
        seen.add(k); return true;
      });
      cacheSet(key, jobs);
    }
    let out = jobs.filter((j) => {
      if (jt.length && j.job_type !== 'unknown' && !jt.includes(j.job_type)) return false;
      if (md.length && j.modality !== 'unknown' && !md.includes(j.modality)) return false;
      return true;
    }).map((j) => ({ ...j, spam: spamDetect(j) }));
    if (hide) out = out.filter((j) => !j.spam.is_spam);
    if (state.cv) out = out.map((j) => ({ ...j, m: matchCv(state.cv, j) }))
      .sort((a, b) => (b.m ? b.m.score : 0) - (a.m ? a.m.score : 0));
    state.jobs = out;
    render(out);
  } catch (e) {
    showError(String(e && e.message || e));
  } finally {
    btn.disabled = false;
    btn.textContent = T('search');
  }
}

function render(jobs) {
  $('resTitle').textContent = T('results') + ' "' + state.q + '" ' + T('in') + ' ' + state.loc + ' (' + jobs.length + ')';
  const box = $('results');
  if (!jobs.length) { box.innerHTML = '<p>' + esc(T('noResults')) + '</p>'; return; }
  box.innerHTML = jobs.map((j) => {
    const badges =
      (j.m ? '<span class="badge">' + j.m.score + '% ' + esc(T('match')) + '</span>' : '') +
      (j.job_type && j.job_type !== 'unknown' ? '<span class="badge gray">' + esc(T(j.job_type)) + '</span>' : '') +
      (j.modality && j.modality !== 'unknown' ? '<span class="badge gray">' + esc(T(j.modality)) + '</span>' : '') +
      (j.spam.is_spam
        ? '<span class="badge danger">' + esc(T('possibleScam')) + ' (' + esc(T('risk')) + ' ' + j.spam.risk_score + ')</span>'
        : '<span class="badge ok">✓ ' + esc(T('verified')) + '</span>');
    return '<div class="card job"><div class="job-head"><b>' + esc(j.title) + '</b><br>' + badges + '</div>' +
      '<div class="muted">' + esc([j.company, j.location, j.source].filter(Boolean).join(' · ')) + '</div>' +
      (j.m && j.m.matched.length ? '<div class="skills">' + esc(T('skills')) + ': ' + esc(j.m.matched.join(', ')) + '</div>' : '') +
      '<p>' + esc((j.description || '').slice(0, 280)) + '</p>' +
      (j.url ? '<a class="btn" href="' + esc(j.url) + '" target="_blank" rel="noopener">' + esc(T('viewOffer')) + ' →</a>' : '') +
      '</div>';
  }).join('');
  document.querySelector('#results').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* ---------- wire ---------- */
window.addEventListener('DOMContentLoaded', () => {
  if (window.pdfjsLib && window.pdfjsLib.GlobalWorkerOptions) {
    window.pdfjsLib.GlobalWorkerOptions.workerSrc =
      'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
  }
  $('langEs').onclick = () => setLang('es');
  $('langEn').onclick = () => setLang('en');
  $('btnSearch').onclick = search;
  $('inKeyword').addEventListener('keydown', (e) => { if (e.key === 'Enter') search(); });
  $('navHome').onclick = (e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); };
  $('navResults').onclick = (e) => { e.preventDefault(); document.querySelector('#results').scrollIntoView({ behavior: 'smooth' }); };
  $('btnAnalyze').onclick = async () => {
    const f = $('inCv').files[0];
    if (!f) { showError(T('pdfNeed')); return; }
    showError(null);
    $('btnAnalyze').disabled = true;
    $('cvStatus').textContent = T('analyzing');
    try {
      const cv = await analyzeCv(f);
      state.cv = cv;
      $('cvStatus').textContent = cvLine(cv);
      const box = $('cvBox');
      box.classList.remove('hidden');
      box.innerHTML = '<b>' + esc(T('cvReady')) + ':</b> ' + esc(cv.email) + ' · ' +
        esc(T('experience')) + ': ' + esc(cv.experience) + ' · ' + esc(cv.skills.slice(0, 10).join(', '));
      if (state.jobs.length) {
        state.jobs = state.jobs.map((j) => ({ ...j, m: matchCv(cv, j) }))
          .sort((a, b) => (b.m ? b.m.score : 0) - (a.m ? a.m.score : 0));
        render(state.jobs);
      }
    } catch (e) {
      showError(T('cvFail'));
      $('cvStatus').textContent = T('noCv');
    } finally {
      $('btnAnalyze').disabled = false;
    }
  };
  setLang('es');
});
