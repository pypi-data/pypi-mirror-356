# SPDX-FileCopyrightText: 2023 CELESTIFYX Team
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import sys

from wgetx.args import parse_arguments
from wgetx.download import Download

def main() -> None:
    try:
        arguments: argparse.Namespace = parse_arguments()

        downloader: Download = Download(url=arguments.url, destination=arguments.destination, overwrite=arguments.force, continue_download=arguments.resume, echo=arguments.echo, quiet=arguments.quiet, batch=arguments.batch, icon_done=arguments.done, icon_left=arguments.left, icon_current=arguments.current, icon_border=arguments.border, color_done=arguments.color_done, color_left=arguments.color_left, color_current=arguments.color_current)
        success: bool = downloader.download()

        if success and arguments.echo:
            print(downloader.destination)

        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print("Unexpected error: " + str(e), file=sys.stderr)
        sys.exit(1)
