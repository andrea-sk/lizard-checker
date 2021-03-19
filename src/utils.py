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
