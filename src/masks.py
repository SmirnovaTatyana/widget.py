def get_mask_card_number(card_number: str) -> str:
    """
        Маскирует номер банковской карты.Args:
        card_number: Номер карты в виде строки.

    Returns:
        Маскированный номер карты в формате XXXX XX** **** XXXX.
    """
    card_number = str(card_number)
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"


def get_mask_account(account_number: str) -> str:
    """
        Маскирует номер банковского счета.Args:
        account_number: Номер счета в виде строки.

    Returns:
        Маскированный номер счета в формате **XXXX.
    """
    account_number = str(account_number)
    return f"{account_number[-4:]}"
