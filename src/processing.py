from typing import List, Dict, Any


def filter_by(data: List[Dict[str, Any]], state: str) -> List[Dict[str, Any]]:
    """
    Фильтрует данные по заданному состоянию.

    :param data: Список словарей или объектов для фильтрации.
    :param state: Состояние, по которому фильтруются данные.
    :return: Отфильтрованный список.
    """
    # Пример реализации фильтрации
    return [item for item in data if item.get("state") == state]


def sort_by(data: List[Dict [str, Any]], date_field: str) -> List[Dict[str, Any]]:
    """
    Сортирует данные по полю даты.

    :paramоварей или объектов для сортировки.
    :param date_field: Поле, содержащее дату.
    :return: Отсортированный список.
    """
    # Пример реализации сортировки
    return sorted(data, key=lambda item: item.get(date_field))
