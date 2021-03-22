from utils import validate_timestamp


def test_validate_ts():
    timestamp_timezone = "2021-03-16T11:10:24.921-04:00"
    timestamp_notimezone = "2021-03-16T12:51:43.625Z"
    malformed_timestamp = "2021-03-16"

    res_timestamp = validate_timestamp(timestamp_timezone)
    res_notimezone = validate_timestamp(timestamp_notimezone, territory="GB")
    malformed_res = validate_timestamp(malformed_timestamp)

    assert res_timestamp
    assert res_notimezone
    assert not malformed_res
