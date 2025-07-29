# SPDX-FileCopyrightText: 2023 CELESTIFYX Team
# SPDX-License-Identifier: GPL-3.0-or-later

import _io
import sys
import time

from os import path
from urllib.request import (Request, urlopen)

from wgetx.color import ShellColor
from wgetx.progress import ProgressBar
from wgetx.typedefs import ProgressInfo
from wgetx.utils import (extract_border_icons, get_filename_from_url, is_valid_url, parse_urls_from_file)

class Download:
    def __init__(self, url: str, destination: str | None = None, overwrite: bool = False, continue_download: bool = False, echo: bool = False, quiet: bool = False, batch: bool = False, icon_done: str = "▓", icon_left: str = "░", icon_current: str = "▓", icon_border: str = "|", color_done: str = "", color_left: str = "", color_current: str = "") -> None:
        self.url = url
        self.destination = destination
        self.passed_directory: str | None = None
        self.overwrite = overwrite
        self.continue_download = continue_download
        self.echo = echo
        self.quiet = quiet
        self.batch = batch
        self.file_exists: bool = False
        self.basename: str = ""

        self.color_engine: ShellColor = ShellColor()
        self._validate_colors(color_done, color_left, color_current)

        (border_left, border_right) = extract_border_icons(icon_border)
        self.progress_bar: ProgressBar = ProgressBar(self.color_engine, done_icon=icon_done, left_icon=icon_left, current_icon=icon_current, border_left=border_left, border_right=border_right, done_color=color_done, left_color=color_left, current_color=color_current, quiet=quiet)

        self.headers: dict[str, str] = {}
        self.file_size: int | None = None
        self.output_stream: _io.TextIOWrapper = sys.stderr if echo else sys.stdout

    def _validate_colors(self, *colors: str) -> None:
        for color in colors:
            if color and not self.color_engine.is_valid_color(color):
                raise ValueError("Invalid color: " + color)

    def _build_resume_headers(self, resume_byte: int) -> None:
        self.headers = {"Range": "bytes=" + str(resume_byte) + "-"}
        print("Resuming download at: " + str(resume_byte) + " bytes", file=self.output_stream)

    def _handle_existing_file(self) -> None:
        if self.overwrite:
            return

        if not self.continue_download:
            print("ERROR: File exists. Use --force to overwrite or --resume to continue", file=self.output_stream)
            sys.exit(1)

        current_size: int = path.getsize(self.destination)

        try:
            with urlopen(url=self.url) as response:
                original_size: str = response.info().get('Content-Length')

            if original_size is None:
                print("WARNING: Cannot verify partial download size", file=self.output_stream)
                self._build_resume_headers(current_size)

                return

            if current_size < int(original_size):
                self._build_resume_headers(current_size)

        except Exception as e:
            print("ERROR: Cannot resume download: " + str(e), file=self.output_stream)
            sys.exit(1)

    def _prepare_connection(self) -> None:
        try:
            request = Request(url=self.url, headers=self.headers)
            self.connection = urlopen(request)

            content_length = self.connection.info().get('Content-Length')
            self.file_size = int(content_length) if content_length else None

        except Exception as e:
            print("ERROR: Failed to connect: " + str(e), file=self.output_stream)
            sys.exit(1)

    def _resolve_destination(self) -> None:
        if self.destination is not None and path.isdir(self.destination):
            self.passed_directory = self.destination
            self.destination = path.join(self.destination, get_filename_from_url(self.url))

        if self.destination is None:
            self.destination = get_filename_from_url(self.url)

        if path.exists(self.destination):
            self._handle_existing_file()
            self.file_exists = True

    def _calculate_progress_info(self, downloaded: int, start_time: float, current_time: float) -> ProgressInfo:
        elapsed_time: float = current_time - start_time

        if elapsed_time == 0:
            return ProgressInfo(downloaded=downloaded, total=self.file_size, speed=0.0, eta=0.0, percent=None)

        speed: float = (downloaded / 1024) / elapsed_time
        eta:   float = ((self.file_size - downloaded) / 1024) / speed if self.file_size and speed > 0 else 0.0

        percent: float | None = (downloaded * 100 / self.file_size) if self.file_size else None
        return ProgressInfo(downloaded=downloaded, total=self.file_size, speed=speed, eta=eta, percent=percent)

    def _download_file(self) -> bool:
        try:
            self._resolve_destination()
            self._prepare_connection()

            if self.file_size and not self.quiet:
                from .utils import format_size
                size_value, size_unit = format_size(self.file_size)
                print("Size: " + str(round(size_value)) + " " + size_unit, file=self.output_stream)

            action:  str = "Overwriting" if (self.file_exists and self.overwrite) else "Saving as"
            message: str = action + ": " + self.destination

            self.output_stream.write(message + ("..." if self.quiet else "\n"))

            if not self.quiet:
                self.output_stream.flush()

            with open(file=self.destination, mode='ab') as file_stream:
                downloaded_bytes: int = 0
                block_size:       int = 8192

                start_time: float = time.time()

                while True:
                    buffer: bytes = self.connection.read(block_size)

                    if not buffer:
                        break

                    downloaded_bytes += len(buffer)
                    file_stream.write(buffer)

                    if not self.quiet:
                        progress_info: ProgressInfo = self._calculate_progress_info(downloaded_bytes, start_time, time.time())

                        status:       str = self.progress_bar.format_status(progress_info)
                        progress_bar: str = self.progress_bar.create_bar(status, progress_info)

                        self.output_stream.write('\r' + progress_bar)
                        self.output_stream.flush()

            self.output_stream.write("...success\n" if self.quiet else "\n")

            if self.quiet:
                self.output_stream.flush()

            self.basename = path.basename(self.destination)
            return True

        except KeyboardInterrupt:
            self.output_stream.flush()
            print("\nDownload interrupted by user. Exiting gracefully.")

            sys.exit(0)
        except Exception as e:
            print("ERROR: Download failed: " + str(e), file=self.output_stream)
            return False

    def _parse_urls(self) -> list[str]:
        if is_valid_url(self.url):
            return [self.url]

        if not self.batch:
            print(self.url + ": Not a valid URL. Use --batch for file input.", file=self.output_stream)
            sys.exit(1)

        try:
            return parse_urls_from_file(self.url)
        except FileNotFoundError as e:
            print("ERROR: " + str(e), file=self.output_stream)
            sys.exit(1)

    def download(self) -> bool:
        urls: list[str] = self._parse_urls()
        success: bool = True

        for url in urls:
            self.url = url
            success = self._download_file() and success

            self.destination = self.passed_directory

        return success
