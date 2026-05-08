// ─── Samples ─────────────────────────────────────────────────────────────────
const SAMPLES = {
  ai: [
    "Furthermore, it is important to note that artificial intelligence plays a crucial role in modern technological advancement. Leveraging these comprehensive solutions enables robust paradigm shifts across multiple domains. It is worth noting that the utilization of these methodologies yields substantial improvements in operational efficiency.",
    "In conclusion, the integration of machine learning algorithms into enterprise workflows provides substantial competitive advantages. As mentioned in previous analyses, these systems demonstrate remarkable capabilities in processing complex datasets. Additionally, the implementation of neural networks offers a comprehensive framework for understanding intricate patterns.",
    "The multifaceted nature of climate change necessitates a holistic and comprehensive approach to mitigation. Furthermore, the intricate interplay of various environmental factors contributes significantly to the overall complexity of the situation. It should be noted that robust international cooperation frameworks are absolutely essential for achieving meaningful progress."
  ],
  human: [
    "ok so I tried making that pasta recipe you sent me and honestly?? it was NOT great lol. I think I added way too much salt but also the sauce was really watery. idk what I did wrong but my roommate was too polite to say anything which made it worse",
    "Just got back from the dentist. Two cavities. TWO. I brush my teeth literally every single day, this is so unfair. Also the waiting room had the most depressing music playing the entire time I was there.",
    "Can't believe it's already Friday, this week absolutely flew by. Met up with Jake for coffee and we ended up talking for like 3 hours about everything and nothing. I forgot how much I missed just hanging out without any agenda."
  ]
};

const DATASET_SAMPLES = [
  { text: "Furthermore, it is important to note that artificial intelligence plays a crucial role in modern technological advancement. Leveraging these comprehensive solutions enables robust paradigm shifts.", label: "ai" },
  { text: "In conclusion, the utilization of machine learning algorithms provides substantial benefits. It is worth noting that these systems demonstrate remarkable capabilities in data processing.", label: "ai" },
  { text: "The multifaceted nature of this phenomenon necessitates a holistic approach. Furthermore, the intricate interplay of various factors contributes to the overall complexity.", label: "ai" },
  { text: "It should be noted that climate change represents one of the most significant challenges facing humanity. Robust mitigation strategies are absolutely essential for addressing this critical issue.", label: "ai" },
  { text: "As a result of these developments, it becomes increasingly clear that digital transformation is a fundamental business necessity in today's competitive landscape.", label: "ai" },
  { text: "The synthesis of available evidence suggests that multimodal learning approaches yield superior outcomes. Comprehensive implementation strategies must therefore be developed and executed carefully.", label: "ai" },
  { text: "Certainly, the strategic alignment of organizational objectives with technological capabilities represents a cornerstone of successful digital transformation initiatives.", label: "ai" },
  { text: "Of course, stakeholder engagement plays a pivotal role in ensuring the successful implementation of transformative initiatives. Comprehensive communication strategies are therefore absolutely essential.", label: "ai" },
  { text: "The empirical evidence unequivocally demonstrates that proactive risk management frameworks significantly enhance organizational resilience and operational effectiveness.", label: "ai" },
  { text: "In summary, the intersection of artificial intelligence and healthcare presents remarkable opportunities for improving patient outcomes through personalized medical interventions.", label: "ai" },
  { text: "The paradigmatic shift toward remote work environments has necessitated the development of more sophisticated digital collaboration tools to address diverse user needs.", label: "ai" },
  { text: "I was so tired yesterday I literally fell asleep on my keyboard. Woke up with 'gggggggg' in my email draft to my boss. Not my finest moment honestly.", label: "human" },
  { text: "ok so I tried making that pasta recipe you sent me and it was... not great? I think I added too much salt but also the sauce was kinda watery. idk what went wrong", label: "human" },
  { text: "Can't believe it's already Friday! This week absolutely flew by. Met up with Jake for coffee and we ended up talking for like 3 hours about everything and nothing.", label: "human" },
  { text: "Just got back from the dentist. Two cavities. TWO. I brush my teeth every day, this is honestly so unfair. Also the waiting room had the most depressing music playing.", label: "human" },
  { text: "my dog did the funniest thing this morning - she brought me my shoe and just sat there staring at me like 'are we going or what?' she's honestly smarter than me", label: "human" },
  { text: "FINALLY finished that book I've been reading for like 6 months. The ending was not what I expected at all - kinda disappointed but also impressed by the twist.", label: "human" },
  { text: "Had the worst commute today. Train was delayed 40 minutes, then some guy spilled his coffee on my jacket. Just one of those days I guess.", label: "human" },
  { text: "My mom called three times while I was in a meeting. Called back and she just wanted to tell me about a bird that landed on her porch. I love her so much.", label: "human" },
  { text: "Started learning guitar two weeks ago and I'm... not good. My fingers hurt constantly and my cat leaves the room every time I practice. Baby steps I guess!", label: "human" },
  { text: "Just realized I've been mispronouncing 'quinoa' for years. Like years. Had a whole conversation at a dinner party last week. Nobody corrected me.", label: "human" },
];

