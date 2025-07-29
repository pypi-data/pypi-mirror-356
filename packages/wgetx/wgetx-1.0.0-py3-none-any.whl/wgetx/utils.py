# SPDX-FileCopyrightText: 2023 CELESTIFYX Team
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from os import (get_terminal_size, name as os_name, path)

from wgetx.typedefs import (BorderIcons, SizeInfo, SpeedInfo, TimeInfo)

def extract_border_icons(icon: str) -> BorderIcons:
    return (icon, icon) if len(icon) == 1 else ((icon[0], icon[1]) if len(icon) == 2 else ("|", "|"))

def format_size(size: int) -> SizeInfo:
    units: list[str] = ['bytes', 'KB', 'MB', 'GB']
    formatted_size: float = float(size)
    unit_index: int = 0

    while (formatted_size > 1024) and (unit_index < (len(units) - 1)):
        formatted_size /= 1024
        unit_index += 1

    return formatted_size, units[unit_index]

def format_time(seconds: float) -> TimeInfo:
    units: list[str] = ['s', 'm', 'h', 'd']
    unit_index: int = 0

    while (seconds > 60) and (unit_index < (len(units) - 1)):
        seconds /= 60
        unit_index += 1

    return seconds, units[unit_index]

def format_speed(speed: float) -> SpeedInfo:
    units: list[str] = ['Kb/s', 'Mb/s', 'Gb/s']
    unit_index: int = 0

    while (speed > 1000) and (unit_index < (len(units) - 1)):
        speed /= 1000
        unit_index += 1

    return speed, units[unit_index]

def get_terminal_width(quiet: bool = False) -> int:
    if quiet:
        return 50

    cols = get_terminal_size().columns
    return cols if os_name != "nt" else cols - 1

def is_valid_url(url: str) -> bool:
    return bool(re.match(pattern=r"^https?://|^file://", string=url))

def is_valid_file_path(file_path: str) -> bool:
    return path.exists(file_path) and path.isfile(file_path)

def get_filename_from_url(url: str) -> str:
    return url.split(sep='/')[-1].split(sep='?')[0] or 'temp'

def parse_urls_from_file(file_path: str) -> list[str]:
    expanded_path: str = path.expanduser(file_path)

    if not is_valid_file_path(expanded_path):
        raise FileNotFoundError("Invalid file path: " + str(expanded_path))

    with open(expanded_path, encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]
