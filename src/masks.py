import logging
import os

print(f"Текущая рабочая директория: {os.getcwd()}")  # Добавлено для отладки

# --- Настройка логирования для модуля masks.py ---

# Получаем логгер для текущего модуля
logger = logging.getLogger(__name__)  # __name__ будет 'src.masks' если файл лежит там
logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования: DEBUG - самый подробный

# Создаем папку logs, если ее нет
logs_dir = 'logs'
try:
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"Папка '{logs_dir}' успешно создана.")  # Добавлено для отладки
    else:
        print(f"Папка '{logs_dir}' уже существует.")  # Добавлено для отладки
except OSError as e:
    print(f"Ошибка при создании папки '{logs_dir}': {e}")  # Выводим информацию об ошибке

# Получаем абсолютный путь к директории проекта (где находится masks.py)
project_dir = os.path.dirname(os.path.abspath(__file__))
logs_dir = os.path.join(project_dir, 'logs')  # Абсолютный путь к папке logs

# Создаем обработчик для записи логов в файл
# 'w' для перезаписи файла при каждом запуске. Используем 'a' для добавления в конец файла
file_handler = logging.FileHandler(os.path.join(logs_dir, 'masks.log'), mode='a', encoding='utf-8')
# Изменил mode на 'a' (append) чтобы логи не перезаписывались каждый раз при запуске.
# Добавил encoding='utf-8' для корректной записи кириллицы, если таковая будет в логах.

# Создаем форматтер
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Добавляем обработчик к логеру
logger.addHandler(file_handler)

# --- Функции модуля masks.py с добавленным логированием ---


def get_mask_card_number(card_number: str) -> str:
    """
        Маскирует номер банковской карты.
    Args:
        card_number: Номер карты в виде строки.

    Returns:
        Маскированный номер карты в формате XXXX XX** **** XXXX.
    """
    logger.debug(f"Вызвана функция get_mask_card_number с аргументом: {card_number}")

    card_number_str = str(card_number)  # Приводим к строке независимо от типа

    if len(card_number_str) != 16 or not card_number_str.isdigit():
        logger.warning(f"Некорректный номер карты '{card_number_str}'. Возвращаем ошибку.")
        return "Некорректный номер карты"

    masked_card = f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"
    logger.info(f"Номер карты '{card_number_str}' успешно замаскирован как '{masked_card}'.")
    return masked_card


def get_mask_account(account_number: str) -> str:
    """
        Маскирует номер банковского счета.
    Args:
        account_number: Номер счета в виде строки.

    Returns:
        Маскированный номер счета в формате **XXXX.
    """
    logger.debug(f"Вызвана функция get_mask_account с аргументом: {account_number}")

    account_number_str = str(account_number)  # Приводим к строке независимо от типа

    if not account_number_str.isdigit() or len(account_number_str) < 4:
        logger.warning(f"Некорректный номер счета '{account_number_str}'. Возвращаем ошибку.")
        return "Некорректный номер счета"

    masked_account = f"**{account_number_str[-4:]}"
    logger.info(f"Номер счета '{account_number_str}' успешно замаскирован как '{masked_account}'.")
    return masked_account
