import os
import unittest
from unittest.mock import MagicMock, patch

import requests

import src.external_api  # Убедитесь, что это правильный путь к вашему файлу


class TestExternalApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Сохраняем исходное значение EXCHANGE_RATES_API_KEY, если оно есть
        cls.original_api_key_env = os.getenv("EXCHANGE_RATES_API_KEY")
        # Устанавливаем фиктивное значение для большинства тестов
        os.environ["EXCHANGE_RATES_API_KEY"] = "fake_api_key"

    @classmethod
    def tearDownClass(cls):
        # Восстанавливаем исходное значение или удаляем, если не было
        if cls.original_api_key_env is not None:
            os.environ["EXCHANGE_RATES_API_KEY"] = cls.original_api_key_env
        else:
            if "EXCHANGE_RATES_API_KEY" in os.environ:
                del os.environ["EXCHANGE_RATES_API_KEY"]
        # После изменения переменных окружения, нужно "перезагрузить" модуль для тестов
        # Но для этого теста это не нужно, так как мы патчим само значение API_KEY

    def setUp(self):
        # Патчим os.getenv для предотвращения взаимодействия с реальными переменными окружения
        # Это будет активно во всех тестах, кроме test_get_exchange_rate_no_api_key,
        # где мы специально переопределяем патч.
        # Для удобства, пусть по умолчанию getenv возвращает наше фиктивное значение.
        self.patcher_getenv = patch('os.getenv', return_value="fake_api_key")
        self.mock_getenv = self.patcher_getenv.start()

        # Патчим API_KEY в самом модуле src.external_api
        # Это важно, так как API_KEY в модуле инициализируется при импорте.
        # Мы хотим, чтобы для большинства тестов оно было fake_api_key.
        self.patcher_api_key = patch('src.external_api.API_KEY', "fake_api_key")
        self.patcher_api_key.start()

    def tearDown(self):
        self.patcher_getenv.stop()
        self.patcher_api_key.stop()  # Обязательно останавливаем патч для API_KEY

    @patch('requests.get')
    def test_get_exchange_rate_success(self, mock_requests_get):
        """Тест успешного получения курса валют."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 75.5}}
        mock_requests_get.return_value = mock_response

        rate = src.external_api.get_exchange_rate("USD")
        self.assertEqual(rate, 75.5)
        expected_url = "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD"
        mock_requests_get.assert_called_once_with(expected_url, headers={"apikey": "fake_api_key"})
        # self.mock_getenv.assert_called_once_with("EXCHANGE_RATES_API_KEY") # Не нужно, так как API_KEY уже установлен

    @patch('requests.get', side_effect=requests.exceptions.RequestException("API connection error"))
    def test_get_exchange_rate_request_failure(self, mock_requests_get):
        """Тест обработки сбоя сетевого запроса."""
        with self.assertRaisesRegex(requests.exceptions.RequestException, "API request failed: API connection error"):
            src.external_api.get_exchange_rate("EUR")
        expected_url = "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=EUR"
        mock_requests_get.assert_called_once_with(expected_url, headers={"apikey": "fake_api_key"})

    @patch('requests.get')
    def test_get_exchange_rate_http_error(self, mock_requests_get):
        """Тест обработки HTTP ошибок (4xx, 5xx)."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Forbidden", response=mock_response)
        mock_requests_get.return_value = mock_response

        with self.assertRaisesRegex(requests.exceptions.RequestException, "API request failed: Forbidden"):
            src.external_api.get_exchange_rate("GBP")
        expected_url = "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=GBP"
        mock_requests_get.assert_called_once_with(expected_url, headers={"apikey": "fake_api_key"})

    @patch('requests.get')
    def test_get_exchange_rate_invalid_json(self, mock_requests_get):
        """Тест обработки некорректного JSON ответа."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON response")  # Имитируем ошибку парсинга JSON
        mock_requests_get.return_value = mock_response

        with self.assertRaisesRegex(Exception,
                                    "An unexpected error occurred in get_exchange_rate: .*Invalid JSON response"):
            src.external_api.get_exchange_rate("USD")
        expected_url = "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD"
        mock_requests_get.assert_called_once_with(expected_url, headers={"apikey": "fake_api_key"})

    @patch('requests.get')
    def test_get_exchange_rate_missing_key_in_response(self, mock_requests_get):
        """Тест обработки отсутствия нужных данных в ответе API."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"msg": "Success", "data": {}}
        mock_requests_get.return_value = mock_response

        with self.assertRaisesRegex(KeyError, "Missing key in API response: 'rates'"):
            src.external_api.get_exchange_rate("USD")
        expected_url = "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD"
        mock_requests_get.assert_called_once_with(expected_url, headers={"apikey": "fake_api_key"})

    def test_get_exchange_rate_no_api_key(self):
        """Тест на отсутствие API_KEY в переменных окружения."""
        # Для этого конкретного теста устанавливаем API_KEY в None
        # Важно: Останавливаем предыдущий патч, чтобы применился новый
        self.patcher_api_key.stop()
        self.patcher_api_key = patch('src.external_api.API_KEY', None)
        self.patcher_api_key.start()
        # Также убеждаемся, что os.getenv для этого теста возвращает None,
        # хотя в данном сценарии это не вызовет os.getenv из get_exchange_rate
        self.patcher_getenv.stop()  # Остановка общего патча getenv
        self.patcher_getenv = patch('os.getenv', return_value=None)
        self.patcher_getenv.start()

        with self.assertRaisesRegex(ValueError, "API_KEY not found in environment variables."):
            src.external_api.get_exchange_rate("USD")
        # Здесь не должно быть assert_called_once_with для self.mock_getenv,
        # потому что get_exchange_rate не вызывает os.getenv в этом сценарии.
        # os.getenv вызывается при импорте модуля, который мы уже спатчили.
        # Достаточно убедиться, что ValueError выброшена.

    @patch('src.external_api.get_exchange_rate')
    def test_convert_to_rub_usd_success(self, mock_get_exchange_rate):
        """Тест успешной конвертации USD в RUB."""
        mock_get_exchange_rate.return_value = 75.0
        transaction = {"operationAmount": {"amount": "100", "currency": "USD"}}
        result = src.external_api.convert_to_rub(transaction)
        self.assertEqual(result, 100 * 75.0)
        mock_get_exchange_rate.assert_called_once_with("USD")

    @patch('src.external_api.get_exchange_rate')
    def test_convert_to_rub_eur_success(self, mock_get_exchange_rate):
        """Тест успешной конвертации EUR в RUB."""
        mock_get_exchange_rate.return_value = 85.0
        transaction = {"operationAmount": {"amount": "50", "currency": "EUR"}}
        result = src.external_api.convert_to_rub(transaction)
        self.assertEqual(result, 50 * 85.0)
        mock_get_exchange_rate.assert_called_once_with("EUR")

    @patch('src.external_api.get_exchange_rate')
    def test_convert_to_rub_rub_currency(self, mock_get_exchange_rate):
        """Тест для валюты RUB (конвертация не нужна)."""
        transaction = {"operationAmount": {"amount": "200", "currency": "RUB"}}
        result = src.external_api.convert_to_rub(transaction)
        self.assertEqual(result, 200.0)
        mock_get_exchange_rate.assert_not_called()

    @patch('src.external_api.get_exchange_rate')
    def test_convert_to_rub_other_currency(self, mock_get_exchange_rate):
        """Тест для другой валюты (KZT, GBP), конвертация не нужна."""
        transaction = {"operationAmount": {"amount": "5000", "currency": "KZT"}}
        result = src.external_api.convert_to_rub(transaction)
        self.assertEqual(result, 5000.0)
        mock_get_exchange_rate.assert_not_called()

    @patch('src.external_api.get_exchange_rate', side_effect=requests.exceptions.RequestException("API Error"))
    def test_convert_to_rub_api_error_handling(self, mock_get_exchange_rate):
        """Тест обработки ошибки API при конвертации."""
        transaction = {"operationAmount": {"amount": "100", "currency": "USD"}}
        result = src.external_api.convert_to_rub(transaction)
        self.assertIsNone(result)
        mock_get_exchange_rate.assert_called_once_with("USD")

    @patch('src.external_api.get_exchange_rate', side_effect=KeyError("rates"))
    def test_convert_to_rub_key_error_handling(self, mock_get_exchange_rate):
        """Тест обработки Missing KeyError при конвертации."""
        transaction = {"operationAmount": {"amount": "100", "currency": "USD"}}
        result = src.external_api.convert_to_rub(transaction)
        self.assertIsNone(result)
        mock_get_exchange_rate.assert_called_once_with("USD")

    @patch('src.external_api.get_exchange_rate', side_effect=ValueError("Test Error"))
    def test_convert_to_rub_value_error_from_api(self, mock_get_exchange_rate):
        """Тест обработки ValueError, возникающего в get_exchange_rate."""
        transaction = {"operationAmount": {"amount": "100", "currency": "USD"}}
        result = src.external_api.convert_to_rub(transaction)
        self.assertIsNone(result)
        mock_get_exchange_rate.assert_called_once_with("USD")

    @patch('src.external_api.get_exchange_rate')
    def test_convert_to_rub_missing_amount(self, mock_get_exchange_rate):
        """Тест транзакции без поля 'amount'."""
        transaction = {"operationAmount": {"currency": "USD"}}
        result = src.external_api.convert_to_rub(transaction)
        self.assertIsNone(result)
        mock_get_exchange_rate.assert_not_called()

    @patch('src.external_api.get_exchange_rate')
    def test_convert_to_rub_invalid_amount_type(self, mock_get_exchange_rate):
        """Тест транзакции с невалидным типом 'amount' (не число)."""
        transaction = {"operationAmount": {"amount": "abc", "currency": "USD"}}
        result = src.external_api.convert_to_rub(transaction)
        self.assertIsNone(result)
        mock_get_exchange_rate.assert_not_called()

    @patch('src.external_api.get_exchange_rate')
    def test_convert_to_rub_missing_operation_amount(self, mock_get_exchange_rate):
        """Тест транзакции без поля 'operationAmount'."""
        transaction = {"id": 1, "description": "Test"}
        result = src.external_api.convert_to_rub(transaction)
        self.assertIsNone(result)
        mock_get_exchange_rate.assert_not_called()

    @patch('src.external_api.get_exchange_rate')
    def test_convert_to_rub_zero_amount(self, mock_get_exchange_rate):
        """Тест суммы 0."""
        transaction = {"operationAmount": {"amount": "0", "currency": "USD"}}
        mock_get_exchange_rate.return_value = 70.0
        result = src.external_api.convert_to_rub(transaction)
        self.assertEqual(result, 0.0)
        mock_get_exchange_rate.assert_called_once_with("USD")

    @patch('src.external_api.get_exchange_rate')
    def test_convert_to_rub_negative_amount(self, mock_get_exchange_rate):
        """Тест отрицательной суммы."""
        transaction = {"operationAmount": {"amount": "-50", "currency": "USD"}}
        mock_get_exchange_rate.return_value = 70.0
        result = src.external_api.convert_to_rub(transaction)
        self.assertEqual(result, -3500.0)
        mock_get_exchange_rate.assert_called_once_with("USD")


if __name__ == '__main__':
    unittest.main()
