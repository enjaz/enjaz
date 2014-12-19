"""
Tests for the Media Center app.
"""
# Notes on handling of tests in django:
# (1) Each test suite (class) starts with an empty database.
# (2) Test methods should start with the prefix test_* in order to be detected
# (3) setUp is the name that should be used to set up the testing environment


# Rather than creating all tests here, it's neater to create
# them seperately and just import them here.

from media.test_suites.followupreport_tests import *
from media.test_suites.views import *
from media.test_suites.models import *