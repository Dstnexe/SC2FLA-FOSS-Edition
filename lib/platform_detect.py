"""
Platform Detection Module for SC2FLA-FOSS-Edition

Detects operating system, architecture, and available tools.
"""

import platform
import sys
import os
import shutil
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class OperatingSystem(Enum):
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    UNKNOWN = "unknown"


class Architecture(Enum):
    X86_64 = "x86_64"
    ARM64 = "arm64"
    X86 = "x86"
    UNKNOWN = "unknown"


@dataclass
class PlatformInfo:
    """Contains all platform-related information."""
    os: OperatingSystem
    arch: Architecture
    os_version: str
    python_version: str
    is_64bit: bool
    
    def __str__(self) -> str:
        return (
            f"OS: {self.os.value} ({self.os_version})\n"
            f"Architecture: {self.arch.value}\n"
            f"64-bit: {self.is_64bit}\n"
            f"Python: {self.python_version}"
        )


def detect_os() -> OperatingSystem:
    """Detect the current operating system."""
    system = platform.system().lower()
    
    if system == "windows":
        return OperatingSystem.WINDOWS
    elif system == "darwin":
        return OperatingSystem.MACOS
    elif system == "linux":
        return OperatingSystem.LINUX
    else:
        return OperatingSystem.UNKNOWN


def detect_architecture() -> Architecture:
    """Detect the CPU architecture."""
    machine = platform.machine().lower()
    
    if machine in ("x86_64", "amd64"):
        return Architecture.X86_64
    elif machine in ("arm64", "aarch64"):
        return Architecture.ARM64
    elif machine in ("i386", "i686", "x86"):
        return Architecture.X86
    else:
        return Architecture.UNKNOWN


def get_platform_info() -> PlatformInfo:
    """Get comprehensive platform information."""
    return PlatformInfo(
        os=detect_os(),
        arch=detect_architecture(),
        os_version=platform.version(),
        python_version=platform.python_version(),
        is_64bit=sys.maxsize > 2**32
    )


def get_binary_extension() -> str:
    """Get the appropriate binary extension for the current OS."""
    os_type = detect_os()
    if os_type == OperatingSystem.WINDOWS:
        return ".exe"
    else:
        return ""  # macOS and Linux don't use extensions


def get_script_extension() -> str:
    """Get the appropriate script extension for the current OS."""
    os_type = detect_os()
    if os_type == OperatingSystem.WINDOWS:
        return ".bat"
    else:
        return ".sh"


def is_wine_available() -> bool:
    """Check if Wine is installed and available."""
    return shutil.which("wine") is not None or shutil.which("wine64") is not None


def get_wine_command() -> Optional[str]:
    """Get the Wine command if available."""
    # Prefer wine64 for 64-bit executables
    if shutil.which("wine64"):
        return "wine64"
    elif shutil.which("wine"):
        return "wine"
    return None


def is_rosetta_available() -> bool:
    """Check if Rosetta 2 is available (macOS Apple Silicon only)."""
    if detect_os() != OperatingSystem.MACOS:
        return False
    if detect_architecture() != Architecture.ARM64:
        return False
    
    # Check for Rosetta by looking for the runtime
    return os.path.exists("/Library/Apple/usr/share/rosetta")


def print_platform_info():
    """Print platform information to console."""
    from colorama import Fore, Style, init
    init()
    
    info = get_platform_info()
    
    print(f"\n{Fore.CYAN}═══ Platform Information ═══{Style.RESET_ALL}\n")
    print(f"{Fore.GREEN}OS:{Style.RESET_ALL} {info.os.value}")
    print(f"{Fore.GREEN}OS Version:{Style.RESET_ALL} {info.os_version}")
    print(f"{Fore.GREEN}Architecture:{Style.RESET_ALL} {info.arch.value}")
    print(f"{Fore.GREEN}64-bit:{Style.RESET_ALL} {info.is_64bit}")
    print(f"{Fore.GREEN}Python:{Style.RESET_ALL} {info.python_version}")
    
    if info.os == OperatingSystem.MACOS:
        print(f"\n{Fore.CYAN}═══ macOS Specific ═══{Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}Wine Available:{Style.RESET_ALL} {is_wine_available()}")
        if info.arch == Architecture.ARM64:
            print(f"{Fore.GREEN}Rosetta 2:{Style.RESET_ALL} {is_rosetta_available()}")
    
    print()


# Module-level cached platform info
_platform_info: Optional[PlatformInfo] = None


def get_cached_platform_info() -> PlatformInfo:
    """Get cached platform info (computed once)."""
    global _platform_info
    if _platform_info is None:
        _platform_info = get_platform_info()
    return _platform_info


if __name__ == "__main__":
    print_platform_info()
