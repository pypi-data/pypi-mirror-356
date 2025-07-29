# SPDX-FileCopyrightText: 2023 CELESTIFYX Team
# SPDX-License-Identifier: GPL-3.0-or-later

import itertools

from typing import Iterator

from wgetx.color import ShellColor
from wgetx.typedefs import ProgressInfo
from wgetx.utils import (format_size, format_speed, format_time, get_terminal_width)

class ProgressBar:
    def __init__(self, color_engine: ShellColor, done_icon: str = "▓", left_icon: str = "░", current_icon: str = "▓", border_left: str = "|", border_right: str = "|", done_color: str = "", left_color: str = "", current_color: str = "", quiet: bool = False) -> None:
        self.color_engine = color_engine
        self._done_icon = done_icon
        self._left_icon = left_icon
        self._current_icon = current_icon
        self.border_left = border_left
        self.border_right = border_right
        self._done_color = done_color
        self._left_color = left_color
        self._current_color = current_color
        self.quiet = quiet
        self._cycle_iterator: Iterator[int] | None = None

    @property
    def done_icon(self) -> str:
        return self.color_engine.wrap_in_color(self._done_icon, self._done_color)

    @property
    def left_icon(self) -> str:
        return self.color_engine.wrap_in_color(self._left_icon, self._left_color)

    @property
    def current_icon(self) -> str:
        return self.color_engine.wrap_in_color(self._current_icon, self._current_color)

    def _get_cycle_position(self, bar_width: int) -> int:
        if self._cycle_iterator is None:
            self._cycle_iterator = itertools.cycle(range(1, bar_width + 1))

        return next(self._cycle_iterator)

    def _create_progress_icons(self, done_count: int, remaining_count: int) -> str:
        if done_count == 0:
            return ""

        if remaining_count == 0:
            return self.done_icon * done_count

        return self.done_icon * (done_count - len(self._current_icon)) + self.current_icon

    @staticmethod
    def _calculate_bar_width(status_length: int, terminal_width: int) -> int:
        base_width:     int = 40
        required_space: int = status_length + 7

        while base_width > 0:
            if required_space + base_width <= terminal_width:
                break

            base_width //= 2

        return base_width

    def create_bar(self, status: str, progress_info: ProgressInfo) -> str:
        terminal_width: int = get_terminal_width(self.quiet)
        bar_width:      int = self._calculate_bar_width(len(status), terminal_width)

        if bar_width <= 0:
            return status

        space_count: int = terminal_width - (len(status) + 2 + bar_width + 5)
        status += " " * max(0, space_count)

        status += "\033[1m\033[1;34m"

        if progress_info["percent"] is not None:
            done_count:      int = int(progress_info["percent"] / (100 / bar_width))
            remaining_count: int = bar_width - done_count

            bar_content: str = (self._create_progress_icons(done_count, remaining_count) + self.left_icon * remaining_count)
        else:
            current_pos: int = self._get_cycle_position(bar_width)
            bar_content: str = (" " * (current_pos - 1) + self.current_icon + " " * (bar_width - current_pos))

        status += (self.border_left + bar_content + self.border_right)
        status += "\033[0m"

        if progress_info["percent"] is not None:
            status += " " + str(round(progress_info['percent'])) + "%"

        return status

    @staticmethod
    def format_status(progress_info: ProgressInfo) -> str:
        (downloaded_size, size_unit) = format_size(progress_info["downloaded"])
        (speed_value, speed_unit)    = format_speed(progress_info["speed"])

        status: str = str(round(downloaded_size)) + " " + size_unit + " | " + str(round(speed_value)) + " " + speed_unit

        if progress_info["total"] is not None and (progress_info["eta"] > 0):
            (eta_value, eta_unit) = format_time(progress_info["eta"])
            status += " || ETA: " + str(round(eta_value)) + " " + eta_unit

        return status
