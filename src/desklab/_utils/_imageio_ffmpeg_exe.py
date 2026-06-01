# ==============================================================================
# The following code block or function incorporates code from 'imageio'.
#
# Copyright (c) 2019-2025, imageio
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLD

import os
import platform
import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional, no_type_check

FNAME_PER_PLATFORM = {
    "macos-aarch64": "ffmpeg-macos-aarch64-v7.1",
    "macos-x86_64": "ffmpeg-macos-x86_64-v7.1",
    "windows-x86_64": "ffmpeg-win-x86_64-v7.1.exe",
    "windows-i686": "ffmpeg-win32-v4.2.2.exe",
    "linux-aarch64": "ffmpeg-linux-aarch64-v7.0.2",
    "linux-x86_64": "ffmpeg-linux-x86_64-v7.0.2",
}


def _get_os_string() -> str:
    if sys.platform.startswith("win"):
        return "windows"
    elif sys.platform.startswith("darwin"):
        return "macos"
    elif sys.platform.startswith("linux"):
        return "linux"
    return sys.platform


def _get_arch() -> str:
    is_64_bit = sys.maxsize > 2**32
    machine = platform.machine()

    if machine == "armv7l":
        return "armv7"
    elif is_64_bit and machine.startswith(("arm", "aarch64")):
        return "aarch64"
    elif is_64_bit:
        return "x86_64"
    return "i686"


def _get_platform() -> str:
    return _get_os_string() + "-" + _get_arch()


@no_type_check
def _popen_kwargs() -> dict[str, Any]:
    startupinfo = None
    creationflags = 0
    if sys.platform.startswith("win"):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
    }


def _is_valid_exe(exe: str) -> bool:
    cmd = [exe, "-version"]
    try:
        with open(os.devnull, "w") as null:
            subprocess.check_call(
                cmd, stdout=null, stderr=subprocess.STDOUT, **_popen_kwargs()
            )
        return True
    except (OSError, ValueError, subprocess.CalledProcessError):
        return False


@lru_cache(maxsize=1)
def _find_ffmpeg_path() -> Optional[Path]:
    plat = _get_platform()
    os_str = _get_os_string()
    expected_filename = FNAME_PER_PLATFORM.get(plat, "ffmpeg")

    possible_paths: list[Path] = []
    home = Path.home()

    imageio_cache_dir = home / ".imageio" / "ffmpeg"
    desklab_cache_dir = home / ".desklab" / "ffmpeg"

    possible_paths.extend([
        imageio_cache_dir / expected_filename,
        desklab_cache_dir / expected_filename,
    ])

    prefix_path = Path(sys.prefix)
    if os_str == "windows":
        possible_paths.append(prefix_path / "Library" / "bin" / "ffmpeg.exe")
    else:
        possible_paths.append(prefix_path / "bin" / "ffmpeg")

    if os_str == "windows":
        appdata_local = Path(os.environ.get(
            "LOCALAPPDATA", home / "AppData/Local"))
        possible_paths.extend([
            appdata_local / "Microsoft/WindowsApps/ffmpeg.exe",
            home / "ffmpeg" / "bin" / "ffmpeg.exe",
            Path("C:/Program Files/ffmpeg/bin/ffmpeg.exe"),
            Path("C:/ffmpeg/bin/ffmpeg.exe"),
        ])
    elif os_str == "macos":
        possible_paths.extend([
            Path("/opt/homebrew/bin/ffmpeg"),
            Path("/usr/local/bin/ffmpeg"),
            Path("/usr/bin/ffmpeg"),
            home / "bin" / "ffmpeg",
        ])
    elif os_str == "linux":
        possible_paths.extend([
            Path("/usr/bin/ffmpeg"),
            Path("/usr/local/bin/ffmpeg"),
            Path("/snap/bin/ffmpeg"),
            home / "bin" / "ffmpeg",
            home / ".local" / "bin" / "ffmpeg",
        ])

    for path in possible_paths:
        if path.is_file() and _is_valid_exe(str(path)):
            return path

    if _is_valid_exe("ffmpeg"):
        return Path("ffmpeg")

    return None


def get_ffmpeg_exe() -> Path:
    exe_env = os.getenv("DESKLAB_FFMPEG_EXE") or os.getenv(
        "IMAGEIO_FFMPEG_EXE")
    if exe_env:
        return Path(exe_env)

    detected_path = _find_ffmpeg_path()
    if detected_path:
        return detected_path

    raise RuntimeError(
        "No ffmpeg exe could be found. Install ffmpeg on your system, "
        "or set the DESKLAB_FFMPEG_EXE environment variable."
    )
