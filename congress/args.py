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
        "-o",
        "--output",
        default="members.csv",
        type=str,
        required=False,
        help="Save the output to disk. DEFAULT: members.csv",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{version()}",
        help="Display the version",
    )

    return parser.parse_args()


def billsArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Bills Scraper",
        usage="A tool to download the metadata for all Congress Bills listed on https://congress.gov",
        description="This tool downloads all of the front matter for Congress Bills listed on https://congress.gov",
        epilog=f"Created by: {', '.join(authors)}",
    )

    parser.add_argument(
        "-i",
        "--input",
        default="members.csv",
        type=str,
        required=False,
        help="File containing member URLs in JSON format. DEFAULT: members.csv",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="bills.csv",
        type=str,
        required=False,
        help="Save the output to disk. DEFAULT: bills.csv",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{version()}",
        help="Display the version",
    )

    return parser.parse_args()
