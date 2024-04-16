"""
Tests for the functions module.
"""

from unittest.mock import patch
from functions import parse_java_file

def test_parse_java_file():
    f = open("test_files/File1.java")
    with patch("snowflake.snowpark.files.SnowflakeFile.open") as mock_open:
        mock_open.return_value = f
        file_info = parse_java_file("test.java")
        class_info = file_info[0]
        assert (class_info is not None)
        assert class_info['name'] == 'File1.main'