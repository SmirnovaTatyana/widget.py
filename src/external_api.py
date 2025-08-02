import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных окружения из .env

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data"

def convert_to_rub(transaction):
    """
    Конвертирует сумму транзакции в рубли, если валюта USD или EUR.Args:
    transaction (dict): Словарь с данными о транзакции.

Returns:
    float: Сумма транзакции в рублях.
"""
amount = transaction.get("operationAmount", {}).get("amount")
currency = transaction.get("operationAmount", {}).get("currency", "RUB")  # Default to RUB

if currency == "RUB":
    return float(amount)

if currency in ("USD", "EUR"):
    try:
        rate = get_exchange_rate(currency)
        return float(amount) * rate
    except Exception as e:
        print(f"Ошибка при конвертации валюты: {e}")
        return None  # Или какое-то другое значение по умолчанию
else:
    return float(amount) #Если валюта не USD и не EUR, возвращаем сумму без изменений.

            def get_exchange_rate(currency):
    """
    Получает текущий курс валюты из API.Args:
    currency (str): Валюта для конвертации (USD или EUR).

Returns:
    float: Курс валюты по отношению к рублю.

Raises:
    Exception: Если произошла ошибка при обращении к API.
"""
url = f"{BASE_URL}/latest?symbols=RUB&amp;base={currency}"
headers = {"apikey": API_KEY}

response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

data = response.json()
return data["rates"]["RUB"]
if __name__ == '__main__':
    # Пример использования
    sample_transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": "USD"
        }
    }
    rub_amount = convert_to_rub(sample_transaction)
    if rub_amount is not None:
        print(f"Сумма в рублях: {rub_amount}")
    else:
        print("Не удалось конвертировать сумму.")

