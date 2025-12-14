"""
Tool Runner Module for SC2FLA-FOSS-Edition

Handles execution of external tools with cross-platform support (native & Wine).
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

from lib.platform_detect import (
    detect_os,
    OperatingSystem,
    is_wine_available,
    get_wine_command,
    get_cached_platform_info
)
from lib.config import (
    get_config,
    find_tool,
    Config
)


class ToolExecutionMode(Enum):
    """How a tool will be executed."""
    NATIVE = "native"
    WINE = "wine"
    UNAVAILABLE = "unavailable"


@dataclass
class ToolInfo:
    """Information about a tool and how it can be executed."""
    name: str
    path: Optional[Path]
    execution_mode: ToolExecutionMode
    is_windows_binary: bool
    
    @property
    def available(self) -> bool:
        return self.execution_mode != ToolExecutionMode.UNAVAILABLE


class ToolExecutionError(Exception):
    """Raised when a tool fails to execute."""
    pass


class ToolNotFoundError(Exception):
    """Raised when a required tool is not found."""
    pass


def get_tool_info(tool_name: str, config: Optional[Config] = None) -> ToolInfo:
    """
    Get information about a tool including how it would be executed.
    """
    config = config or get_config()
    tool_path = find_tool(tool_name, config)
    
    if tool_path is None:
        return ToolInfo(
            name=tool_name,
            path=None,
            execution_mode=ToolExecutionMode.UNAVAILABLE,
            is_windows_binary=False
        )
    
    os_type = detect_os()
    is_windows_binary = str(tool_path).endswith('.exe')
    
    # Determine execution mode
    if os_type == OperatingSystem.WINDOWS:
        # On Windows, run everything natively
        execution_mode = ToolExecutionMode.NATIVE
    elif is_windows_binary:
        # Windows binary on non-Windows OS
        if config.settings.use_wine and is_wine_available():
            execution_mode = ToolExecutionMode.WINE
        else:
            execution_mode = ToolExecutionMode.UNAVAILABLE
    else:
        # Native binary
        execution_mode = ToolExecutionMode.NATIVE
    
    return ToolInfo(
        name=tool_name,
        path=tool_path,
        execution_mode=execution_mode,
        is_windows_binary=is_windows_binary
    )


def build_command(tool_info: ToolInfo, args: List[str]) -> List[str]:
    """
    Build the command list for executing a tool.
    """
    if tool_info.path is None:
        raise ToolNotFoundError(f"Tool not found: {tool_info.name}")
    
    if tool_info.execution_mode == ToolExecutionMode.UNAVAILABLE:
        raise ToolNotFoundError(
            f"Tool '{tool_info.name}' is a Windows binary and Wine is not available. "
            f"Install Wine with: brew install wine-stable"
        )
    
    if tool_info.execution_mode == ToolExecutionMode.WINE:
        wine_cmd = get_wine_command()
        if wine_cmd is None:
            raise ToolNotFoundError("Wine command not found")
        return [wine_cmd, str(tool_info.path)] + args
    else:
        return [str(tool_info.path)] + args


def run_tool(
    tool_name: str,
    args: List[str],
    config: Optional[Config] = None,
    capture_output: bool = True,
    check: bool = True,
    cwd: Optional[str] = None,
    timeout: Optional[float] = None
) -> subprocess.CompletedProcess:
    """
    Run an external tool with the appropriate method for the current platform.
    
    Args:
        tool_name: Internal tool name (sc_downgrade, sctx_converter, etc.)
        args: Command line arguments to pass to the tool
        config: Optional configuration object
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise on non-zero exit code
        cwd: Working directory for the command
        timeout: Timeout in seconds
    
    Returns:
        CompletedProcess instance
    
    Raises:
        ToolNotFoundError: If the tool cannot be found or executed
        ToolExecutionError: If the tool fails during execution
    """
    config = config or get_config()
    tool_info = get_tool_info(tool_name, config)
    
    if not tool_info.available:
        raise ToolNotFoundError(
            f"Tool '{tool_name}' is not available. "
            f"Path: {tool_info.path}, Mode: {tool_info.execution_mode.value}"
        )
    
    command = build_command(tool_info, args)
    
    if config.settings.verbose:
        print(f"[DEBUG] Running: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            check=check,
            cwd=cwd,
            timeout=timeout,
            text=True
        )
        return result
    
    except subprocess.CalledProcessError as e:
        raise ToolExecutionError(
            f"Tool '{tool_name}' failed with exit code {e.returncode}.\n"
            f"stdout: {e.stdout}\n"
            f"stderr: {e.stderr}"
        ) from e
    
    except subprocess.TimeoutExpired as e:
        raise ToolExecutionError(
            f"Tool '{tool_name}' timed out after {timeout} seconds"
        ) from e
    
    except FileNotFoundError as e:
        raise ToolNotFoundError(
            f"Could not execute tool '{tool_name}': {e}"
        ) from e


def run_sc_downgrade(input_path: str, output_path: str, version: Optional[float] = None) -> subprocess.CompletedProcess:
    """
    Run ScDowngrade to convert SC2 files to SC1.
    
    Args:
        input_path: Path to input .sc file
        output_path: Path for output .sc file
        version: Target version (1.0 or 0.5, None for auto)
    """
    args = [input_path, output_path]
    if version is not None:
        args.append(str(version))
    
    return run_tool("sc_downgrade", args)


def run_sctx_converter(
    mode: str,
    input_path: str,
    output_path: str,
    transparent: bool = True
) -> subprocess.CompletedProcess:
    """
    Run SctxConverter to decode/encode SCTX textures.
    
    Args:
        mode: "decode" or "encode"
        input_path: Path to input file
        output_path: Path for output file
        transparent: Add -t flag for transparency
    """
    args = [mode, input_path, output_path]
    if transparent:
        args.append("-t")
    
    return run_tool("sctx_converter", args)


def run_pvr_tex_tool(
    input_path: str,
    output_path: str,
    color_space: str = "sRGB"
) -> subprocess.CompletedProcess:
    """
    Run PVRTexToolCLI to convert KTX textures.
    
    Args:
        input_path: Path to input .ktx file
        output_path: Path for output .png file
        color_space: Color space (default: sRGB)
    """
    args = ["-i", input_path, "-d", output_path, "-ics", color_space, "-noout"]
    return run_tool("pvr_tex_tool", args)


def check_tool_availability() -> dict:
    """
    Check which tools are available and how they would be executed.
    
    Returns:
        Dictionary with tool names as keys and ToolInfo as values
    """
    tools = ["sc_downgrade", "sctx_converter", "pvr_tex_tool", "sc_tex"]
    return {name: get_tool_info(name) for name in tools}


def print_tool_status():
    """Print status of all tools to console."""
    from colorama import Fore, Style, init
    init()
    
    tools = check_tool_availability()
    os_type = detect_os()
    wine_available = is_wine_available()
    
    print(f"\n{Fore.CYAN}═══ Tool Status ═══{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}Environment:{Style.RESET_ALL}")
    print(f"  OS: {os_type.value}")
    print(f"  Wine Available: {wine_available}")
    if wine_available:
        print(f"  Wine Command: {get_wine_command()}")
    
    print(f"\n{Fore.YELLOW}Tools:{Style.RESET_ALL}")
    
    for name, info in tools.items():
        if info.available:
            status = f"{Fore.GREEN}✓{Style.RESET_ALL}"
            mode = f"({info.execution_mode.value})"
        else:
            status = f"{Fore.RED}✗{Style.RESET_ALL}"
            mode = "(unavailable)"
        
        path_str = str(info.path) if info.path else "Not found"
        print(f"  {status} {name} {mode}")
        print(f"      Path: {path_str}")
        if info.is_windows_binary and os_type != OperatingSystem.WINDOWS:
            print(f"      Note: Windows binary, requires Wine")
    
    # Suggestions
    print(f"\n{Fore.YELLOW}Suggestions:{Style.RESET_ALL}")
    
    missing_tools = [name for name, info in tools.items() if not info.available]
    if missing_tools:
        print(f"  {Fore.RED}Missing tools:{Style.RESET_ALL} {', '.join(missing_tools)}")
        
        if os_type == OperatingSystem.MACOS:
            print(f"\n  To use Windows tools via Wine:")
            print(f"    brew install wine-stable")
            print(f"\n  To compile native tools:")
            print(f"    See BUILD_MACOS.md")
    else:
        print(f"  {Fore.GREEN}All tools available!{Style.RESET_ALL}")
    
    print()


if __name__ == "__main__":
    print_tool_status()
