<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-GPL%20v3-orange?style=for-the-badge" alt="License">
</p>

<h1 align="center">🎮 SC2FLA-FOSS-Edition</h1>

<p align="center">
  <strong>Free and Open-Source tool for converting Supercell <code>.sc</code> files to Adobe Animate <code>.fla</code> files</strong>
</p>

<p align="center">
  <em>Now with full macOS & Linux support!</em>
</p>

---

## ✨ Features

| Feature | Status |
|---------|--------|
| Basic `.sc` to `.fla` conversion | ✅ |
| SC2 to SC1 downgrade support | ✅ |
| SCTX texture decoding | ✅ |
| KTX/Khronos texture support | ✅ |
| Batch processing | ✅ |
| **macOS support (Intel & Apple Silicon)** | ✅ NEW |
| **Linux support** | ✅ NEW |
| **Wine integration for cross-platform** | ✅ NEW |
| Spritesheet creation | 🔜 Soon |
| Multi-threading | 🔜 Soon |

---

## 🖥️ Platform Support

| Platform | Status | Method |
|----------|--------|--------|
| Windows 10/11 | ✅ Native | Direct execution |
| macOS (Intel) | ✅ Full | Wine or native binaries |
| macOS (Apple Silicon) | ✅ Full | Wine or native binaries |
| Linux | ✅ Full | Wine or native binaries |

---

## 📦 Quick Start

### Prerequisites

- **Python 3.9+** (3.10+ recommended)
- **pip** (Python package manager)
- **Wine** (macOS/Linux only, for Windows binaries)

### Installation

<details>
<summary><b>🪟 Windows</b></summary>

```powershell
# 1. Clone the repository
git clone https://github.com/Dstnexe/SC2FLA-FOSS-Edition.git
cd SC2FLA-FOSS-Edition

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run setup to download required tools
python user-scripts/setup.py

# 4. Test installation
python main.py --help
```

</details>

<details>
<summary><b>🍎 macOS</b></summary>

```bash
# 1. Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Wine
brew install wine-stable

# 3. Clone the repository
git clone https://github.com/Dstnexe/SC2FLA-FOSS-Edition.git
cd SC2FLA-FOSS-Edition

# 4. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run setup to download required tools
python user-scripts/setup.py

# 7. Test installation
python main.py --platform
python main.py --tools
```

</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
# 1. Install Wine
# Ubuntu/Debian:
sudo apt install wine

# Fedora:
sudo dnf install wine

# Arch:
sudo pacman -S wine

# 2. Clone the repository
git clone https://github.com/Dstnexe/SC2FLA-FOSS-Edition.git
cd SC2FLA-FOSS-Edition

# 3. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run setup to download required tools
python user-scripts/setup.py

# 6. Test installation
python main.py --platform
python main.py --tools
```

</details>

---

## 🚀 Usage

### Basic Usage

1. **Place your files** in the `$assets/` folder:
   - `.sc` files (main assets)
   - `_tex.sc` files (textures)
   - `.sctx` files (if applicable)

2. **Run the conversion:**

```bash
# Process all files in $assets folder
python main.py -p \$assets

# Process a single file
python main.py -p \$assets/your_file.sc

# Dump RAW resources
python main.py -dr -p \$assets
```

3. **Find your output** in the same directory as the input files (`.fla` files)

### Command-Line Interface

```
usage: main.py [-h] [-p FILE/DIR] [-dr] [-dp] [-dx FILE] [-cx FILE] [-s]
               [--platform] [--tools] [--config]

Arguments:
  -h,  --help          Show this help message and exit
  -p,  --process       Process .sc file or directory
  -dr, --dump-raw      Dump RAW resources of .sc files
  -dp, --dump-png      Dump PNG resources of .sc files
  -dx, --decompress    Decompress .sc files
  -cx, --compress      Compress .sc files (LZMA | SC | V1)
  -s,  --sort-layers   Enable layer sorting

Platform Commands (NEW):
  --platform           Show platform information
  --tools              Show tool status and paths
  --config             Show configuration status
