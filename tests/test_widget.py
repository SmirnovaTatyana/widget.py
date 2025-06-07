# tests/test_widget.py
import pytest
from src.widget import mask_account_card, get_date

# Фикстуры для тестовых данных
@pytest.fixture
def valid_card_string():
    return "Visa Platinum 7000792289606361"

@pytest.fixture
def valid_account_string():
    return "Счет 73654108430135874305"

@pytest.fixture
def invalid_format_string():
    return "InvalidStringWithoutSpace"

@pytest.fixture
def valid_date_string():
    return "2024-03-11T02:26:18.671407"

@pytest.fixture
def invalid_date_string():
    return "InvalidDateFormat"

# Тесты для mask_account_card
def test_mask_account_card_valid_card(valid_card_string):
    """Тестирование корректной строки с номером карты."""
    masked = mask_account_card(valid_card_string)
    assert masked == "Visa Platinum 7000 79** **** 6361"

def test_mask_account_card_valid_account(valid_account_string):
    """Тестирование корректной строки с номером счета."""
    masked = mask_account_card(valid_account_string)
    assert masked == "Счет **874305"

def test_mask_account_card_invalid_format(invalid_format_string):
    """Тестирование строки с некорректным форматом."""
    masked = mask_account_card(invalid_format_string)
    assert masked == "Некорректный формат входных данных"

def test_mask_account_card_non_string_input():
    """Тестирование входных данных не строкового типа."""
    masked = mask_account_card(12345)
    assert masked == "Некорректный формат входных данных"

# Тесты для get_date
def test_get_date_valid_input(valid_date_string):
    """Тестирование корректного формата даты."""
    formatted_date = get_date(valid_date_string)
    assert formatted_date == "11.03.2024"

def test_get_date_invalid_input(invalid_date_string):
    """Тестирование некорректного формата даты."""
    formatted_date = get_date(invalid_date_string)
    assert formatted_date == "Некорректный формат даты"
