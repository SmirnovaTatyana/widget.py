import functools
from datetime import datetime
from typing import Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функций.

    :param filename: Имя файла для записи логов. Если не указано, логи выводятся в консоль.
    :return: Декорированный объект функции.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                start_time = datetime.now()
                result = func(*args, **kwargs)
                end_time = datetime.now()

                # Лог успешного выполнения
                log_message = (
                    f"{func.__name__} ok. "
                    f"Inputs: {args}, {kwargs}. "
                    f"Result: {result}. "
                    f"Execution time: {end_time - start_time}\n"
                )
            except Exception as e:
                # Лог ошибки
                log_message = (
                    f"{func.__name__} error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}. "
                    f"Error message: {str(e)}\n"
                )
                if not filename:
                    print(log_message)  # Выводим в консоль, если файл не задан
                else:
                    with open(filename, "a") as f:
                        f.write(log_message)
                raise  # Повторно выбрасываем исключение

            # Запись успешного выполнения в файл или вывод в консоль
            if filename:
                with open(filename, "a") as f:
                    f.write(log_message)
            else:
                print(log_message)

            return result

        return wrapper

    return decorator
