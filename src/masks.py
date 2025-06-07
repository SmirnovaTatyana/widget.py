# src/masks.py


def get_mask_card_number(card_number: str) -> str:
    """
        Маскирует номер банковской карты.Args:
        card_number: Номер карты в виде строки.

    Returns:
        Маскированный номер карты в формате XXXX XX** **** XXXX.
    """
    card_number = str(card_number)
    if len(card_number) != 16 or not card_number.isdigit():
        return "Некорректный номер карты"
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
        Маскирует номер банковского счета.Args:
        account_number: Номер счета в виде строки.

    Returns:
        Маскированный номер счета в формате **XXXX.
    """
    account_number = str(account_number)
    if not account_number.isdigit() or len(account_number) < 4:
        return "Некорректный номер счета"
    return f"**{account_number[-4:]}"
