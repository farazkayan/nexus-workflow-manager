<div align="center">
  <img src="https://github.com/farazkayan/nexus-workflow-manager/releases/download/v1.0/nexus.ico" width="120" height="120" alt="Nexus Logo"/>

  <h1>Nexus</h1>
  <p>A one-click workflow launcher for Windows.<br/>Group your apps and websites into workflows and launch them all instantly.</p>

  <a href="https://github.com/farazkayan/nexus-workflow-manager/releases/latest">
    <img src="https://img.shields.io/github/v/release/farazkayan/nexus-workflow-manager?color=6D63F5&label=Download&style=for-the-badge" alt="Download"/>
  </a>
  &nbsp;
  <img src="https://img.shields.io/badge/Platform-Windows-6D63F5?style=for-the-badge" alt="Windows"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Python-3.11-6D63F5?style=for-the-badge" alt="Python"/>

</div>

---

## What is Nexus?

Nexus lets you group your apps and websites into named **workflow cards**. Click a card and everything in it launches at once — your browser tabs, your tools, your whole setup — in one click.

No subscriptions. No account. No bloat. Just install and go.

---

## Features

- **One-click launch** — open all your apps and URLs in a single click
- **Workflow cards** — create, name, and organise as many workflows as you want
- **Drag to reorder** — rearrange cards by dragging them
- **System tray** — runs quietly in the tray, launch workflows without opening the window
- **Dark & light theme** — switch in settings
- **Search** — find workflows instantly as you type
- **Import / Export** — back up and restore your workflows as JSON
- **Run on startup** — optionally launch Nexus when Windows boots
- **Configurable launch delay** — control the gap between each item launching
- **Broken path detection** — warns you if an app has been moved or uninstalled

---

## Download

👉 **[Download Nexus_Setup.exe from the latest release](https://github.com/farazkayan/nexus-workflow-manager/releases/latest)**

Run the installer, click through the wizard, and Nexus will appear in your Start Menu and on your desktop.

> **Note:** Windows SmartScreen may show a warning the first time you run the installer. Click **More info → Run anyway**. This is normal for indie apps that aren't code-signed.

---

## How to use

1. Click **➕ Add Workflow**
2. Give it a name and optionally a description and colour tag
3. Add the apps (`.exe` files) and URLs you want it to launch
4. Click **Save Workflow**
5. Click the card whenever you want to launch everything in it

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
pyinstaller --onefile --windowed --name "Nexus" --icon="nexus.ico" --add-data "nexus.ico;." nexus.py
```

---

## Roadmap

- [ ] Scheduled workflows — auto-launch at a set time
- [ ] Categories / folders for cards
- [ ] Custom emoji icon per workflow card
- [ ] Auto-updater

---

## Creator

Made by **Faraz Kayan Haque**

If you find Nexus useful, leave a ⭐ on the repo — it means a lot!
