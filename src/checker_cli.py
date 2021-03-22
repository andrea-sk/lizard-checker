import json
import argparse
from utils import bcolors
from checker import run_checks


def main():
    args = get_args()
    avro_path = args.avro_path

    with open(args.checks_file, "r") as f:
        checks = json.load(f)
    res = run_checks(avro_path, checks, args.export_json)

    # Print results
    print("")
    print("~" * 50)
    print(f"{bcolors.OKGREEN}PASSED: {res['passed']}{bcolors.ENDC}")
    print(f"{bcolors.FAIL}FAILED: {res['failed']}{bcolors.ENDC}")


def get_args():
    parser = argparse.ArgumentParser(description="Run tests on .avro DIF file")

    parser.add_argument(
        "avro_path",
        type=str,
        metavar="AVRO_PATH",
        help="Path of the folder containing .avro files from DIF pipeline",
    )
    parser.add_argument(
        "checks_file",
        type=str,
        metavar="CHECKS_FILE",
        help=".json file containing checks for feeds in AVRO_PATH",
    )
    parser.add_argument(
        "--export-json",
        required=False,
        help="Export .avro feeds in json format for further checks",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main()
