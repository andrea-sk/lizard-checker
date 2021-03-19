import json
import argparse
from checker import run_checks


def main():
    args = get_args()
    avro_path = args.avro_path

    with open(args.checks_file, "r") as f:
        checks = json.load(f)
    run_checks(avro_path, checks)


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

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main()
