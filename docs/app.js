const QUALITY_LABELS = [
  { value: 0, label: "0 — Blackout", desc: "No recollection at all" },
  { value: 1, label: "1 — Wrong", desc: "Recognized only after seeing it" },
  { value: 2, label: "2 — Wrong, familiar", desc: "Felt familiar, couldn't produce it" },
  { value: 3, label: "3 — Correct, hard", desc: "Got there, but it was a struggle" },
  { value: 4, label: "4 — Correct, hesitant", desc: "Correct after some hesitation" },
  { value: 5, label: "5 — Perfect", desc: "Immediate, confident recall" },
];

let PROGRESS = {};
let PATTERNS = {};
let PATTERNS_ORDERED = [];
let QUESTIONS = {};
let currentProblem = null;

function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

function isDue(entry) {
  if (!entry.next_review) return true;
  return entry.next_review <= todayISO();
}

function daysUntil(dateStr) {
  const diff = (new Date(dateStr) - new Date(todayISO())) / 86400000;
  return Math.round(diff);
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

async function loadProgress() {
  const [progressRes, patternsRes, questionsRes] = await Promise.all([
    fetch("progress.json", { cache: "no-store" }),
    fetch("patterns.json", { cache: "no-store" }),
    fetch("questions.json", { cache: "no-store" }),
  ]);
  PROGRESS = await progressRes.json();
  QUESTIONS = await questionsRes.json();

  const patternsData = await patternsRes.json();
  PATTERNS_ORDERED = (patternsData.topics || []).slice().sort((a, b) => a.order - b.order);
  PATTERNS = {};
  PATTERNS_ORDERED.forEach((t) => {
    PATTERNS[t.id] = t;
  });

  renderStats();
  renderList();
  renderUpNext();
}

function topicFor(entry) {
  return entry && entry.topic ? PATTERNS[entry.topic] : null;
}

function questionFor(entry) {
  return entry ? QUESTIONS[entry.number] : null;
}

function renderStats() {
  const entries = Object.values(PROGRESS);
  const due = entries.filter(isDue).length;
  const overdue = entries.filter(
    (e) => e.next_review && e.next_review < todayISO()
  ).length;
  const mastered = entries.filter((e) => e.mastery === "Mastered").length;

  document.getElementById("stats").innerHTML = `
    <div class="stat"><strong>${entries.length}</strong><span>Solved</span></div>
    <div class="stat"><strong>${due}</strong><span>Due</span></div>
    <div class="stat"><strong>${overdue}</strong><span>Overdue</span></div>
    <div class="stat"><strong>${mastered}</strong><span>Mastered</span></div>
  `;
}

function renderList() {
  const dueList = document.getElementById("due-list");
  const upcomingList = document.getElementById("upcoming-list");
  dueList.innerHTML = "";
  upcomingList.innerHTML = "";

  const entries = Object.entries(PROGRESS)
    .map(([number, entry]) => ({ number, ...entry }))
    .sort((a, b) => (a.next_review || "").localeCompare(b.next_review || ""));

  let dueCount = 0;

  entries.forEach((entry) => {
    const item = buildListItem(entry);
    if (isDue(entry)) {
      dueCount++;
      dueList.appendChild(item);
    } else {
      upcomingList.appendChild(item);
    }
  });

  document.getElementById("due-count").textContent = `(${dueCount})`;

  if (!dueList.children.length) {
    dueList.innerHTML = '<p class="empty">Nothing due right now.</p>';
  }
  if (!upcomingList.children.length) {
    upcomingList.innerHTML = '<p class="empty">No scheduled reviews yet.</p>';
  }
}

function buildListItem(entry) {
  const div = document.createElement("div");
  div.className = "problem-item";

  const overdue = entry.next_review && entry.next_review < todayISO();

  let dueLabel;
  if (!entry.next_review) {
    dueLabel = "New";
  } else if (overdue) {
    dueLabel = `Overdue ${-daysUntil(entry.next_review)}d`;
  } else if (isDue(entry)) {
    dueLabel = "Due today";
  } else {
    dueLabel = `In ${daysUntil(entry.next_review)}d`;
  }

  const difficultyClass = (entry.difficulty || "").toLowerCase();

  div.innerHTML = `
    <div class="problem-item-main">
      <span class="prob-number">#${entry.number}</span>
      <span class="prob-name">${entry.problem}</span>
      <span class="badge difficulty ${difficultyClass}">${entry.difficulty || ""}</span>
      <span class="badge pattern">${entry.pattern || ""}</span>
    </div>
    <div class="problem-item-side">
      <span class="due-label ${overdue ? "overdue" : ""}">${dueLabel}</span>
      <button class="btn-primary btn-sm">Start Review</button>
    </div>
  `;

  div.querySelector("button").addEventListener("click", () => startReview(entry.number));

  return div;
}

// -----------------------------------------------------------------
// Up Next: first pattern in the handbook's recommended order that
// none of the tracked problems belong to yet.
// -----------------------------------------------------------------

function computeNextTopic() {
  const covered = new Set(
    Object.values(PROGRESS)
      .map((e) => e.topic)
      .filter(Boolean)
  );
  return PATTERNS_ORDERED.find((t) => !covered.has(t.id)) || null;
}

function renderUpNext() {
  const container = document.getElementById("up-next-section");
  const topic = computeNextTopic();

  if (!topic) {
    container.innerHTML = "";
    return;
  }

  const ladderRows = (topic.leetcode_ladder || [])
    .map(
      (item) => `
        <a class="up-next-problem" href="${item.url || "#"}" target="_blank" rel="noopener">
          <span class="prob-number">#${item.leetcode_number}</span>
          <span class="prob-name">${item.title}</span>
          <span class="badge difficulty ${(item.difficulty || "").toLowerCase()}">${item.difficulty || ""}</span>
          <span class="up-next-tests">${item.tests || ""}</span>
        </a>`
    )
    .join("");

  container.innerHTML = `
    <h2>Up Next: New Pattern to Learn</h2>
    <div class="up-next-card">
      <div class="up-next-header">
        <span class="badge pattern">${topic.title}</span>
        <span class="up-next-order">Pattern ${topic.order} of ${PATTERNS_ORDERED.length}</span>
      </div>
      <p class="up-next-goal">${topic.goal || ""}</p>
      <h4>Practice ladder (LeetCode)</h4>
      <div class="up-next-list">${ladderRows}</div>
    </div>
  `;
}

// -----------------------------------------------------------------
// Review mode
// -----------------------------------------------------------------

function startReview(number) {
  currentProblem = { ...PROGRESS[number], number };

  document.getElementById("list-view").classList.add("hidden");
  document.getElementById("review-view").classList.remove("hidden");

  const difficultyEl = document.getElementById("rv-difficulty");
  difficultyEl.textContent = currentProblem.difficulty || "";
  difficultyEl.className = `badge difficulty ${(currentProblem.difficulty || "").toLowerCase()}`;

  document.getElementById("rv-pattern").textContent = currentProblem.pattern || "";
  document.getElementById("rv-title").textContent = `#${number} ${currentProblem.problem}`;
  document.getElementById("rv-meta").textContent =
    `Solved ${currentProblem.solved || "—"} · Reviewed ${currentProblem.reviews || 0}x · Last reviewed ${currentProblem.last_reviewed || "never"}`;

  const question = questionFor(currentProblem);
  const lcLink = document.getElementById("rv-lc-link");
  if (question && question.url) {
    lcLink.href = question.url;
    lcLink.classList.remove("hidden");
  } else {
    lcLink.classList.add("hidden");
  }

  renderProblemTab(question);
  renderPatternGuide(topicFor(currentProblem), currentProblem.leetcode_number);
  resetSolutionTab();

  switchTab("problem");
}

function switchTab(tabName) {
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.tab === tabName);
  });
  document.querySelectorAll(".tab-panel").forEach((panel) => {
    panel.classList.toggle("hidden", panel.id !== `tab-${tabName}`);
  });
}

