import glob
from argparse import Namespace
import os
import utils
import checker
import checker_cli


def test_run_passing_checks(good_avro, config):
    feed_class = checker.DifOutput(good_avro)

    for check in config["common_checks"]:
        feed_class.check_expr(check)

    # Check if the counter was updated accordingly
    assert feed_class.failed == 0


def test_run_failing_checks(bad_avro, config):
    feed_class = checker.DifOutput(bad_avro)

    for check in config["common_checks"]:
        feed_class.check_expr(check)

    # Check if the counter was updated accordingly
    assert feed_class.failed > 0


def test_cli_runner(monkeypatch, config, good_avro):
    def mocked_get_args():
        return Namespace(
            avro_path="some_avros/", checks_file="fake_checks.json", export_json=False
        )

    def mock_glob_glob(path):
        res = [os.path.join("my_avro_files", "fake_file.avro")]
        return res

    def mock_read_checks(path):
        return config

    def mock_read_avro(fpath):
        return good_avro

    monkeypatch.setattr(checker_cli, "get_args", mocked_get_args)
    monkeypatch.setattr(utils, "read_checks", mock_read_checks)
    monkeypatch.setattr(utils, "read_avro", mock_read_avro)
    monkeypatch.setattr(glob, "glob", mock_glob_glob)

    res = checker_cli.main()

    assert res["passed"] == 6
    assert res["failed"] == 0
