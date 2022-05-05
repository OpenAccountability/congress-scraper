from argparse import ArgumentParser, Namespace

from congress.version import version

authors: list = ["Nicholas M. Synovic"]
name: str = "Congress"


def memberArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Member Scraper",
        usage="A tool to download the metadata for all Congress Members listed on https://congress.gov",
        description="This tool downloads all of the front matter for Congress Members listed on https://congress.gov",
        epilog=f"Created by: {', '.join(authors)}",
    )

    parser.add_argument(
        "-v",
        "--version",
        required=False,
        type=bool,
        default=False,
        action="version",
        version=f"{version()}",
        help="Display the version",
    )

    return parser.parse_args()
