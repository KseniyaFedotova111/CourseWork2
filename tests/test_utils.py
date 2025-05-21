from src.utils import validate_currency, format_salary, validate_url, clean_string


def test_validate_currency():
    """тестирует валидацию валюты"""
    assert validate_currency("RUR") == "RUR"
    assert validate_currency("USD") == "USD"
    assert validate_currency("INVALID") == "RUR"
    assert validate_currency("KZT", ["KZT", "USD"]) == "KZT"
    assert validate_currency("RUR", ["KZT", "USD"]) == "RUR"


def test_format_salary():
    """тестирует форматирование зарплаты"""
    assert format_salary(100000, 150000, "RUR") == "от 100000 до 150000 RUR"
    assert format_salary(0, 0, "RUR") == "Зарплата не указана"


def test_validate_url():
    """тестирует валидацию url"""
    assert validate_url("http://example.com") == "http://example.com"
    assert validate_url("") == "Ссылка недоступна"
    assert validate_url("invalid") == "Ссылка недоступна"


def test_clean_string():
    """тестирует очистку строк"""
    assert clean_string("  Python Developer  ") == "Python Developer"
    assert clean_string("") == ""
    assert clean_string(None) == ""
