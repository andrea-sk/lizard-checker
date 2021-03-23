import json

from utils import validate_timestamp  # noqa: F401

# Double import requred to make monkeypatching work
import utils


class DifOutput:
    def __init__(self, data):
        self.data = data
        self.passed = 0
        self.failed = 0
        self.warning = 0

    def check_expr(self, expr):
        """
        Evaluates an expression on data

        :param expr: An expression to be evaluated
        :type expr: str
        """
        # Stiil need to keep data around in the context?
        data = self.data  # noqa: F841

        try:
            eval_res = eval(expr)
            assert eval_res
            print(f"{utils.bcolors.OKGREEN}{expr} passed{utils.bcolors.ENDC}")
            self.passed += 1
        except AssertionError:
            print(f"{utils.bcolors.FAIL}{expr} didn't go well{utils.bcolors.ENDC}")
            self.failed += 1
        except KeyError as e:
            print(
                f"{utils.bcolors.WARNING}field {e} not found - check for typos{utils.bcolors.ENDC}"
            )
            self.warning += 1

    def data_to_json(self, filename):
        """
        Dumps data to json file

        :param filename: Name of the output file
        :type filename: str
        """
        with open(f"{filename}.json", "w") as f:
            json.dump(self.data, f)
