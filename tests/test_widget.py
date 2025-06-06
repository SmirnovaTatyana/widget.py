# tests/test_widget.py

import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "account_card_number, expected",
    [
        # Корректные номера карт
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("MasterCard 5555555555554444", "MasterCard 5555 55** **** 4444"),
        ("Maestro 6762971638034782567", "Maestro 6762 97** **** 8256"),  # Номер карты с лишними цифрами

        # Корректные номера счетов
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 00000000000000000000", "Счет **0000"),

        # Граничные случаи
        ("Visa Platinum", "Visa Platinum Некорректный номер карты"),  # Нет номера после типа
        ("Счет", "Счет Некорректный номер счета"),  # Нет номера после типа

        # Некорректные входные данные
        ("InvalidType 1234567890123456", "InvalidType Некорректный номер карты"),  # Неизвестный тип
        ("", " Некорректный номер карты"),  # Пустая строка
        ("Visa Platinum abcdefghijklmn", "Visa Platinum Некорректный номер карты"),  # Нецифровой номер карты
        ("Счет abcdefgh", "Счет Некорректный номер счета"),  # Нецифровой номер счета
        ("Счет 123", "Счет Некорректный номер счета"),  # Слишком короткий номер счета
    ]
)
def test_mask_account_card(account_card_number, expected):
    """Тестирование функции mask_account_card."""
    assert mask_account_card(account_card_number) == expected


@pytest.mark.parametrize(
    "date_string, expected",
    [
        # Корректные даты
        ("2024-03-11T02:26:18.671407", "11.03.2024"),  # Стандартная дата
        ("1999-12-31T23:59:59.999999", "31.12.1999"),  # Последний день года
        ("2000-01-01T00:00:00.000000", "01.01.2000"),  # Первый день года

        # Граничные случаи
        ("2024-03-11T", "11.03.2024"),  # Минимальная строка без времени
        ("2024-03-11", "Invalid date format"),  # Отсутствует 'T'

        # Некорректные даты
        ("2024/03/11T02:26:18.671407", "Invalid date format"),  # Неправильный разделитель
        ("abcd-ef-ghTij:kl:mn.opqrstuv", "Invalid date format"),  # Буквы вместо цифр
        ("", "Invalid date format"),  # Пустая строка
    ]
)
def test_get_date(date_string, expected):
    """Тестирование функции get_date."""
    assert get_date(date_string) == expected