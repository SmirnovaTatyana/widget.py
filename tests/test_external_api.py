import unittest
from unittest.mock import patch, MagicMock
import src.external_api as external_api
import os

class TestExternalApi(unittest.TestCase):@patch('src.external_api.get_exchange_rate')
def test_convert_to_rub_usd(self, mock_get_exchange_rate):
    """Тест конвертации USD в RUB."""
    mock_get_exchange_rate.return_value = 75.0
    transaction = {"operationAmount": {"amount": "100", "currency": "USD"}}
    result = external_api.convert_to_rub(transaction)
    self.assertEqual(result, 7500.0)
    mock_get_exchange_rate.assert_called_once_with("USD")

@patch('src.external_api.get_exchange_rate')
def test_convert_to_rub_eur(self, mock_get_exchange_rate):
    """Тест конвертации EUR в RUB."""
    mock_get_exchange_rate.return_value = 85.0
    transaction = {"operationAmount": {"amount": "50", "currency": "EUR"}}
    result = external_api.convert_to_rub(transaction)
    self.assertEqual(result, 4250.0)
    mock_get_exchange_rate.assert_called_once_with("EUR")

def test_convert_to_rub_rub(self):
    """Тест, когда валюта уже в RUB."""
    transaction = {"operationAmount": {"amount": "200", "currency": "RUB"}}
    result = external_api.convert_to_rub(transaction)
    self.assertEqual(result, 200.0)

def test_convert_to_rub_unknown_currency(self):
    """Тест с неизвестной валютой."""
    transaction = {"operationAmount": {"amount": "300", "currency": "GBP"}}
    result = external_api.convert_to_rub(transaction)
    self.assertEqual(result, 300.0)

@patch('requests.get')
def test_get_exchange_rate_success(self, mock_get):
    """Тест успешного получения курса валюты."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"RUB": 75.0}}
    mock_response.raise_for_status.return_value = None  # Имитируем успешный ответ
    mock_get.return_value = mock_response

    result = external_api.get_exchange_rate("USD")
    self.assertEqual(result, 75.0)
    mock_get.assert_called_once()

@patch('requests.get')
def test_get_exchange_rate_failure(self, mock_get):
    """Тест неудачного получения курса валюты (ошибка API)."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("API Error")
    mock_get.return_value = mock_response

    with self.assertRaises(Exception):
        external_api.get_exchange_rate("USD")
    mock_get.assert_called_once()

def test_convert_to_rub_api_error(self):
   """Тест convert_to_rub при ошибке API."""
   transaction = {"operationAmount": {"amount": "100", "currency": "USD"}}
   with patch('src.external_api.get_exchange_rate', side_effect=Exception("API Error")):
        result = external_api.convert_to_rub(transaction)
        self.assertIsNone(result)

            if __name__ == '__main__':
    unittest.main()
