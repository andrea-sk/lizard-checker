import os
import glob
from checker import check_assert
from checker import run_checks
import utils


def test_single_check(single_expr, good_avro, bad_avro):
    # True with good input
    good_res = check_assert(single_expr, good_avro)
    assert good_res

    # False with bad input
    bad_res = check_assert(single_expr, bad_avro)
    assert not bad_res


def test_run_passing_checks(monkeypatch, config, good_avro):
    def mock_glob_glob(path):
        res = [
            os.path.join("my_avro_files", "gb-dcm-user-stream-eviction-2021-03-16.avro")
        ]
        return res

    def mock_read_avro(file_path):
        return good_avro

    monkeypatch.setattr(glob, "glob", mock_glob_glob)
    monkeypatch.setattr(utils, "read_avro", mock_read_avro)

    res_good = run_checks("fake_folder", config)

    assert res_good["passed"] == 10 and res_good["failed"] == 0


def test_run_failing_checks(monkeypatch, config, bad_avro):
    def mock_glob_glob(path):
        res = [
            os.path.join("my_avro_files", "gb-dcm-user-stream-eviction-2021-03-16.avro")
        ]
        return res

    def mock_read_avro(file_path):
        return bad_avro

    monkeypatch.setattr(glob, "glob", mock_glob_glob)
    monkeypatch.setattr(utils, "read_avro", mock_read_avro)

    res_bad = run_checks("fake_folder", config)

    assert res_bad["failed"] != 0
