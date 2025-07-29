# SPDX-FileCopyrightText: 2023 CELESTIFYX Team
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypedDict

class ProgressInfo(TypedDict):
    downloaded: int
    total: int | None
    speed: float
    eta: float
    percent: float | None

ColorMap: type[dict[str, int]] = dict[str, int]
BorderIcons: type[tuple[str, str]] = tuple[str, str]
SizeInfo: type[tuple[float, str]] = tuple[float, str]
TimeInfo: type[tuple[float, str]] = tuple[float, str]
SpeedInfo: type[tuple[float, str]] = tuple[float, str]
