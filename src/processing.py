from typing import List, Dict

def filter_by:
    """
    Список словарей с данными о банковских операциях.
        state: Значение ключа 'state', по которому фильтруются словари (по умолчанию 'EXECUTED').

    Returns:
        Новый список словарей, содержащий старых к новым) (по умолчанию True).

    Returns:
        Новый список словарей, отсортированный по дате.
    """
    return sorted(data, key=lambda x: x['date'], reverse=reverse)


if __name__ == '__main__':
    test_data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    executed_transactions = filter_by_state(test_data)
    print("Executed transactions:", executed_transactions)

    canceled_transactions = filter_by_state(test_data, state='CANCELED')
    print("Canceled transactions:", canceled_transactions)

    sorted_transactions_desc = sort_by_date(test_data)
    print("Sorted transactions (descending):", sorted_transactions_desc)

    sorted_transactions_asc = sort_by_date(test_data, reverse=False)
    print("Sorted transactions (ascending):", sorted_transactions_asc)