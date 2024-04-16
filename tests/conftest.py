"""
Fixtures and configurations for the PyTest suite
"""

import pytest
from snowflake.snowpark.session import Session


@pytest.fixture
def session(scope='module'):
    # pylint: disable=unused-argument
    """
    Creates a Session object for tests
    """

    return Session.builder.getOrCreate()