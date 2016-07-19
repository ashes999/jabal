import unittest
from src.io import *

class TestWatch:
    def test_validate_args_throws_if_path_doesnt_exist(self):
        args = ['path/to/nothing']
        AppBuilder().watch(args)