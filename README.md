# SJournaller

> A secure, encrypted personal journal application.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-yellow)

## Features

- 🔒 **Encrypted database** — Fernet (AES-128-CBC) + PBKDF2-HMAC-SHA256 key derivation
- 📅 **Date-based journaling** — pick any date, write
- 📋 **Templates** — reusable text skeletons (Daily Reflection, Gratitude Log, Meeting Notes)
- 📤 **Export / Import** — delimited text with `-----------[date]----` separators
- 🌙 **Dark & Light themes** — Catppuccin-inspired
- 🔍 **Full-text search**
- 💾 **Auto-save** — configurable interval
- 🔑 **Change password** — re-encrypts DB on the fly
- 📊 **Word & character count** in status bar
- 🚫 **Fully offline**

## Quick Start

```bash
pip install PyQt6 cryptography
python -m sjournaller
```

On first launch: set a password, pick a theme. That's it.

⚠️ **No password recovery.** If you forget it, your data is gone.

## Data Storage

| File | Path |
|------|------|
| Config | `%APPDATA%\sjournaller\config.json` |
| Encrypted DB | `%APPDATA%\sjournaller\data\journal.enc` |
| Temp decrypted DB | `%APPDATA%\sjournaller\data\journal.db` *(deleted on exit)* |

## Export Format

```text
-----------[2027-01-15]----
Entry content here...

-----------[2027-01-12]----
Another entry...
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save current entry |
| `Ctrl+T` | Go to today |
| `Ctrl+E` | Export journal |
| `Ctrl+I` | Import journal |
| `Ctrl+L` | Open template manager |
| `Ctrl+Shift+T` | Toggle dark / light theme |
| `Ctrl++` | Increase font size |
| `Ctrl+-` | Decrease font size |
| `Ctrl+,` | Open settings |
| `Ctrl+Q` | Quit |

## Compile to EXE

### 1. Install build dependencies

```bash
pip install pyinstaller Pillow
```

### 2. Generate the icon

```bash
python create_icon.py
```

Creates `assets/icon.ico` and `assets/icon.png`.

### 3. Build

```bash
python build.py
```

This wipes `build/` and `dist/`, then runs PyInstaller with `--clean`.
Output: `dist/SJournaller.exe` (~15–25 MB).

### 4. Or build manually

```bash
rmdir /s /q build dist
pyinstaller --clean sjournaller.spec
```

> **Always delete `dist/` before rebuilding.** PyInstaller overwrites the `.exe` but leaves stale `.dll`/`.pyd` files from previous builds. The `--clean` flag only clears `build/`, not `dist/`.

## Security

| | |
|---|---|
| Encryption | Fernet (AES-128-CBC + HMAC-SHA256) |
| Key derivation | PBKDF2-HMAC-SHA256, 480 000 iterations |
| Salt | 16 bytes, random per installation |

- Password hash is stored in config for verification — the encryption key is derived at runtime and never persisted
- Plaintext DB exists only while the app is running; encrypted and deleted on exit
- On crash, the temp `.db` may remain — it is auto-deleted on next launch

## License

MIT. © 2026 Syphax.

