<div align="center">
  <img src="https://raw.githubusercontent.com/farazkayan/nexus-workflow-manager/main/logo.svg" width="120" height="120" alt="Nexus Logo"/>

  <h1>Nexus</h1>
  <p>A one-click workflow launcher for Windows.<br/>Group your apps and websites into workflows and launch them all instantly.</p>

  <a href="https://github.com/farazkayan/nexus-workflow-manager/releases/latest">
    <img src="https://img.shields.io/github/v/release/farazkayan/nexus-workflow-manager?color=6366F1&label=Download&style=for-the-badge" alt="Download"/>
  </a>
  &nbsp;
  <img src="https://img.shields.io/badge/Platform-Windows-6366F1?style=for-the-badge" alt="Windows"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Version-2.0-6366F1?style=for-the-badge" alt="Version"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Python-3.11-6366F1?style=for-the-badge" alt="Python"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Chrome-Extension-6366F1?style=for-the-badge" alt="Chrome Extension"/>

</div>

---

## What is Nexus?

Nexus lets you group your apps and websites into named **workflow cards**. Click a card and everything in it launches at once — your browser tabs, your tools, your whole setup — in one click.

Now with a **Chrome Extension** that lets you launch workflows and save tab sessions directly from your browser.

No subscriptions. No account. No bloat. Just install and go.

---

## Features

### Desktop App
- **One-click launch** — open all your apps and URLs in a single click
- **Workflow cards** — create, name, and organise as many workflows as you want
- **Global hotkeys** — assign a keyboard shortcut to any workflow and launch it from anywhere on Windows
- **Scheduled workflows** — auto-launch workflows at a set time and day
- **Emoji icons** — pick an emoji to identify each workflow at a glance
- **Categories + sidebar** — organise workflows into categories with a filterable sidebar
- **Profiles** — switch between entire sets of workflows instantly (Work mode, Gaming mode, etc.)
- **Pin workflows** — keep important workflows always at the top
- **Drag to reorder** — rearrange cards and items inside workflows
- **Compact mode** — toggle a slim view to see more workflows at once
- **System tray** — runs quietly in the tray, launch workflows without opening the window
- **Dark & light theme** — switch in settings
- **Search** — find workflows instantly as you type
- **Import / Export** — back up and restore your workflows as JSON
- **Usage stats** — track how many times each workflow has been launched
- **Run on startup** — optionally launch Nexus when Windows boots
- **Configurable launch delay** — control the gap between each item launching
- **Broken path detection** — warns you if an app has been moved or uninstalled
- **Auto-updater** — notified when a new version is available on GitHub

### Chrome Extension
- **Workflow launcher popup** — see all your workflows and launch them from Chrome
- **Save all tabs as a workflow** — save your entire current tab session with one click
- **Right-click to add** — right-click any page or link → "Add to Nexus workflow"
- **Instant status** — live green/red dot shows whether Nexus is running
- **Instant loading** — cached workflows shown immediately while fresh data loads

---

## Download

👉 **[Download Nexus_Setup.exe from the latest release](https://github.com/farazkayan/nexus-workflow-manager/releases/latest)**

Run the installer, click through the wizard, and Nexus will appear in your Start Menu and on your desktop.

> **Note:** Windows SmartScreen may show a warning the first time you run the installer. Click **More info → Run anyway**. This is normal for indie apps that aren't code-signed.

---

## Chrome Extension

The extension connects to the Nexus desktop app running locally. No account or API key needed.

### Install

1. **[Download nexus-extension.zip](https://github.com/farazkayan/nexus-workflow-manager/releases/latest)** from the latest release and unzip it
2. Open Chrome → go to `chrome://extensions`
3. Enable **Developer Mode** (top right toggle)
4. Click **Load unpacked** → select the `nexus-extension` folder
5. Make sure Nexus desktop app is running
6. Click the Nexus icon in your Chrome toolbar

> The extension talks to Nexus over `localhost:57832`. No registry setup. No native messaging. No extra steps.

---

## How to use

1. Click **+ Add Workflow** (or press `Ctrl+N`)
2. Give it a name, emoji, colour tag and category
3. Add the apps (`.exe` files) and URLs you want it to launch
4. Optionally assign a **global hotkey** (e.g. `ctrl+shift+w`)
5. Click **Save Workflow**
6. Click the card — or press your hotkey from anywhere on Windows — to launch everything

---

## Global Hotkeys

Nexus uses the Windows `RegisterHotKey` API — hotkeys fire system-wide even when Nexus is minimised to the tray.

To assign a hotkey: open the **⋮ menu** on any card → **Set Hotkey** → press your combination → **Save**.

---

## Scheduled Workflows

Open the **⋮ menu** on any card → **Schedule** → enable the toggle → pick a time and days → **Save**. Nexus will auto-launch that workflow at the set time every selected day.

---

## Profiles

Profiles let you switch between entire sets of workflows instantly. Switch via the dropdown in the header. Create profiles for Work, Gaming, Creative — each with its own independent cards.

---

## Built with

- [Python 3.11](https://python.org)
- [PySide6](https://doc.qt.io/qtforpython/) — UI framework
- [platformdirs](https://github.com/platformdirs/platformdirs) — cross-platform data paths
- [PyInstaller](https://pyinstaller.org) — packaging
- [Inno Setup](https://jrsoftware.org/isinfo.php) — installer

---

## Building from source

```bash
# Install dependencies
pip install PySide6 platformdirs pyinstaller

# Run directly
python nexus.py

# Build EXE
pyinstaller --onefile --windowed --name "Nexus" --icon="nexus.ico" nexus.py
```

---

## Roadmap

- [x] Emoji icon per workflow card
- [x] Pin workflows to top
- [x] Compact view mode
- [x] Scheduled workflows
- [x] Categories + sidebar
- [x] Global hotkeys
- [x] Profiles
- [x] Usage stats
- [x] Auto-updater
- [x] Chrome Extension
- [ ] Chrome Web Store release
- [ ] macOS support

---

## Creator

Made by **Faraz Kayan Haque** — [GitHub](https://github.com/farazkayan)

If you find Nexus useful, leave a ⭐ on the repo — it means a lot!
