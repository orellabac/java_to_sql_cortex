"""
Tests for the procedures module.
"""

from unittest.mock import patch
from functions import parse_java_file
from procedures import convert_with_cortex

from snowflake.snowpark.session import Session

def test_procedures(session: Session):
    f = open("test_files/File1.java")
    with patch("snowflake.snowpark.files.SnowflakeFile.open") as mock_open:
        mock_open.return_value = f
        file_info = parse_java_file("test.java")
        main_method = file_info[0]['code']
        converted_code = convert_with_cortex(session,main_method)
        assert converted_code is not None