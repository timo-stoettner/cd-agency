// CD Agency Figma Plugin — UI Thread
// Runs in an iframe, communicates with code.ts via postMessage

const API_URL_KEY = 'cd-agency-api-url';
const HISTORY_KEY = 'cd-agency-history';

interface AgentSummary {
  name: string;
  slug: string;
  description: string;
  tags: string[];
}

interface RunResult {
  content: string;
  agent_name: string;
  model: string;
  tokens: { input: number; output: number };
  score?: {
    readability?: { grade: number; ease: number; grade_label: string };
    a11y?: { passed: boolean; issues: number };
  };
}

interface HistoryEntry {
  timestamp: string;
  agent: string;
  original: string;
  result: string;
}

let agents: AgentSummary[] = [];
let selectedAgent = '';
let currentText = '';
let apiUrl = localStorage.getItem(API_URL_KEY) || 'http://localhost:8000';

// Listen for messages from code.ts (main Figma thread)
window.onmessage = async (event: MessageEvent) => {
  const msg = event.data.pluginMessage;
  if (!msg) return;

  if (msg.type === 'selection-text') {
    currentText = msg.text;
    (document.getElementById('original-text') as HTMLElement).textContent = msg.text;
    showScreen('agent-picker');
    autoSuggestAgent(msg.text);
  }

  if (msg.type === 'no-selection') {
    showScreen('no-selection');
  }
};

// Screen management
function showScreen(id: string) {
  document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
  const screen = document.getElementById(id);
  if (screen) screen.classList.add('active');
}

// Auto-suggest an agent based on text content
function autoSuggestAgent(text: string) {
  const lower = text.toLowerCase();
  if (lower.includes('error') || lower.includes('failed') || lower.includes('wrong')) {
    selectedAgent = 'error-message-architect';
  } else if (lower.length < 40) {
    selectedAgent = 'cta-optimization-specialist';
  } else if (lower.includes('welcome') || lower.includes('get started')) {
    selectedAgent = 'onboarding-flow-designer';
  } else {
    selectedAgent = 'microcopy-review-agent';
  }

  const select = document.getElementById('agent-select') as HTMLSelectElement;
  if (select) select.value = selectedAgent;
}

// Fetch agents from API
async function fetchAgents() {
  try {
    const res = await fetch(`${apiUrl}/api/v1/agents`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    agents = await res.json();
    populateAgentDropdown();
  } catch (e) {
    console.error('Failed to fetch agents:', e);
    showScreen('setup');
  }
}

function populateAgentDropdown() {
  const select = document.getElementById('agent-select') as HTMLSelectElement;
  if (!select) return;
  select.innerHTML = '';
  for (const agent of agents) {
    const opt = document.createElement('option');
    opt.value = agent.slug;
    opt.textContent = agent.name;
    select.appendChild(opt);
  }
}

// Run agent
async function runAgent() {
  const select = document.getElementById('agent-select') as HTMLSelectElement;
  const preset = document.getElementById('preset-select') as HTMLSelectElement;
  const slug = select?.value || selectedAgent;

  if (!slug || !currentText) return;

  showScreen('loading');

  try {
    // Run agent
    const runRes = await fetch(`${apiUrl}/api/v1/agents/${slug}/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        input: { text: currentText },
        preset: preset?.value || null,
      }),
    });

    if (!runRes.ok) throw new Error(`Agent run failed: HTTP ${runRes.status}`);
    const result: RunResult = await runRes.json();

    // Also score the result
    let score = null;
    try {
      const scoreRes = await fetch(`${apiUrl}/api/v1/score/all`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: result.content }),
      });
      if (scoreRes.ok) score = await scoreRes.json();
    } catch (_) { /* scoring is optional */ }

    displayResults(result, score);
    saveHistory(slug, currentText, result.content);
  } catch (e: any) {
    showScreen('agent-picker');
    const err = document.getElementById('error-msg');
    if (err) {
      err.textContent = e.message || 'Something went wrong';
      err.style.display = 'block';
      setTimeout(() => err.style.display = 'none', 5000);
    }
  }
}

function displayResults(result: RunResult, score: any) {
  (document.getElementById('result-agent-name') as HTMLElement).textContent = result.agent_name;
  (document.getElementById('result-original') as HTMLElement).textContent = currentText;
  (document.getElementById('result-content') as HTMLElement).textContent = result.content;

  // Scores
  const scoreEl = document.getElementById('result-scores') as HTMLElement;
  if (score && scoreEl) {
    const parts: string[] = [];
    if (score.readability) {
      parts.push(`Grade ${score.readability.flesch_kincaid_grade}`);
    }
    if (score.a11y) {
      parts.push(score.a11y.passed ? 'A11y: Pass' : `A11y: ${score.a11y.issue_count} issues`);
    }
    if (score.lint) {
      const issues = score.lint.total_issues || 0;
      parts.push(issues === 0 ? 'Lint: Clean' : `Lint: ${issues} issues`);
    }
    scoreEl.textContent = parts.join(' | ');
  }

  showScreen('results');
}

// Apply text back to Figma
function applyText() {
  const content = (document.getElementById('result-content') as HTMLElement).textContent || '';
  parent.postMessage({ pluginMessage: { type: 'apply-text', text: content } }, '*');
}

// Copy to clipboard
function copyText() {
  const content = (document.getElementById('result-content') as HTMLElement).textContent || '';
  navigator.clipboard.writeText(content);
  const btn = document.getElementById('btn-copy') as HTMLElement;
  if (btn) {
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 1500);
  }
}

// History
function saveHistory(agent: string, original: string, result: string) {
  const history: HistoryEntry[] = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
  history.unshift({ timestamp: new Date().toISOString(), agent, original, result });
  if (history.length > 20) history.length = 20;
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
}

// Save API URL
function saveApiUrl() {
  const input = document.getElementById('api-url-input') as HTMLInputElement;
  if (input?.value) {
    apiUrl = input.value.replace(/\/$/, '');
    localStorage.setItem(API_URL_KEY, apiUrl);
    fetchAgents();
  }
}

// Run another agent on the same text
function runAnother() {
  showScreen('agent-picker');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  // Bind buttons
  document.getElementById('btn-run')?.addEventListener('click', runAgent);
  document.getElementById('btn-apply')?.addEventListener('click', applyText);
  document.getElementById('btn-copy')?.addEventListener('click', copyText);
  document.getElementById('btn-save-url')?.addEventListener('click', saveApiUrl);
  document.getElementById('btn-run-another')?.addEventListener('click', runAnother);

  // Set current API URL
  const urlInput = document.getElementById('api-url-input') as HTMLInputElement;
  if (urlInput) urlInput.value = apiUrl;

  // Try to load agents
  fetchAgents();
});
