# Remove Shortcut Arrows – Windows 10/11

<p align="center">
  <img src="https://img.shields.io/badge/Windows-10%20%7C%2011-0078D6?logo=windows&logoColor=white" alt="Windows 10/11">
  <img src="https://img.shields.io/badge/Python-3.6+-3776AB?logo=python&logoColor=white" alt="Python 3.6+">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
</p>

A simple Python script that removes the ugly shortcut overlay arrows from your desktop icons on Windows 10 & 11.

**Before → After:**


![Before and After](https://media.discordapp.net/attachments/1471504359249678379/1471505559122346146/image2.jpg?ex=698f2dd8&is=698ddc58&hm=dfb1697950342c159fbe9543e6b9a6343c29c174aba2d3163ce153c4a3727e9a&=&format=webp)


## How It Works

The script uses a **built-in Windows blank icon** (`imageres.dll,-17`) — no external `.ico` file needed. This avoids the common "black square" or "white page" bugs that happen with custom transparent icons.

1. **Sets** the registry value `29` under `Shell Icons` pointing to `%windir%\System32\imageres.dll,-17`
2. **Applies** to both 64-bit and WOW6432Node registry paths for full compatibility
3. **Clears** the icon cache to prevent rendering artifacts
4. **Restarts** Windows Explorer so changes take effect immediately

No third-party dependencies. No downloads. Pure Python standard library.

## Quick Start

### Remove arrows

```bash
python remove_shortcut_arrows.py
```

### Restore arrows

```bash
python remove_shortcut_arrows.py --restore
```

### Rebuild icon cache only

```bash
python remove_shortcut_arrows.py --rebuild-cache
```

> **Note:** The script must run as **Administrator**. It will automatically prompt for elevation via UAC if needed.

## Requirements

- **Windows 10 or 11**
- **Python 3.6+** (uses only standard library modules)
- **Administrator privileges** (the script auto-elevates)

## What Gets Changed

| Item | Location | Action |
|------|----------|--------|
| Registry key | `HKLM\...\Explorer\Shell Icons` | Created |
| Registry key | `HKLM\...\WOW6432Node\...\Explorer\Shell Icons` | Created |
| Registry value | `29` → `%windir%\System32\imageres.dll,-17` | Set |
| Icon cache | `%LOCALAPPDATA%\Microsoft\Windows\Explorer\iconcache*` | Cleared |

The `--restore` flag cleanly reverts **all** of the above.

## FAQ

**Is this safe?**
Yes. This is a standard Windows registry tweak that has been used since Windows XP. It only changes how shortcut overlays are rendered — no system files are modified.

**Do I need to restart my PC?**
No. The script restarts `explorer.exe` and clears the icon cache automatically.

**Will this survive Windows updates?**
Generally yes. In rare cases, a major feature update might reset it — just run the script again.

**I see black squares or white pages instead of arrows?**
Run `--restore` first, then run the script again. If you previously used a different method with a custom `.ico` file, make sure to remove it.

**Can I undo it?**
Yes, run `python remove_shortcut_arrows.py --restore` and everything goes back to normal.

## License

MIT — do whatever you want with it.

## Author

Made by **Swif2D**
