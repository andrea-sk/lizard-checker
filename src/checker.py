import os
import glob

from utils import read_avro, validate_timestamp, bcolors  # noqa: F401


def check_assert(expr, data):
    """
    Evaluate an expression on test data and checks if assert
        passes correctly

    :param expr: An expression to evaluate
    :type expr: str
    :param data: Some test data
    :type data: dict
    """
    data = data
    eval_res = eval(expr)
    try:
        assert eval_res
        print(f"\033[92m{expr} passed\033[0m")
    except AssertionError:
        print(f"\033[93m{expr} didn't go well\033[0m")


def run_checks(avro_folder, configs):
    """
    Traverses a config dict and run checks iteratively

    :param avro_folder: Path pointing to the folder containing AVRO files
    :type avro_foolder: str
    :param configs: A dict of configs (more on this in README.md)
    :type configs: dict
    """
    # print(f"confs {configs}")
    for feed in configs["feeds"]:
        glob_expr = list(feed.keys())[0]
        files = glob.glob(os.path.join(avro_folder, glob_expr))

        for glob_expr, checks in feed.items():
            files = glob.glob(os.path.join(avro_folder, glob_expr))
            for file in files:
                data = read_avro(file)
                print(data)
                # Common checks block
                for expr in configs["common_checks"]:
                    check_assert(expr, data)

                # Feed specific checks
                for expr in checks:
                    check_assert(expr, data)
