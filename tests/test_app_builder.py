import pytest
import src.io.directory
from src.app_builder import AppBuilder

class TestAppBuilder:
    def test_validate_args_throws_if_path_doesnt_exist(self):
        args = ['path/to/nothing']
        with pytest.raises(Exception):
            AppBuilder().validate_args(args)
            
    def test_validate_args_throws_if_number_of_arguments_isnt_one(self):
        test_cases = ([], ['one', 'two'], range(5))
        for args in test_cases:
            with pytest.raises(Exception):
                AppBuilder().validate_args(args)
            
    