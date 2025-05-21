from typing import List, Optional


def validate_currency(currency: str, valid_currencies: List[str] = None) -> str:
    """валидирует валюту, возвращает rur, если валюта некорректная"""
    if valid_currencies is None:
        valid_currencies = ["RUR", "KZT", "UZS", "USD"]
    return currency if currency in valid_currencies else "RUR"


def format_salary(salary_from: float, salary_to: float, currency: str) -> str:
    """форматирует зарплату для вывода"""
    if salary_from == 0 and salary_to == 0:
        return "Зарплата не указана"
    return f"от {salary_from:.0f} до {salary_to:.0f} {currency}"


def validate_url(url: str) -> str:
    """проверяет и возвращает корректный url"""
    if not url or not url.startswith("http"):
        return "Ссылка недоступна"
    return url


def clean_string(text: Optional[str]) -> str:
    """очищает строку от лишних пробелов и символов"""
    return text.strip() if text else ""