```

### Shell Scripts (macOS/Linux)

```bash
# Make scripts executable (first time only)
chmod +x user-scripts/*.sh

# Process all files
./user-scripts/process_folder.sh

# Dump RAW resources
./user-scripts/dump_raw.sh
```

### Batch Scripts (Windows)

- `process folder.bat` — Convert all `.sc` files
- `dump raw.bat` — Dump RAW resources
- `clean all files.vbs` — Reset the tool

---

## 🔧 Platform Commands

Check your system compatibility:

```bash
# Show platform information
python main.py --platform

# Example output:
# ═══ Platform Information ═══
# OS: macos
# Architecture: arm64
# Python: 3.12.0
# Wine Available: True
```

Check tool status:

```bash
# Show tool availability
python main.py --tools

# Example output:
# ═══ Tool Status ═══
# ✓ sc_downgrade (wine)
# ✓ sctx_converter (wine)
# ✓ pvr_tex_tool (wine)
# ✓ sc_tex (wine)
```

---

## 📁 Project Structure

```
SC2FLA-FOSS-Edition/
├── $assets/              # Place your .sc files here
├── lib/
│   ├── bin/
│   │   ├── macos/        # Native macOS binaries (optional)
│   │   ├── windows/      # Windows binaries
│   │   └── linux/        # Native Linux binaries (optional)
│   ├── sc/               # SC file parsing
│   ├── fla/              # FLA file generation
│   ├── platform_detect.py    # OS detection
│   ├── config.py             # Configuration management
│   └── tools.py              # Cross-platform tool runner
├── user-scripts/
│   ├── setup.py          # Setup script (all platforms)
│   ├── process_folder.sh # macOS/Linux script
│   ├── dump_raw.sh       # macOS/Linux script
│   └── *.bat             # Windows scripts
├── main.py               # Main entry point
├── requirements.txt      # Python dependencies
└── README.md
```

---

## 🍷 Wine Integration (macOS/Linux)

This fork automatically detects and uses Wine to run Windows binaries on macOS and Linux.

**How it works:**
1. The tool checks for native binaries in `lib/bin/macos/` or `lib/bin/linux/`
2. If not found, it falls back to Windows `.exe` files via Wine
3. Wine is detected automatically — no configuration needed

**Tool search priority:**
1. Native binary in platform-specific folder
2. Windows binary via Wine
3. Legacy paths (`lib/`, `user-scripts/`)

---

## 🛠️ External Dependencies

| Tool | Purpose | Source |
|------|---------|--------|
| ScDowngrade | Convert SC2 → SC1 format | [GitHub](https://github.com/Daniil-SV/ScDowngrade/releases) |
| SctxConverter | Decode SCTX textures | [GitHub](https://github.com/Daniil-SV/SCTX-Converter/releases) |
| PVRTexToolCLI | Decode KTX textures | [Imagination Tech](https://developer.imaginationtech.com/pvrtextool/) |
| SCTex | Create spritesheets | [GitHub](https://github.com/sc-workshop/SupercellFlash) |

---

## ❓ Troubleshooting

<details>
<summary><b>Wine not found (macOS)</b></summary>

```bash
brew install wine-stable
```

</details>

<details>
<summary><b>Python module not found</b></summary>

Make sure you're in your virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

</details>

<details>
<summary><b>Permission denied on shell scripts</b></summary>

```bash
chmod +x user-scripts/*.sh
```

</details>

<details>
<summary><b>Tools not detected</b></summary>

Run the setup script:
```bash
python user-scripts/setup.py
```

Then check with:
```bash
python main.py --tools
```

</details>

---

## 📝 Changelog

### This Fork (macOS Support)
- ✅ Full macOS support (Intel & Apple Silicon)
- ✅ Full Linux support
- ✅ Wine integration for cross-platform execution
- ✅ New platform detection system (`--platform`, `--tools`, `--config`)
- ✅ Shell scripts for macOS/Linux
- ✅ Python 3.9+ compatibility
- ✅ Improved error handling

### Original Project
- ~~Improve logging [V1.1]~~
- ~~Allow directory as argument [V2.0]~~
- ~~Implement SCTX Converter [V3.0]~~
- ~~Implement RAW dump feature [V4.0]~~
- ~~Fix Khronos textures with PVRTexTool [V5.0]~~
- 🔜 Spritesheet creation with SCTex.exe
- 🔜 Multi-threading support

---

## 🙏 Credits

| Contributor | Contribution |
|-------------|--------------|
| [Daniil-SV](https://github.com/daniil-sv) | Original SC2FLA creator |
| [Fred-31](https://github.com/pavidloq) | Original SC2FLA co-creator |
| [GenericName1911](https://github.com/GenericName1911) | FOSS Edition maintainer |
| [Dstnexe](https://github.com/Dstnexe) | macOS/Linux port |

---

## 📄 License

```
Copyright (C) 2025 GenericName1911 & Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
```

---

<p align="center">
  <strong>⭐ Star this repo if it helped you! ⭐</strong>
</p>

<p align="center">
  <a href="https://github.com/Dstnexe/SC2FLA-FOSS-Edition/issues">Report Bug</a>
  ·
  <a href="https://github.com/Dstnexe/SC2FLA-FOSS-Edition/issues">Request Feature</a>
</p>