// ─── State ────────────────────────────────────────────────────────────────────
let currentSection = 'detector';

// ─── Navigation ───────────────────────────────────────────────────────────────
function showSection(name) {
  document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
  document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
  document.getElementById('sec-' + name).style.display = 'block';
  document.querySelectorAll('.pill').forEach(p => {
    if (p.textContent.toLowerCase() === name) p.classList.add('active');
  });
  currentSection = name;
  if (name === 'dataset') loadDatasetSection();
}

// ─── Text input live counters ─────────────────────────────────────────────────
document.getElementById('textInput').addEventListener('input', function () {
  const text = this.value;
  const chars = text.length;
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  document.getElementById('charCount').textContent = chars + ' chars';
  document.getElementById('wordCount').textContent = words + ' words';
});

// ─── Load sample ──────────────────────────────────────────────────────────────
function loadSample(type) {
  const arr = SAMPLES[type];
  const text = arr[Math.floor(Math.random() * arr.length)];
  const ta = document.getElementById('textInput');
  ta.value = '';
  let i = 0;
  const interval = setInterval(() => {
    ta.value += text[i++];
    ta.dispatchEvent(new Event('input'));
    if (i >= text.length) clearInterval(interval);
  }, 10);
}

// ─── Clear ────────────────────────────────────────────────────────────────────
function clearAll() {
  document.getElementById('textInput').value = '';
  document.getElementById('textInput').dispatchEvent(new Event('input'));
  document.getElementById('resultPanel').querySelector('.result-idle').style.display = 'flex';
  const ra = document.getElementById('resultActive');
  ra.style.display = 'none';
}

