# SPDX-FileCopyrightText: 2023 CELESTIFYX Team
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import (Enum, auto)
from typing import Union

class ColorCode(Enum):
    RESET   = 0
    BLACK   = 30
    RED     = 31
    GREEN   = 32
    YELLOW  = 33
    BLUE    = 34
    MAGENTA = 35
    CYAN    = 36
    WHITE   = 37

    BRIGHT_BLACK   = 90
    BRIGHT_RED     = 91
    BRIGHT_GREEN   = 92
    BRIGHT_YELLOW  = 93
    BRIGHT_BLUE    = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN    = 96
    BRIGHT_WHITE   = 97

class ColorStyle(Enum):
    NORMAL    = auto()
    BOLD      = auto()
    DIM       = auto()
    ITALIC    = auto()
    UNDERLINE = auto()

class ShellColor:
    _STYLE_CODES: dict[ColorStyle, int] = {
        ColorStyle.NORMAL:    0,
        ColorStyle.BOLD:      1,
        ColorStyle.DIM:       2,
        ColorStyle.ITALIC:    3,
        ColorStyle.UNDERLINE: 4
    }

    _COLOR_ALIASES: dict[str, ColorCode] = {
        'reset':   ColorCode.RESET,
        'black':   ColorCode.BLACK,
        'red':     ColorCode.RED,
        'green':   ColorCode.GREEN,
        'yellow':  ColorCode.YELLOW,
        'blue':    ColorCode.BLUE,
        'magenta': ColorCode.MAGENTA,
        'cyan':    ColorCode.CYAN,
        'white':   ColorCode.WHITE
    }

    def __init__(self) -> None:
        self._reset_sequence = "\033[0m"

    @staticmethod
    def _is_ansi_sequence(text: str) -> bool:
        return text.startswith(("\033[", r"\e["))

    def _build_ansi_sequence(self, color: ColorCode, style: ColorStyle = ColorStyle.BOLD) -> str:
        return self._reset_sequence if color == ColorCode.RESET else "\033[" + str(self._STYLE_CODES[style]) + ";" + str(color.value) + "m"

    def _resolve_color(self, color_input: Union[str, ColorCode]) -> ColorCode | None:
        return color_input if isinstance(color_input, ColorCode) else (self._COLOR_ALIASES.get(color_input.lower()) if isinstance(color_input, str) else None)

    def is_valid_color(self, color: Union[str, ColorCode]) -> bool:
        return True if self._is_ansi_sequence(str(color)) else bool(resolved := self._resolve_color(color)) and (resolved != ColorCode.RESET)

    def _colorize(self, text: str, color: Union[str, ColorCode, None] = None, style: ColorStyle = ColorStyle.BOLD, auto_reset: bool = True) -> str:
        return text if not color else (str(color) + text + (self._reset_sequence if auto_reset else '')) if self._is_ansi_sequence(str(color)) else (lambda resolved: ((self._build_ansi_sequence(resolved, style) + text + (self._reset_sequence if auto_reset else '')) if resolved else (_ for _ in ()).throw(ValueError("Invalid color: " + str(color)))))(self._resolve_color(color))

    def wrap_in_color(self, text: str, color: Union[str, ColorCode], skip_reset: bool = False) -> str:
        return self._colorize(text, color, auto_reset=not skip_reset)
