# Kouprey Window Font Changer

A Windows tool to customize system fonts for UI elements like title bars, menus, message boxes, icon labels, and more.

Built with PyQt6 and uses the Windows `SystemParametersInfoW` API to apply font changes system-wide.

## Features

- Change fonts for individual UI elements (title bars, menus, tooltips, icon labels, etc.)
- Apply a single font to all elements at once
- Preview current font settings in a table
- Reset to default fonts
- Light/dark theme toggle
- Khmer/English language support
- AgentOS quick-preset button

## Requirements

- Windows (uses Win32 API)
- Python 3.10+
- PyQt6

## Installation

```bash
pip install PyQt6 PyQt6-Qt6 PyQt6-sip
```

## Usage

```bash
python main.py
```

## Font Elements

| Element | Description |
|---------|-------------|
| Font Icon | Icon text labels on desktop |
| Font Message boxes | Message box text |
| Font Tooltips | Tooltip text |
| Font Menus | Menu text |
| Font Title Bars | Window title bar text |
| Font Palette Titles | Palette/dialog title text |

## Project Structure

```
├── main.py              # Application entry point
├── ui_main.py           # Main window UI
├── theme.py             # Theme manager (light/dark)
├── language.py          # Language manager (en/km)
├── win32_metrics.py     # Win32 font API bindings
├── icons.py             # SVG icon renderer (Lucide)
├── assets/
│   ├── lang/
│   │   ├── en.json      # English strings
│   │   └── km.json      # Khmer strings
│   └── fonts/           # Font assets
└── lucide/              # Lucide icon SVGs
```

## License

© 2026 Kouprey
