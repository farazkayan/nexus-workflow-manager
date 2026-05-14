const API = "http://127.0.0.1:57832";
const DEBUG = false;

const statusDot = document.getElementById('status-dot');
const listEl = document.getElementById('list');
const errorEl = document.getElementById('error-state');
const btnSave = document.getElementById('btn-save');
const inputGroup = document.getElementById('name-input-group');
const inName = document.getElementById('in-name');
const btnCreate = document.getElementById('btn-create');
const btnRetry = document.getElementById('btn-retry');
const toastEl = document.getElementById('toast');

let toastTimer;
function showToast(msg, type = "success") {
    toastEl.textContent = msg;
    toastEl.className = `toast ${type} show`;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.className = 'toast', 2500);
}

function showError() {
    statusDot.className = 'status-dot';
    listEl.style.display = 'none';
    errorEl.style.display = 'flex';
}

function hideError() {
    statusDot.className = 'status-dot connected';
    listEl.style.display = 'block';
    errorEl.style.display = 'none';
}

function renderWorkflows(workflows) {
    listEl.innerHTML = '';
    const entries = Object.entries(workflows).map(([name, data]) => ({ name, ...data }));
    
    entries.sort((a, b) => {
        if (a.pinned !== b.pinned) return b.pinned ? 1 : -1;
        return a.name.localeCompare(b.name);
    });

    if (entries.length === 0) {
        listEl.innerHTML = '<div style="text-align:center; padding: 20px; color: var(--text3); font-size: 13px;">No workflows found.</div>';
        return;
    }

    entries.forEach(w => {
        const card = document.createElement('div');
        card.className = 'card';
        card.setAttribute('data-name', w.name);
        
        card.innerHTML = `
            <div class="c-emoji">${w.emoji || '🚀'}</div>
            <div class="c-name">${w.name}</div>
            <div class="c-count">${w.item_count} items</div>
        `;
        
        card.addEventListener('click', () => launchWorkflow(w.name, card));
        listEl.appendChild(card);
    });
}

async function launchWorkflow(name, cardEl) {
    if (cardEl) cardEl.classList.add('loading');
    try {
        const res = await fetch(API + "/launch", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name })
        });
        if (!res.ok) throw new Error("Failed");
        showToast("✅ Launched " + name, "success");
    } catch (e) {
        showToast("❌ Nexus not running", "error");
        showError();
    } finally {
        if (cardEl) cardEl.classList.remove('loading');
    }
}

async function fetchWorkflows() {
    try {
        const res = await fetch(API + "/workflows", { signal: AbortSignal.timeout(2000) });
        if (!res.ok) throw new Error("API Error");
        const data = await res.json();
        
        // Update cache
        chrome.storage.local.set({ cached_workflows: data.workflows, cache_time: Date.now() });
        
        hideError();
        renderWorkflows(data.workflows);
    } catch (e) {
        showError();
    }
}

async function createWorkflow() {
    const name = inName.value.trim() || "Chrome Session";
    
    try {
        const tabs = await chrome.tabs.query({ currentWindow: true });
        const urls = tabs.map(t => t.url).filter(u => u && u.startsWith("http"));
        
        if (urls.length === 0) {
            showToast("❌ No valid URLs", "error");
            return;
        }

        const res = await fetch(API + "/create-workflow", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, urls })
        });
        
        if (!res.ok) throw new Error("Failed");
        
        showToast("✅ Workflow created", "success");
        inputGroup.classList.remove('visible');
        inName.value = '';
        fetchWorkflows();
    } catch (e) {
        showToast("❌ Nexus not running", "error");
        showError();
    }
}

// Events
btnSave.addEventListener('click', () => {
    inputGroup.classList.toggle('visible');
    if (inputGroup.classList.contains('visible')) inName.focus();
});

btnCreate.addEventListener('click', createWorkflow);
inName.addEventListener('keydown', e => {
    if (e.key === 'Enter') createWorkflow();
    if (e.key === 'Escape') inputGroup.classList.remove('visible');
});

btnRetry.addEventListener('click', () => {
    listEl.innerHTML = `
        <div class="card skeleton"></div>
        <div class="card skeleton"></div>
        <div class="card skeleton"></div>
    `;
    hideError();
    fetchWorkflows();
});

// Init
document.addEventListener('DOMContentLoaded', async () => {
    async function checkStatus() {
        try {
            const r = await fetch(API + "/status", {signal: AbortSignal.timeout(1500)});
            const d = await r.json();
            if (d.status === "running") {
                statusDot.className = "status-dot connected";
                statusDot.title = "Nexus is running";
                return true;
            }
        } catch {}
        statusDot.className = "status-dot";
        statusDot.title = "Nexus is not running";
        showError();
        return false;
    }

    const isRunning = await checkStatus();
    if (isRunning) {
        chrome.storage.local.get(['cached_workflows', 'cache_time'], (res) => {
            if (res.cached_workflows && res.cache_time && (Date.now() - res.cache_time < 30000)) {
                hideError();
                renderWorkflows(res.cached_workflows);
            }
            fetchWorkflows();
        });
    }
});
