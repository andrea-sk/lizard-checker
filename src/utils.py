from datetime import datetime
import fastavro
import json


def read_avro(file_path):
    """
    Read an AVRO file and returns one record for testing
    purposes

    :param file_path: A file path pointing to an .avro file
    :type file_path: str
    :return: A dictionary containing test data
    :rtype: Dict
    """
    res = []
    print(f"\nopening: {file_path}")
    with open(file_path, "rb") as f:
        for record in fastavro.reader(f):
            res.append(record)

    return res[0]  # we need just one record to run tests


def validate_timestamp(timestamp, territory=None):
    """
    Validate a timestamp according to

    :param timestamp: A timestamp from the .avro file.
    :type timestamp: str
    :param territory: Territory/Region. Needed to check whether a timezone should be
      expected or not in the timestamp, defaults to None
    :type territory: str, default
    :return: `True` if validated, `False` otherwise
    :rtype: Bool
    """
    # GB has no timezone attached
    if territory == "GB":
        try:
            datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            return True
        except ValueError:
            return False

    # Anything else has hour offsets according to the timezone
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
        return True
    except ValueError:
        return False


def read_checks(fpath):
    with open(fpath, "r") as f:
        checks = json.load(f)
    return checks


class bcolors:
    """
    Colourful console output
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
