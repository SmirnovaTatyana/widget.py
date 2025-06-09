from typing import Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, str]], currency: str) -> List[Dict[str, str]]:
    """
    Фильтрует транзакции по указанной валюте.

    Args:
        transactions (List[Dict]): Список транзакций.
        currency_code (str): Код валюты (например, "USD").

    Yields:
        Dict: Транзакция, соответствующая указанной валюте.
    """
    for transaction in transactions:
        # Проверяем наличие ключей и совпадение валюты
        if (
            isinstance(transaction, dict)
            and "operationAmount" in transaction
            and isinstance(transaction["operationAmount"], dict)
            and "currency" in transaction["operationAmount"]
            and isinstance(transaction["operationAmount"]["currency"], dict)
            and transaction["operationAmount"]["currency"].get("code") == currency
        ):
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """
    Возвращает описание каждой транзакции.

    Args:
        transactions (List[Dict]): Список транзакций.

    Yields:
        str: Описание транзакции.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в диапазоне от start до stop.

    Args:
        start (int): Начальное значение.
        stop (int): Конечное значение.

    Yields:
        str: Номер карты в формате XXXX XXXX XXXX XXXX.
    """
    for number in range(start, stop + 1):
        formatted_number = f"{number:016d}"
        card_number = " ".join([formatted_number[i:i+4] for i in range(0, 16, 4)])
        yield card_number
