const API = "http://127.0.0.1:57832";

const params = new URLSearchParams(window.location.search);
const targetUrl = params.get("url") || "";
const errorParam = params.get("error");

const errorState = document.getElementById("error-state");
const contentArea = document.getElementById("content-area");
const urlDisplay = document.getElementById("url-display");
const listEl = document.getElementById("list");
const emptyState = document.getElementById("empty-state");
const searchInput = document.getElementById("search-input");
const btnClose = document.getElementById("btn-close");
const btnCancel = document.getElementById("btn-cancel");

let allWorkflows = [];

urlDisplay.textContent = targetUrl;
urlDisplay.title = targetUrl;

btnClose.addEventListener("click", () => window.close());
btnCancel.addEventListener("click", () => window.close());

if (errorParam === "not_running") {
    showError();
} else {
    fetchWorkflows();
}

function showError() {
    errorState.style.display = "flex";
    contentArea.style.display = "none";
}

async function fetchWorkflows() {
    try {
        const res = await fetch(API + "/workflows", { signal: AbortSignal.timeout(2000) });
        if (!res.ok) throw new Error("API Error");
        const data = await res.json();
        
        allWorkflows = Object.entries(data.workflows).map(([name, w]) => ({ name, ...w }));
        allWorkflows.sort((a, b) => {
            if (a.pinned !== b.pinned) return b.pinned ? 1 : -1;
            return a.name.localeCompare(b.name);
        });
        
        renderWorkflows(allWorkflows);
    } catch (e) {
        showError();
    }
}

function renderWorkflows(workflows) {
    // Clear list but keep empty state
    Array.from(listEl.children).forEach(child => {
        if (child !== emptyState) listEl.removeChild(child);
    });

    if (workflows.length === 0) {
        emptyState.style.display = "block";
    } else {
        emptyState.style.display = "none";
        workflows.forEach(w => {
            const card = document.createElement("div");
            card.className = "card";
            card.innerHTML = `
                <div class="c-emoji">${w.emoji || '🚀'}</div>
                <div class="c-name">${w.name}</div>
            `;
            card.addEventListener("click", () => addUrlToWorkflow(w.name, card));
            listEl.appendChild(card);
        });
    }
}

async function addUrlToWorkflow(workflowName, cardEl) {
    cardEl.classList.add("added");
    cardEl.querySelector(".c-name").textContent = `✅ Added to ${workflowName}!`;
    
    try {
        await fetch(API + "/add-url", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: targetUrl, workflow: workflowName })
        });
        setTimeout(() => window.close(), 1200);
    } catch (e) {
        showError();
    }
}

searchInput.addEventListener("input", (e) => {
    const query = e.target.value.toLowerCase().trim();
    if (!query) {
        renderWorkflows(allWorkflows);
        return;
    }
    const filtered = allWorkflows.filter(w => w.name.toLowerCase().includes(query));
    renderWorkflows(filtered);
});
