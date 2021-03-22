import os
import glob

from utils import validate_timestamp  # noqa: F401

# Double import requred to make monkeypatching work
import utils


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
        print(f"{utils.bcolors.OKGREEN}{expr} passed{utils.bcolors.ENDC}")
        return True
    except AssertionError:
        print(f"{utils.bcolors.FAIL}{expr} didn't go well{utils.bcolors.ENDC}")
        return False


def run_checks(avro_folder, configs):
    """
    Traverses a config dict and run checks iteratively

    :param avro_folder: Path pointing to the folder containing AVRO files
    :type avro_foolder: str
    :param configs: A dict of configs (more on this in README.md)
    :type configs: dict
    """
    res_counter = {"passed": 0, "failed": 0}  # init counter
    # TODO: this was done in a rush, it could be probably refactored using
    #   `itertools`.
    for feed in configs["feeds"]:
        for glob_expr, checks in feed.items():
            files = glob.glob(os.path.join(avro_folder, glob_expr))
            for file in files:
                data = utils.read_avro(file)
                print(data)
                # Common checks block
                for expr in configs["common_checks"]:
                    if check_assert(expr, data):
                        res_counter["passed"] += 1
                    else:
                        res_counter["failed"] += 1

                # Feed specific checks
                for expr in checks:
                    if check_assert(expr, data):
                        res_counter["passed"] += 1
                    else:
                        res_counter["failed"] += 1

    return res_counter
