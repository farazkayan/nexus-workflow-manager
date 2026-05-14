const API = "http://127.0.0.1:57832";
const DEBUG = false;

chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "add_page_to_nexus",
        title: "Add this page to a Nexus workflow",
        contexts: ["page"]
    });
    chrome.contextMenus.create({
        id: "add_link_to_nexus",
        title: "Add this link to a Nexus workflow",
        contexts: ["link"]
    });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
    let url = "";
    if (info.menuItemId === "add_page_to_nexus") {
        url = info.pageUrl;
    } else if (info.menuItemId === "add_link_to_nexus") {
        url = info.linkUrl;
    } else {
        return;
    }

    try {
        await fetch(API + "/status", {signal: AbortSignal.timeout(1500)});
    } catch {
        chrome.windows.create({
            url: chrome.runtime.getURL("workflow_picker.html") + "?error=not_running",
            type: "popup", width: 380, height: 200
        });
        return;
    }

    chrome.windows.create({
        url: chrome.runtime.getURL("workflow_picker.html")
             + "?url=" + encodeURIComponent(url)
             + "&title=" + encodeURIComponent(info.pageTitle || ""),
        type: "popup", width: 380, height: 460
    });
});

async function refreshWorkflowCache() {
    try {
        const r = await fetch(API + "/workflows", {signal: AbortSignal.timeout(2000)});
        const data = await r.json();
        await chrome.storage.local.set({
            cached_workflows: data,
            cache_time: Date.now()
        });
        return data;
    } catch {
        return null;
    }
}