document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => switchTab(btn.dataset.tab));
});

function renderProblemTab(question) {
  const container = document.getElementById("problem-content");

  if (!question) {
    container.innerHTML = '<p class="empty">No LeetCode statement linked for this problem yet.</p>';
    return;
  }

  const tags = (question.topic_tags || [])
    .map((t) => `<span class="badge tag">${t}</span>`)
    .join("");

  container.innerHTML = `
    <div class="problem-tags">${tags}</div>
    <div class="problem-statement">${question.content_html || ""}</div>
  `;
}

function resetSolutionTab() {
  document.getElementById("code-block").classList.add("hidden");
  document.getElementById("rating-section").classList.add("hidden");
  document.getElementById("result-section").classList.add("hidden");
  document.getElementById("result-section").innerHTML = "";

  const revealBtn = document.getElementById("reveal-btn");
  revealBtn.classList.remove("hidden");
  revealBtn.textContent = "Reveal Solution";
  revealBtn.onclick = revealSolution;
}

function renderPatternGuide(topic, leetcodeNumber) {
  const container = document.getElementById("pattern-guide");

  if (!topic) {
    container.innerHTML = '<p class="empty">No pattern linked for this problem yet.</p>';
    return;
  }

  const lcBadge = leetcodeNumber ? `<span class="badge lc">LeetCode #${leetcodeNumber}</span>` : "";
  const template = (topic.templates || [])[0];

  container.innerHTML = `
    <div class="pattern-header">
      <h3>${topic.title}</h3>
      ${lcBadge}
    </div>
    <p class="pattern-goal">${topic.goal || ""}</p>

    <h4>Recognize it when</h4>
    <ul>${(topic.recognition_signals || []).map((s) => `<li>${s}</li>`).join("")}</ul>

    <h4>Common mistakes</h4>
    <ul>${(topic.common_mistakes || []).map((s) => `<li>${s}</li>`).join("")}</ul>

    ${
      template
        ? `<h4>Template: ${template.name}</h4>
           <p class="template-note">${template.note || ""}</p>
           <pre class="code-block template-block"><code>${escapeHtml(template.code)}</code></pre>`
        : ""
    }

    <h4>Graduation requirement</h4>
    <p class="pattern-grad">${topic.graduation_requirement || ""}</p>
  `;
}

