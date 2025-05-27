from src.masks import get_mask_card_number, get_mask_account

def mask_account_card(account_card_number: str) -> str:
    """
    Маскирует номер банковской карты или счета.

    Args:
        account_card_number: Строка, содержащая тип и номер карты или счета.
                             Например: "Visa Platinum 7000792289606361" или "Счет 73654108430135874305"

    Returns:
        Строка с замаскированным номером карты или счета.
        Пример: "Visa Platinum 7000 79** **** 6361" или "Счет **4305"
    """
    parts = account_card_number.split()
    account_type = parts[0]
    number = parts[1] if len(parts) > 1 else ""  # Обработка случая, когда нет номера после типа
    if "Счет" in account_type:
        masked_number = "" + number[-4:]
        return f"{account_type} {masked_number}"
    else:
        masked_number = f"{number[:4]} {number[4:6]}** **** {number[12:]}"
        return f"{account_type} {masked_number}"

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
