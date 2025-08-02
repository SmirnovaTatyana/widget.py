import json
import os


def read_json_file(file_path):
    """
    Читает JSON-файл и возвращает список словарей с данными.Args:
    file_path (str): Путь к JSON-файлу.

    Returns:
    list: Список словарей с данными о финансовых транзакциях.
           Возвращает пустой список, если файл не найден, пустой или содержит не-список.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


if __name__ == '__main__':
    # Пример использования (замените 'data/operations.json' на реальный путь)
    file_path = os.path.join('data', 'operations.json')
    transactions = read_json_file(file_path)
    if transactions:
        print(f"Прочитано {len(transactions)} транзакций.")
    else:
        print("Не удалось прочитать данные из файла.")
