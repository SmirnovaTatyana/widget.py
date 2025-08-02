import unittest
import json
import os
from unittest.mock import patch, mock_open

# Импортируем функцию, которую будем тестировать
from src.utils import read_json_file


class TestReadJsonFile(unittest.TestCase):

    def setUp(self):
        """
        Метод вызывается перед каждым тестом.
        Здесь мы создадим временную директорию 'data' для тестов.
        """
        self.data_dir = 'test_data'
        os.makedirs(self.data_dir, exist_ok=True)
        self.test_file_path = os.path.join(self.data_dir, 'test_operations.json')

    def tearDown(self):
        """
        Метод вызывается после каждого теста.
        Здесь мы удалим временную директорию 'data' и её содержимое.
        """
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        if os.path.exists(self.data_dir):
            os.rmdir(self.data_dir)

    def _create_test_file(self, content):
        """Вспомогательная функция для создания тестового файла с заданным содержимым."""
        with open(self.test_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def test_read_valid_json_file(self):
        """Тест на успешное чтение корректного JSON-файла."""
        mock_data = [
            {"id": 1, "description": "Payment", "amount": 100},
            {"id": 2, "description": "Purchase", "amount": 50}
        ]
        self._create_test_file(json.dumps(mock_data))
        result = read_json_file(self.test_file_path)
        self.assertEqual(result, mock_data)

    def test_read_empty_json_file(self):
        """Тест на чтение пустого JSON-файла (должен вернуть [])."""
        self._create_test_file("")  # Пустой файл
        result = read_json_file(self.test_file_path)
        self.assertEqual(result, [])

    def test_read_invalid_json_format(self):
        """Тест на чтение файла с некорректным JSON-форматом."""
        self._create_test_file("this is not json")
        result = read_json_file(self.test_file_path)
        self.assertEqual(result, [])

    def test_read_json_not_a_list(self):
        """Тест на чтение JSON-файла, где корневой элемент не является списком."""
        self._create_test_file(json.dumps({"id": 1, "data": "value"}))  # Объект вместо списка
        result = read_json_file(self.test_file_path)
        self.assertEqual(result, [])

    def test_read_non_existent_file(self):
        """Тест на попытку чтения несуществующего файла."""
        # Файл не будет создан, так что функция должна поймать FileNotFoundError
        result = read_json_file("non_existent_file.json")
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=Exception("Simulated unexpected error"))
    def test_read_unexpected_exception(self, mock_json_load, mock_file_open):
        """Тест на обработку неожиданных исключений при чтении файла."""
        # Для этого теста мы просто передаем фиктивный путь, потому что open будет замокан
        result = read_json_file(self.test_file_path)
        self.assertEqual(result, [])
        # Проверяем, что print(f"An unexpected error occurred: {e}") был вызван
        # Это сложнее, т.к. print идет в stdout. Но для этого примера проверка на [] достаточно.
