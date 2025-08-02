import unittest
from unittest.mock import patch
import src.utils as utils
import os

class TestUtils(unittest.TestCase):@patch('src.utils.json.load')
@patch('builtins.open', create=True)
def test_read_json_file_success(self, mock_open, mock_json_load):
    """Тест успешного чтения JSON-файла."""
    mock_json_load.return_value = [{"id": 1, "amount": 100}]
    mock_open.return_value.__enter__.return_value.read.return_value = '[{"id": 1, "amount": 100}]'
    file_path = "fake_path.json"
    result = utils.read_json_file(file_path)
    self.assertEqual(result, [{"id": 1, "amount": 100}])
    mock_open.assert_called_once_with(file_path, 'r', encoding='utf-8')
    mock_json_load.assert_called_once()

@patch('src.utils.json.load')
@patch('builtins.open', create=True)
def test_read_json_file_empty(self, mock_open, mock_json_load):
    """Тест чтения пустого JSON-файла."""
    mock_json_load.return_value = []
    mock_open.return_value.__enter__.return_value.read.return_value = '[]'
    file_path = "fake_path.json"
    result = utils.read_json_file(file_path)
    self.assertEqual(result, [])

@patch('src.utils.json.load')
@patch('builtins.open', create=True)
def test_read_json_file_not_a_list(self, mock_open, mock_json_load):
    """Тест, когда JSON-файл содержит не список."""
    mock_json_load.return_value = {"key": "value"}
    mock_open.return_value.__enter__.return_value.read.return_value = '{"key": "value"}'
    file_path = "fake_path.json"
    result = utils.read_json_file(file_path)
    self.assertEqual(result, [])

@patch('builtins.open', side_effect=FileNotFoundError)
def test_read_json_file_not_found(self, mock_open):
    """Тест, когда файл не найден."""
    file_path = "non_existent_file.json"
    result = utils.read_json_file(file_path)
    self.assertEqual(result, [])

@patch('src.utils.json.load', side_effect=ValueError)
@patch('builtins.open', create=True)
def test_read_json_file_invalid_json(self, mock_open, mock_json_load):
    """Тест, когда JSON-файл содержит невалидный JSON."""
    mock_open.return_value.__enter__.return_value.read.return_value = 'invalid json'
    file_path = "fake_path.json"
    result = utils.read_json_file(file_path)
    self.assertEqual(result, [])

            if __name__ == '__main__':
    unittest.main()
