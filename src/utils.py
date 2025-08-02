import json
import logging  # Импортируем модуль logging
import os

# --- Начало настроек логирования для модуля utils ---

# Настраиваем логер для модуля utils
# __name__ гарантирует, что имя логера будет 'utils' (или имя файла без '.py' при прямом запуске)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования не ниже DEBUG

# Создаем папку logs, если ее нет
logs_folder = "logs"
if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)
    logger.debug(f"Создана папка для логов: {logs_folder}")

# Создаем обработчик для записи логов в файл
# 'w' для перезаписи файла при каждом запуске, как указано в задании
log_file_path = os.path.join(logs_folder, 'utils.log')
file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')

# Создаем форматтер
# Формат записи логов включает метку времени, название модуля, уровень серьезности и сообщение
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)  # Устанавливаем форматер для обработчика

# Добавляем обработчик к логеру
logger.addHandler(file_handler)


# --- Конец настроек логирования для модуля utils ---


def read_json_file(file_path):
    """
    Читает JSON-файл и возвращает список словарей с данными.

    Args:
    file_path (str): Путь к JSON-файлу.

    Returns:
    list: Список словарей с данными о финансовых транзакциях.
           Возвращает пустой список, если файл не найден, пустой или содержит не-список.
    """
    # Логирование в начале функции (успешный случай использования)
    logger.debug(f"Вызвана функция read_json_file с file_path: '{file_path}'")

    try:
        if not os.path.exists(file_path):
            logger.error(f"Файл не найден по пути: '{file_path}'")  # Логирование ошибочного случая (ERROR)
            return []

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if isinstance(data, list):
                logger.info(
                    f"Успешно прочитано {len(data)} элементов из файла '{file_path}'.")  # Логирование успешного случая
                return data
            else:
                logger.warning(
                    f"Файл '{file_path}' содержит данные, но они не являются списком. Возвращен пустой список.")
                return []
    except FileNotFoundError:
        # Этот блок уже обработан проверкой os.path.exists, но оставим для надежности
        logger.error(
            f"Исключение FileNotFoundError: Файл не найден по пути: '{file_path}'")
        # Логирование ошибочного случая (ERROR)
        return []
    except json.JSONDecodeError as e:
        logger.error(
            f"Исключение JSONDecodeError: Ошибка декодирования JSON в файле '{file_path}': {e}")
        # Логирование ошибочного случая (ERROR)
        return []
    except Exception as e:
        logger.critical(f"Непредвиденная ошибка при чтении файла '{file_path}': {e}",
                        exc_info=True)  # Логирование ошибочного случая (CRITICAL) с информацией об исключении
        return []


if __name__ == '__main__':
    # Пример использования (замените 'data/operations.json' на реальный путь)
    # Создадим фиктивный файл для теста
    test_data_folder = 'data'
    test_file_path = os.path.join(test_data_folder, 'operations.json')

    if not os.path.exists(test_data_folder):
        os.makedirs(test_data_folder)

    # Тест 1: Успешное чтение
    sample_json_data = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}]
    with open(test_file_path, 'w', encoding='utf-8') as f:
        json.dump(sample_json_data, f, ensure_ascii=False, indent=4)
    print(f"\n--- Тест 1: Успешное чтение файла '{test_file_path}' ---")
    transactions = read_json_file(test_file_path)
    if transactions:
        print(f"Прочитано {len(transactions)} транзакций.")
        print(transactions)
    else:
        print("Не удалось прочитать данные из файла.")

    # Тест 2: Файл не найден
    print("\n--- Тест 2: Файл не найден (non_existent.json) ---")
    transactions = read_json_file(os.path.join(test_data_folder, 'non_existent.json'))
    if transactions:
        print(f"Прочитано {len(transactions)} транзакций.")
    else:
        print("Не удалось прочитать данные из файла.")

    # Тест 3: Некорректный JSON
    print(f"\n--- Тест 3: Некорректный JSON ('{test_file_path}') ---")
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write("{'key': 'value'")  # Некорректный JSON
    transactions = read_json_file(test_file_path)
    if transactions:
        print(f"Прочитано {len(transactions)} транзакций.")
    else:
        print("Не удалось прочитать данные из файла.")

    # Тест 4: JSON не список
    print(f"\n--- Тест 4: JSON не список ('{test_file_path}') ---")
    not_a_list_json = {"transaction": {"id": 1}}
    with open(test_file_path, 'w', encoding='utf-8') as f:
        json.dump(not_a_list_json, f, ensure_ascii=False, indent=4)
    transactions = read_json_file(test_file_path)
    if transactions:
        print(f"Прочитано {len(transactions)} транзакций.")
    else:
        print("Не удалось прочитать данные из файла.")

    # Удалим тестовый файл
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
