#!/usr/bin/env python3
"""
setup.py - Plattformübergreifendes Setup-Skript für SC2FLA

Installiert Python-Dependencies und lädt externe Tools herunter.
Unterstützt Windows, macOS und Linux.
"""

import subprocess
import sys
import os
import platform
import shutil
import tempfile
from pathlib import Path

# Projekt-Verzeichnisse
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = SCRIPT_DIR.parent
LIB_DIR = PROJECT_DIR / "lib"
BIN_DIR = LIB_DIR / "bin"

# Python-Module
MODULES = [
    'requests',
    'sc-compression==0.6.1',
    'Pillow',
    'numpy',
    'affine6p',
    'colorama',
    'lxml',
    'ujson',
    'zstandard'
]

# Tool-Download-URLs
TOOL_URLS = {
    "scdowngrade": "https://api.github.com/repos/Daniil-SV/ScDowngrade/releases/latest",
    "sctxconverter": "https://api.github.com/repos/Daniil-SV/SCTX-Converter/releases/latest"
}


def get_platform_info():
    """Ermittelt Plattform-Informationen"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "darwin":
        os_name = "macos"
    elif system == "windows":
        os_name = "windows"
    else:
        os_name = "linux"
    
    if machine in ("x86_64", "amd64"):
        arch = "x64"
    elif machine in ("arm64", "aarch64"):
        arch = "arm64"
    else:
        arch = "x86"
    
    return os_name, arch


def print_header():
    """Zeigt Setup-Header an"""
    print("=" * 60)
    print("  SC2FLA-FOSS-Edition Setup")
    print("  Plattformübergreifende Installation")
    print("=" * 60)
    print()
    
    os_name, arch = get_platform_info()
    print(f"  Platform: {os_name} ({arch})")
    print(f"  Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print()


def install_modules():
    """Installiert Python-Module"""
    print("📦 Installiere Python-Module...")
    print()
    
    for module in MODULES:
        try:
            print(f"  Installing: {module}")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", module],
                capture_output=True,
                text=True
            )
            
            if "Requirement already satisfied" in result.stdout:
                print(f"    ✓ Already installed")
            elif result.returncode == 0:
                print(f"    ✓ Successfully installed")
            else:
                print(f"    ✗ Failed: {result.stderr[:100]}")
                
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    print()


def create_bin_directories():
    """Erstellt die Verzeichnisstruktur für Binaries"""
    print("📁 Erstelle Verzeichnisstruktur...")
    
    directories = [
        BIN_DIR / "windows",
        BIN_DIR / "macos",
        BIN_DIR / "linux"
    ]
    
    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"    ✓ {dir_path.relative_to(PROJECT_DIR)}")
    
    print()


def download_windows_tools():
    """Lädt Windows-Tools herunter (für Wine-Kompatibilität)"""
    print("⬇️  Lade Windows-Tools herunter...")
    print()
    
    try:
        import requests
    except ImportError:
        print("    ✗ requests-Modul nicht verfügbar. Überspringe Downloads.")
        return
    
    windows_bin = BIN_DIR / "windows"
    
    for tool_name, api_url in TOOL_URLS.items():
        try:
            print(f"  Downloading: {tool_name}")
            
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            release_data = response.json()
            assets = release_data.get("assets", [])
            
            if not assets:
                print(f"    ⚠ No assets found")
                continue
            
            for asset in assets:
                filename = asset["name"]
                
                # Nur .exe Dateien herunterladen
                if not filename.endswith(".exe"):
                    continue
                
                url = asset["browser_download_url"]
                dest_path = windows_bin / filename
                
                # Prüfen ob bereits vorhanden
                if dest_path.exists():
                    print(f"    ✓ {filename} already exists")
                    continue
                
                # Herunterladen
                print(f"    ⬇ Downloading {filename}...")
                with requests.get(url, stream=True, timeout=30) as r:
                    r.raise_for_status()
                    with open(dest_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                
                print(f"    ✓ {filename} downloaded")
                
        except Exception as e:
            print(f"    ✗ Failed: {e}")
    
    print()


def copy_legacy_tools():
    """Kopiert vorhandene Tools in die neue Struktur"""
    print("🔄 Migriere vorhandene Tools...")
    
    legacy_tools = [
        ("ScDowngrade.exe", "windows"),
        ("SctxConverter.exe", "windows"),
        ("SctxConverter-avx2.exe", "windows"),
        ("PVRTexToolCLI.exe", "windows"),
        ("SCTex.exe", "windows")
    ]
    
    # Suche in lib/ und user-scripts/
    search_dirs = [LIB_DIR, SCRIPT_DIR]
    
    for tool_file, target_platform in legacy_tools:
        for search_dir in search_dirs:
            source = search_dir / tool_file
            if source.exists():
                dest = BIN_DIR / target_platform / tool_file
                if not dest.exists():
                    shutil.copy2(source, dest)
                    print(f"    ✓ Migrated {tool_file}")
                break
    
    print()


def check_wine():
    """Prüft ob Wine verfügbar ist (für macOS/Linux)"""
    os_name, _ = get_platform_info()
    
    if os_name == "windows":
        return
    
    print("🍷 Prüfe Wine-Installation...")
    
    wine_path = shutil.which("wine") or shutil.which("wine64")
    
    if wine_path:
        print(f"    ✓ Wine gefunden: {wine_path}")
    else:
        print("    ⚠ Wine nicht gefunden")
        print()
        print("    Wine wird benötigt, um Windows-Tools auf macOS/Linux auszuführen.")
        print("    Installation:")
        if os_name == "macos":
            print("      brew install wine-stable")
        else:
            print("      sudo apt install wine (Debian/Ubuntu)")
            print("      sudo dnf install wine (Fedora)")
    
    print()


def print_pvrtextool_info():
    """Zeigt Info zur PVRTexToolCLI-Installation"""
    os_name, arch = get_platform_info()
    
    if os_name == "windows":
        return
    
    print("ℹ️  PVRTexToolCLI für macOS/Linux:")
    print()
    print("    PVRTexToolCLI ist für macOS nativ verfügbar!")
    print("    Download: https://developer.imaginationtech.com/pvrtextool/")
    print()
    print(f"    Empfohlene Version für {os_name} ({arch}):")
    if arch == "arm64" and os_name == "macos":
        print("      - macos_arm64 (Apple Silicon)")
    elif os_name == "macos":
        print("      - macos_x86 (Intel)")
    else:
        print("      - linux_x64")
    print()
    print(f"    Nach dem Download in '{BIN_DIR / os_name}/' platzieren")
    print()


def verify_installation():
    """Verifiziert die Installation"""
    print("✅ Verifiziere Installation...")
    print()
    
    # Python-Module prüfen
    modules_ok = True
    for module in MODULES:
        module_name = module.split("==")[0]
        try:
            __import__(module_name.replace("-", "_"))
            print(f"    ✓ {module_name}")
        except ImportError:
            print(f"    ✗ {module_name} nicht verfügbar")
            modules_ok = False
    
    print()
    
    # Tools prüfen
    os_name, _ = get_platform_info()
    tools_dir = BIN_DIR / ("windows" if os_name != "windows" else os_name)
    
    print("  Tools:")
    for tool in ["ScDowngrade.exe", "SctxConverter.exe", "PVRTexToolCLI.exe"]:
        tool_path = tools_dir / tool
        if tool_path.exists():
            print(f"    ✓ {tool}")
        else:
            print(f"    ⚠ {tool} nicht gefunden")
    
    print()
    
    return modules_ok


def main():
    """Hauptfunktion"""
    print_header()
    
    # Python-Module installieren
    install_modules()
    
    # Verzeichnisse erstellen
    create_bin_directories()
    
    # Legacy-Tools migrieren
    copy_legacy_tools()
    
    # Windows-Tools herunterladen
    download_windows_tools()
    
    # Wine-Check (macOS/Linux)
    check_wine()
    
    # PVRTexTool-Info
    print_pvrtextool_info()
    
    # Verifikation
    verify_installation()
    
    print("=" * 60)
    print("  Setup abgeschlossen!")
    print()
    print("  Nächste Schritte:")
    print("    1. Platziere .sc Dateien in '$assets/'")
    print("    2. Führe aus: python main.py --process $assets")
    print("    3. Oder nutze: python main.py --help")
    print("=" * 60)
    print()
    
    input("Drücke Enter zum Beenden...")


if __name__ == "__main__":
    main()
