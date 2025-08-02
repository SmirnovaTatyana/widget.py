import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных окружения из .env

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data"


def get_exchange_rate(currency: str) -> float:
    """
    Получает текущий курс валюты из API.
    Args:
    currency (str): Валюта для конвертации (USD или EUR).

    Returns:
    float: Курс валюты по отношению к рублю.

    Raises:
    requests.exceptions.RequestException: Если произошла ошибка при обращении к API.
    KeyError: Если в ответе API нет нужных данных.
    """
    if not API_KEY:
        raise ValueError("API_KEY not found in environment variables.")

    url = f"{BASE_URL}/latest?symbols=RUB&base={currency}"  # Исправлено: & на &
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Вызовет HTTPError для 4xx/5xx ответов
        data = response.json()
        return data["rates"]["RUB"]
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API request failed: {e}")
    except KeyError as e:
        raise KeyError(f"Missing key in API response: {e}")
    except Exception as e:
        # Для других неожиданных ошибок
        raise Exception(f"An unexpected error occurred in get_exchange_rate: {e}")


def convert_to_rub(transaction: dict) -> [float, None]:
    """
    Конвертирует сумму транзакции в рубли, если валюта USD или EUR.
    Args:
    transaction (dict): Словарь с данными о транзакции.

    Returns:
    float: Сумма транзакции в рублях.
    None: Если произошла ошибка конвертации.
    """
    amount_str = transaction.get("operationAmount", {}).get("amount")
    currency = transaction.get("operationAmount", {}).get("currency", "RUB")  # Default to RUB

    if amount_str is None:
        print("Warning: 'amount' not found in transaction. Returning None.")
        return None

    try:
        amount = float(amount_str)
    except ValueError:
        print(f"Warning: Could not convert amount '{amount_str}' to float. Returning None.")
        return None

    if currency == "RUB":
        return amount

    if currency in ("USD", "EUR"):
        try:
            rate = get_exchange_rate(currency)
            return amount * rate
        except (requests.exceptions.RequestException, KeyError, ValueError, Exception) as e:
            # Логгируем ошибку, но не поднимаем её, так как функция должна вернуть None
            print(f"Ошибка при конвертации валюты: {e}")
            return None
    else:
        # Если валюта не USD, EUR и не RUB (например, KZT, GBP и т.д.), возвращаем сумму без изменений.
        return amount


if __name__ == '__main__':
    # Пример использования
    sample_transaction_usd = {
        "operationAmount": {
            "amount": "100",
            "currency": "USD"
        }
    }
    sample_transaction_rub = {
        "operationAmount": {
            "amount": "100",
            "currency": "RUB"
        }
    }
    sample_transaction_kzt = {
        "operationAmount": {
            "amount": "5000",
            "currency": "KZT"
        }
    }
    # Добавьте свой .env файл с EXCHANGE_RATES_API_KEY
    # EXCHANGE_RATES_API_KEY=YOUR_API_KEY_HERE

    print(f"Конвертация USD: {convert_to_rub(sample_transaction_usd)}")
    print(f"Конвертация RUB: {convert_to_rub(sample_transaction_rub)}")
    print(f"Конвертация KZT: {convert_to_rub(sample_transaction_kzt)}")

    # Пример с отсутствующим ключом
    sample_transaction_no_amount = {
        "operationAmount": {
            "currency": "USD"
        }
    }
    print(f"Конвертация без указания 'amount': {convert_to_rub(sample_transaction_no_amount)}")

    sample_transaction_invalid_amount = {
        "operationAmount": {
            "amount": "abc",
            "currency": "USD"
        }
    }
    print(f"Конвертация с невалидным 'amount': {convert_to_rub(sample_transaction_invalid_amount)}")

    # Тестирование API_KEY - раскомментировать, если хотите проверить отсутствие ключа
    # del os.environ["EXCHANGE_RATES_API_KEY"]
    # try:
    #     get_exchange_rate("USD")
    # except ValueError as e:
    #     print(f"Test API_KEY missing: {e}")