// ─── Analyse ──────────────────────────────────────────────────────────────────
async function analyse() {
  const text = document.getElementById('textInput').value.trim();
  if (!text) { showToast('Please enter some text first.'); return; }
  if (text.length < 20) { showToast('Text too short — enter at least 20 characters.'); return; }

  showLoading(true);

  try {
    const res = await fetch('/api/detect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    if (!res.ok) { showToast(data.error || 'Error analysing text.'); return; }
    showResult(data);
  } catch (e) {
    showToast('Network error — is the server running?');
  } finally {
    showLoading(false);
  }
}

// ─── Show result ──────────────────────────────────────────────────────────────
function showResult(data) {
  const isAI = data.label === 'ai';
  const score = data.score;         // 0–1, higher = more AI
  const conf  = data.confidence;    // 0–100

  // Hide idle, show active
  document.querySelector('.result-idle').style.display = 'none';
  const ra = document.getElementById('resultActive');
  ra.style.display = 'flex';

  // Verdict
  const vt = document.getElementById('verdictText');
  vt.textContent = isAI ? 'AI GENERATED' : 'HUMAN WRITTEN';
  vt.className = 'verdict-text ' + (isAI ? 'is-ai' : 'is-human');

  // Confidence bar
  const barColor = isAI
    ? 'linear-gradient(90deg,#ff6688,#ff3366)'
    : 'linear-gradient(90deg,#00ccff,#00ff88)';
  const bar = document.getElementById('confBar');
  bar.style.width = '0%';
  bar.style.background = barColor;
  setTimeout(() => { bar.style.width = conf + '%'; }, 50);
  document.getElementById('confValue').textContent = conf.toFixed(1) + '% confident';
  document.getElementById('confValue').style.color = isAI ? 'var(--danger)' : 'var(--accent)';

  // Dial — arc length = 251 px (semicircle)
  const offset = 251 - (score * 251);
  setTimeout(() => {
    document.getElementById('dialArc').style.strokeDashoffset = offset;
    document.getElementById('dialScore').textContent = (score * 100).toFixed(0) + '%';
    document.getElementById('dialScore').style.fill = isAI ? '#ff3366' : '#00ff88';
  }, 100);

  // Stats
  document.getElementById('nbScore').textContent   = (data.nb_score * 100).toFixed(1) + '%';
  document.getElementById('heurScore').textContent = (data.heuristic * 100).toFixed(1) + '%';
  document.getElementById('wordCountResult').textContent = data.word_count;
  document.getElementById('charCountResult').textContent = data.char_count;

  // Signal bars
  renderSignalBars(score, isAI);

  // Flash the panel
  const panel = document.querySelector('.result-panel');
  panel.style.borderColor = isAI ? 'rgba(255,51,102,0.5)' : 'rgba(0,255,136,0.5)';
  panel.style.boxShadow   = isAI
    ? '0 0 30px rgba(255,51,102,0.2)'
    : '0 0 30px rgba(0,255,136,0.2)';
  setTimeout(() => {
    panel.style.borderColor = '';
    panel.style.boxShadow = '';
    panel.style.transition = 'border-color 1.5s, box-shadow 1.5s';
  }, 1500);
}

function renderSignalBars(score, isAI) {
  const container = document.getElementById('signalBars');
  container.innerHTML = '';
  const barCount = 24;
  for (let i = 0; i < barCount; i++) {
    const bar = document.createElement('div');
    bar.className = 'signal-bar';
    const h = 8 + Math.random() * 24;
    bar.style.height = h + 'px';
    const t = i / barCount;
    const active = isAI ? t < score : t > score;
    bar.style.background = active
      ? (isAI ? 'var(--danger)' : 'var(--accent)')
      : 'rgba(255,255,255,0.07)';
    bar.style.opacity = active ? (0.5 + t * 0.5) : 0.15;
    bar.style.animationDelay = (i * 0.025) + 's';
    container.appendChild(bar);
  }
}

// ─── Loading ──────────────────────────────────────────────────────────────────
function showLoading(show) {
  document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
}

// ─── Toast ────────────────────────────────────────────────────────────────────
function showToast(msg) {
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

// ─── Dataset section ──────────────────────────────────────────────────────────
async function loadDatasetSection() {
  // Fetch stats
  try {
    const res  = await fetch('/api/dataset/stats');
    const data = await res.json();
    document.getElementById('datasetStats').innerHTML = `
      <div class="ds-stat"><div class="n">${data.total}</div><div class="l">TOTAL SAMPLES</div></div>
      <div class="ds-stat"><div class="n" style="color:var(--danger)">${data.ai}</div><div class="l">AI SAMPLES</div></div>
      <div class="ds-stat"><div class="n">${data.human}</div><div class="l">HUMAN SAMPLES</div></div>
      <div class="ds-stat"><div class="n" style="color:var(--accent2)">${data.vocab}</div><div class="l">VOCAB SIZE</div></div>
    `;
  } catch(e) {}

  // Render samples
  const grid = document.getElementById('sampleGrid');
  if (grid.children.length) return; // already loaded
  DATASET_SAMPLES.forEach(s => {
    const div = document.createElement('div');
    div.className = `sample-item ${s.label}-sample`;
    div.innerHTML = `
      <span class="sample-badge ${s.label}-badge">${s.label.toUpperCase()}</span>
      <div class="sample-text">${s.text}</div>
    `;
    div.addEventListener('click', () => {
      showSection('detector');
      document.getElementById('textInput').value = s.text;
      document.getElementById('textInput').dispatchEvent(new Event('input'));
    });
    grid.appendChild(div);
  });
}

// ─── Copy run instructions ────────────────────────────────────────────────────
function copyInstructions() {
  const text = `cd ai-detector\npip install flask flask-cors\npython app.py\n# Open http://localhost:5000`;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector('.copy-btn');
    btn.textContent = 'COPIED!';
    btn.style.color = 'var(--accent)';
    setTimeout(() => { btn.textContent = 'COPY'; btn.style.color = ''; }, 2000);
  });
}

// ─── Keyboard shortcut (Ctrl+Enter) ──────────────────────────────────────────
document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') analyse();
});

// ─── Entry animation ──────────────────────────────────────────────────────────
window.addEventListener('load', () => {
  document.querySelectorAll('.hero-text > *').forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = `opacity 0.6s ease ${i * 0.15}s, transform 0.6s ease ${i * 0.15}s`;
    setTimeout(() => {
      el.style.opacity = '';
      el.style.transform = '';
    }, 50);
  });
});
