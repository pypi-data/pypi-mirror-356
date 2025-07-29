import argparse

def _create_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="downloader-cli", description="A modern CLI tool for downloading files with progress bars", formatter_class=argparse.RawDescriptionHelpFormatter, epilog="\nExamples:\n  %(prog)s https://example.com/file.zip\n  %(prog)s https://example.com/file.zip /path/to/save/\n  %(prog)s --batch urls.txt\n  %(prog)s --resume https://example.com/large-file.zip\n")
    parser.add_argument('url', help="URL to download or path to file containing URLs (with --batch)", metavar='URL')
    parser.add_argument('destination', nargs='?', help="Destination path (file or directory)", metavar='DESTINATION')

    behavior_group: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group()
    behavior_group.add_argument('-f', '--force',  action='store_true', help="Overwrite existing files")
    behavior_group.add_argument('-c', '--resume', action='store_true', help="Resume interrupted downloads")

    output_group: argparse._ArgumentGroup = parser.add_argument_group('Output Options')
    output_group.add_argument('-e', '--echo',  action='store_true', help="Print file path to stdout after download")
    output_group.add_argument('-q', '--quiet', action='store_true', help="Suppress progress information")
    output_group.add_argument('-b', '--batch', action='store_true', help="Download multiple URLs from file")

    ui_group: argparse._ArgumentGroup = parser.add_argument_group('UI Customization')
    ui_group.add_argument('--done',    default="▓", help="Icon for completed progress (default: ▓)")
    ui_group.add_argument('--left',    default="░", help="Icon for remaining progress (default: ░)")
    ui_group.add_argument('--current', default="▓", help="Icon for current progress position (default: ▓)")
    ui_group.add_argument('--border',  default="|", help="Border characters for progress bar (default: |)")

    color_group: argparse._ArgumentGroup  = parser.add_argument_group('Color Options')
    color_group.add_argument('--color-done',    default="", help="Color for completed progress icon")
    color_group.add_argument('--color-left',    default="", help="Color for remaining progress icon")
    color_group.add_argument('--color-current', default="", help="Color for current progress icon")

    return parser

def parse_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = _create_parser()
    return parser.parse_args()
