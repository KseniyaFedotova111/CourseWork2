import pytest
from src.vacancy import Vacancy


def test_vacancy_init():
    """Тестирует инициализацию вакансии."""
    vacancy = Vacancy(
        title="Python Developer",
        company="Tech Corp",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
        url="http://example.com"
    )
    assert vacancy.title == "Python Developer"
    assert vacancy.salary_from == 100000.0
    assert vacancy.currency == "RUR"


def test_vacancy_init_empty():
    """Тестирует инициализацию с пустыми данными."""
    vacancy = Vacancy("", "", None, None, "", "")
    assert vacancy.title == "Без названия"
    assert vacancy.company == "Неизвестный работодатель"
    assert vacancy.salary_from == 0.0
    assert vacancy.salary_to == 0.0
    assert vacancy.currency == "Не указано"
    assert vacancy.url == "Ссылка недоступна"


def test_vacancy_init_invalid_salary():
    """Тестирует инициализацию с некорректной зарплатой."""
    vacancy = Vacancy(
        title="Java Developer",
        company="Soft Inc",
        salary_from="invalid",
        salary_to=-100,
        currency="RUR",
        url="http://example.com"
    )
    assert vacancy.salary_from == 0.0
    assert vacancy.salary_to == 0.0


def test_vacancy_from_dict():
    """Тестирует создание вакансии из словаря."""
    data = {
        "title": "Java Developer",
        "company": "Soft Inc",
        "salary_from": 200000,
        "salary_to": 250000,
        "currency": "RUR",
        "url": "http://example.com"
    }
    vacancy = Vacancy.from_dict(data)
    assert vacancy.title == "Java Developer"
    assert vacancy.salary_to == 250000.0


def test_vacancy_to_dict():
    """Тестирует преобразование вакансии в словарь."""
    vacancy = Vacancy(
        title="Manager",
        company="Biz Ltd",
        salary_from=0,
        salary_to=0,
        currency="Не указано",
        url=""
    )
    data = vacancy.to_dict()
    assert data["title"] == "Manager"
    assert data["currency"] == "Не указано"


def test_vacancy_get_salary():
    """Тестирует метод get_salary."""
    vacancy = Vacancy(
        title="Python Developer",
        company="Tech Corp",
        salary_from=100000,
        salary_to=0,
        currency="RUR",
        url="http://example.com"
    )
    assert vacancy.get_salary() == 100000.0
    vacancy2 = Vacancy(
        title="Java Developer",
        company="Soft Inc",
        salary_from=0,
        salary_to=200000,
        currency="RUR",
        url="http://example.com"
    )
    assert vacancy2.get_salary() == 200000.0


def test_vacancy_slots():
    """Тестирует использование __slots__."""
    vacancy = Vacancy("Test", "Test Inc", 1000, 2000, "RUR", "http://test.com")
    with pytest.raises(AttributeError, match=".*new_attr.*"):
        vacancy.new_attr = 123  # Должна быть ошибка, так как __slots__
    assert hasattr(vacancy, "title")  # Проверяем, что атрибут из __slots__ существует
    assert not hasattr(vacancy, "new_attr")  # Проверяем, что новый атрибут не создан


def test_vacancy_comparison():
    """Тестирует сравнение вакансий по зарплате."""
    vacancy1 = Vacancy("Test1", "Test Inc", 100000, 150000, "RUR", "http://test.com")
    vacancy2 = Vacancy("Test2", "Test Inc", 200000, 250000, "RUR", "http://test.com")
    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy1
