import pytest
from src.decorators import log


@pytest.fixture
def capsys_wrapper(capsys):
    """Фикстура для удобного перехвата вывода."""
    def wrapper():
        captured = capsys.readouterr()
        return captured.out
    return wrapper


def test_log_to_console(capsys_wrapper):
    """Тест логирования в консоль."""
    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)
    captured_output = capsys_wrapper()
    assert "add ok" in captured_output
    assert "Inputs: (2, 3)" in captured_output
    assert "Result: 5" in captured_output


def test_log_to_file(tmp_path):
    """Тест логирования в файл."""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def multiply(a, b):
        return a * b

    multiply(4, 5)
    with open(log_file, "r") as f:
        log_content = f.read()

    assert "multiply ok" in log_content
    assert "Inputs: (4, 5)" in log_content
    assert "Result: 20" in log_content


def test_log_error_handling(capsys_wrapper):
    """Тест обработки ошибок."""
    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured_output = capsys_wrapper()
    assert "divide error" in captured_output
    assert "ZeroDivisionError" in captured_output
    assert "Inputs: (10, 0)" in captured_output
