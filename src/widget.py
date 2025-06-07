# src/widget.py
from .masks import get_mask_card_number, get_mask_account  # Импортируем функции маскировки


def mask_account_card(account_string: str) -> str:
    """
    Маскирует номер карты или счета в строке.

    Args:
        account_string (str): Строка, содержащая тип и номер карты или счета.
                              Пример: "Visa Platinum 7000792289606361" или "Счет 73654108430135874305".

    Returns:
        str: Строка с замаскированным номером карты или счета.
    """
    # Проверяем, что входные данные являются строкой
    if not isinstance(account_string, str):
        return "Некорректный формат входных данных"

    # Разделяем строку на название и номер
    parts = account_string.rsplit(" ", 1)  # Разделяем по последнему пробелу
    if len(parts) != 2:
        return "Некорректный формат входных данных"

    name, number = parts[0], parts[1]

    # Определяем, является ли строка информацией о счете
    if name == "Счет":
        masked_number = get_mask_account(number)  # Используем функцию маскировки счета
    else:
        masked_number = get_mask_card_number(number)  # Используем функцию маскировки карты

    # Возвращаем результат в виде строки
    return f"{name} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата "2024-03-11T02:26:18.671407" в формат "ДД.ММ.ГГГГ".

    Args:
        date_string (str): Строка с датой в формате "2024-03-11T02:26:18.671407".

    Returns:
        str: Строка с датой в формате "ДД.ММ.ГГГГ".
    """
    try:
        # Извлекаем дату до символа 'T'
        date_part = date_string.split("T")[0]
        year, month, day = date_part.split("-")
        return f"{day}.{month}.{year}"
    except Exception:
        return "Некорректный формат даты"