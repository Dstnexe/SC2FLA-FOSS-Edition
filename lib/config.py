"""
Configuration Module for SC2FLA-FOSS-Edition

Manages tool paths, settings, and configuration persistence.
"""

import os
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any

from lib.platform_detect import (
    detect_os, 
    OperatingSystem, 
    get_binary_extension,
    get_cached_platform_info
)


# Base directory of the project
BASE_DIR = Path(__file__).parent.parent.resolve()
LIB_DIR = BASE_DIR / "lib"
BIN_DIR = LIB_DIR / "bin"
CONFIG_FILE = BASE_DIR / "sc2fla_config.json"


@dataclass
class ToolPaths:
    """Paths to external tools."""
    sc_downgrade: Optional[str] = None
    sctx_converter: Optional[str] = None
    pvr_tex_tool: Optional[str] = None
    sc_tex: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ToolPaths':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Settings:
    """Application settings."""
    use_wine: bool = True  # Use Wine for Windows binaries on macOS/Linux
    prefer_native: bool = True  # Prefer native binaries over Wine
    verbose: bool = False
    auto_download_tools: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Settings':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Config:
    """Main configuration class."""
    tool_paths: ToolPaths = field(default_factory=ToolPaths)
    settings: Settings = field(default_factory=Settings)
    
    def save(self, path: Optional[Path] = None) -> None:
        """Save configuration to JSON file."""
        path = path or CONFIG_FILE
        data = {
            "tool_paths": self.tool_paths.to_dict(),
            "settings": self.settings.to_dict()
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load(cls, path: Optional[Path] = None) -> 'Config':
        """Load configuration from JSON file."""
        path = path or CONFIG_FILE
        if not path.exists():
            return cls()
        
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            return cls(
                tool_paths=ToolPaths.from_dict(data.get("tool_paths", {})),
                settings=Settings.from_dict(data.get("settings", {}))
            )
        except (json.JSONDecodeError, KeyError):
            return cls()


def get_platform_bin_dir() -> Path:
    """Get the binary directory for the current platform."""
    os_type = detect_os()
    
    if os_type == OperatingSystem.WINDOWS:
        return BIN_DIR / "windows"
    elif os_type == OperatingSystem.MACOS:
        return BIN_DIR / "macos"
    elif os_type == OperatingSystem.LINUX:
        return BIN_DIR / "linux"
    else:
        return BIN_DIR / "unknown"


def get_windows_bin_dir() -> Path:
    """Get the Windows binary directory (for Wine fallback)."""
    return BIN_DIR / "windows"


def find_tool(tool_name: str, config: Optional[Config] = None) -> Optional[Path]:
    """
    Find a tool binary, checking multiple locations.
    
    Search order:
    1. Config-specified path
    2. Native binary in platform bin directory
    3. Windows binary in windows bin directory (for Wine)
    4. Legacy location (lib/ directory)
    5. user-scripts/ directory
    """
    os_type = detect_os()
    ext = get_binary_extension()
    
    # Tool name mappings
    tool_filenames = {
        "sc_downgrade": "ScDowngrade",
        "sctx_converter": "SctxConverter",
        "pvr_tex_tool": "PVRTexToolCLI",
        "sc_tex": "SCTex"
    }
    
    base_name = tool_filenames.get(tool_name, tool_name)
    
    # 1. Check config-specified path
    if config:
        config_path = getattr(config.tool_paths, tool_name, None)
        if config_path and Path(config_path).exists():
            return Path(config_path)
    
    # 2. Check native binary directory
    native_path = get_platform_bin_dir() / f"{base_name}{ext}"
    if native_path.exists():
        return native_path
    
    # 3. Check Windows binary directory (for Wine fallback)
    if os_type != OperatingSystem.WINDOWS:
        win_path = get_windows_bin_dir() / f"{base_name}.exe"
        if win_path.exists():
            return win_path
    
    # 4. Check legacy location (lib/ directory)
    legacy_path = LIB_DIR / f"{base_name}.exe"
    if legacy_path.exists():
        return legacy_path
    
    # 5. Check user-scripts/ directory
    user_scripts_path = BASE_DIR / "user-scripts" / f"{base_name}.exe"
    if user_scripts_path.exists():
        return user_scripts_path
    
    return None


def find_all_tools(config: Optional[Config] = None) -> Dict[str, Optional[Path]]:
    """Find all tools and return their paths."""
    tools = ["sc_downgrade", "sctx_converter", "pvr_tex_tool", "sc_tex"]
    return {tool: find_tool(tool, config) for tool in tools}


def ensure_bin_directories() -> None:
    """Ensure all binary directories exist."""
    for subdir in ["windows", "macos", "linux"]:
        dir_path = BIN_DIR / subdir
        dir_path.mkdir(parents=True, exist_ok=True)


def print_config_status(config: Optional[Config] = None):
    """Print configuration status to console."""
    from colorama import Fore, Style, init
    init()
    
    config = config or Config.load()
    tools = find_all_tools(config)
    
    print(f"\n{Fore.CYAN}═══ Configuration Status ═══{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}Settings:{Style.RESET_ALL}")
    print(f"  Use Wine: {config.settings.use_wine}")
    print(f"  Prefer Native: {config.settings.prefer_native}")
    print(f"  Verbose: {config.settings.verbose}")
    
    print(f"\n{Fore.YELLOW}Tool Paths:{Style.RESET_ALL}")
    for tool_name, tool_path in tools.items():
        status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if tool_path else f"{Fore.RED}✗{Style.RESET_ALL}"
        path_str = str(tool_path) if tool_path else "Not found"
        print(f"  {status} {tool_name}: {path_str}")
    
    print(f"\n{Fore.YELLOW}Directories:{Style.RESET_ALL}")
    print(f"  Base: {BASE_DIR}")
    print(f"  Binaries: {BIN_DIR}")
    print(f"  Platform Bin: {get_platform_bin_dir()}")
    print(f"  Config File: {CONFIG_FILE}")
    print(f"  Config Exists: {CONFIG_FILE.exists()}")
    
    print()


# Global config instance (lazy loaded)
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config.load()
    return _config


def reload_config() -> Config:
    """Reload the configuration from disk."""
    global _config
    _config = Config.load()
    return _config


if __name__ == "__main__":
    ensure_bin_directories()
    print_config_status()
