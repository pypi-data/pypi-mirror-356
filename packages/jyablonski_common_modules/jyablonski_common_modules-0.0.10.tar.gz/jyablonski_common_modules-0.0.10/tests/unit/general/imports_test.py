import pytest
from jyablonski_common_modules.aws import (
    S3PrefixCheckFail,
    get_secret_value,
    get_ssm_parameter,
    check_s3_file_exists,
)
from jyablonski_common_modules.general import (
    check_feature_flag,
    construct_date_partition,
    get_leading_zeroes,
    get_feature_flags,
)
from jyablonski_common_modules.logging import create_logger
from jyablonski_common_modules.sql import create_sql_engine, write_to_sql_upsert


# List of functions/classes to test, with their expected names
@pytest.mark.parametrize(
    "obj, name",
    [
        (create_sql_engine, "create_sql_engine"),
        (write_to_sql_upsert, "write_to_sql_upsert"),
        (S3PrefixCheckFail, "S3PrefixCheckFail"),
        (get_secret_value, "get_secret_value"),
        (get_ssm_parameter, "get_ssm_parameter"),
        (check_s3_file_exists, "check_s3_file_exists"),
        (check_feature_flag, "check_feature_flag"),
        (construct_date_partition, "construct_date_partition"),
        (get_leading_zeroes, "get_leading_zeroes"),
        (get_feature_flags, "get_feature_flags"),
        (create_logger, "create_logger"),
    ],
)
def test_imports_are_callable(obj, name):
    assert callable(obj), f"{name} should be callable"
