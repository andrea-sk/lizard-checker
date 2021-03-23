import argparse
import utils
from checker import DifOutput
import glob
import os


def main():
    # TODO: add execution time prompt
    args = get_args()
    # TODO: should this be factored out in order to be unit-testable?
    checks = utils.read_checks(args.checks_file)

    common_checks = checks["common_checks"]
    feeds = checks["feeds"]

    results = {"passed": 0, "failed": 0, "warnings": 0}
    for feed in feeds:
        for glob_expr, checks in feed.items():
            files = glob.glob(os.path.join(args.avro_path, glob_expr))
            for file in files:
                data = utils.read_avro(file)
                feed_class = DifOutput(data)  # init feed class

                # Common checks block
                for expr in common_checks:
                    feed_class.check_expr(expr)

                # Feed-specific tests
                for expr in checks:
                    feed_class.check_expr(expr)

                # Update counter for final reporting
                results["passed"] += feed_class.passed
                results["failed"] += feed_class.failed
                results["warnings"] += feed_class.warning

                # Export feed in .json format if requested
                if args.export_json:
                    fname = os.path.split(file)[1].split(".")[0]
                    feed_class.data_to_json(fname)

    # Pretty print test results
    print("")
    print("~" * 50)
    print(f"{utils.bcolors.OKGREEN}PASSED: {results['passed']}{utils.bcolors.ENDC}")
    print(f"{utils.bcolors.FAIL}FAILED: {results['failed']}{utils.bcolors.ENDC}")
    print(f"{utils.bcolors.WARNING}WARNINGS: {results['warnings']}{utils.bcolors.ENDC}")

    return results


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
