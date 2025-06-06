import re
from typing import Union
from .masks import get_mask_card_number, get_mask_account


def mask_account_card(account_card_number):
    """Маскирует номер карты или счета, оставляя видимыми только первые и последние несколько цифр.

    Args:
        account_card_number (str): Номер карты или счета.

    Returns:
        str: Маскированный номер карты или счета.
             Если входные данные некорректны, возвращает сообщение об ошибке.
    """
    parts = account_card_number.split()
    if not parts:
        return " Некорректный номер карты"

    account_type = parts[0]
    if len(parts) > 1:
        number = parts[-1]
    else:
        number = ""

    if account_type in ["Visa Platinum", "MasterCard", "Maestro"]:
        if not number.isdigit() or len(number) < 13:
            return f"{account_type} Некорректный номер карты"
        number = ''.join(filter(str.isdigit, number))  # Убираем все нецифровые символы
        masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
        return f"{account_type} {masked_number}"

    elif account_type == "Счет":
        if not number.isdigit() or len(number) < 5:
            return f"{account_type} Некорректный номер счета"
        return f"{account_type} **{number[-4:]}"

    else:
        return f"{account_type} Некорректный номер карты"


def get_date(date_string: str) -> str:
    """
    Преобразует строку с датой из формата "ГГГГ-ММ-ДДTЧЧ:ММ:СС.мс" в формат "ДД.ММ.ГГГГ".

    Args:
        date_string: Строка с датой в формате "2024-03-11T02:26:18.671407"

    Returns:
        Строка с датой в формате "ДД.ММ.ГГГГ" (например, "11.03.2024")
    """
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})T", date_string)
    if match:
        year, month, day = match.groups()
        return f"{day}.{month}.{year}"
    else:
        return "Invalid date format"  # Или выбросить исключение, если это более уместно