function revealSolution() {
  const codeBlock = document.getElementById("code-block");
  const codeContent = document.getElementById("code-content");

  codeContent.textContent = currentProblem.code || "No solution file linked for this problem.";
  codeBlock.classList.remove("hidden");
  document.getElementById("reveal-btn").classList.add("hidden");

  renderRatingButtons();
  document.getElementById("rating-section").classList.remove("hidden");
}

function renderRatingButtons() {
  const container = document.getElementById("rating-buttons");
  container.innerHTML = "";

  QUALITY_LABELS.forEach((q) => {
    const btn = document.createElement("button");
    btn.className = "rating-btn";
    btn.innerHTML = `<strong>${q.label}</strong><span>${q.desc}</span>`;
    btn.addEventListener("click", () => rate(q.value, btn));
    container.appendChild(btn);
  });
}

// Mirrors push.py's update_sm2() exactly, for a client-side preview.
function previewSM2(entry, quality) {
  let repetitions = entry.repetitions || 0;
  let interval = entry.interval || 1;
  let ease = entry.ease_factor || 2.5;

  if (quality < 3) {
    repetitions = 0;
    interval = 1;
  } else {
    if (repetitions === 0) interval = 1;
    else if (repetitions === 1) interval = 6;
    else interval = Math.round(interval * ease);
    repetitions += 1;
  }

  ease += 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02);
  ease = Math.max(1.3, ease);
  ease = Math.round(ease * 100) / 100;

  const next = new Date();
  next.setDate(next.getDate() + interval);

  return {
    repetitions,
    interval,
    ease_factor: ease,
    next_review: next.toISOString().slice(0, 10),
  };
}

function rate(quality, btnEl) {
  document.querySelectorAll(".rating-btn").forEach((b) => b.classList.remove("selected"));
  btnEl.classList.add("selected");

  const result = previewSM2(currentProblem, quality);

  const resultSection = document.getElementById("result-section");
  resultSection.innerHTML = `
    <p class="next-review">Next review: <strong>${result.next_review}</strong>
      (in ${result.interval} day${result.interval === 1 ? "" : "s"})</p>
    <p class="preview-note">
      This is a preview — it isn't saved here. Run <code>python push.py</code> locally,
      choose "review" for #${currentProblem.number}, and enter a rating of
      <code>${quality}</code> to record it for real, then commit &amp; push to update this site.
    </p>
  `;
  resultSection.classList.remove("hidden");
}

document.getElementById("back-btn").addEventListener("click", () => {
  document.getElementById("review-view").classList.add("hidden");
  document.getElementById("list-view").classList.remove("hidden");
  currentProblem = null;
  renderStats();
  renderList();
  renderUpNext();
});

loadProgress();
