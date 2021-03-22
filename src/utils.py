import os
from datetime import datetime
import json
import fastavro


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


def export_json(data, file, output_folder=None):
    """
    Export data to .json format

    :param data: A dict containing data to be exported
    :type data: dict
    :param file: original .avro filename
    :type file: str
    :param output_folder: Folder in which dump .json files
    :type output_folder: str, optional
    """
    filename = os.path.split(file)[1].split(".")[0]

    if output_folder:
        output_path = os.path.join(output_folder, filename)
    else:
        output_path = os.path.join(filename)

    with open(f"{output_path}.json", "w") as f:
        json.dump(data, f)


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
