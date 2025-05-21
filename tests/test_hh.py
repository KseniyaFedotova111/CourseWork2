import pytest
import json
from src.vacancy import Vacancy
from data.hh import load_vacancies, filter_vacancies_by_salary, filter_vacancies_by_keywords, sort_vacancies, \
    get_top_vacancies, main


@pytest.fixture
def temp_vacancies_file(tmp_path):
    """создаёт временный json-файл с тестовыми вакансиями"""
    filename = tmp_path / "test_vacancies.json"
    vacancies = [
        {
            "title": "Python Developer",
            "company": "Tech Corp",
            "salary_from": 100000,
            "salary_to": 150000,
            "currency": "RUR",
            "url": "http://example.com/1"
        },
        {
            "title": "Java Developer",
            "company": "Soft Inc",
            "salary_from": 200000,
            "salary_to": 250000,
            "currency": "RUR",
            "url": "http://example.com/2"
        },
        {
            "title": "Manager",
            "company": "Biz Ltd",
            "salary_from": 0,
            "salary_to": 0,
            "currency": "Не указано",
            "url": "http://example.com/3"
        }
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=2)  # type: ignore
    return str(filename)


def test_load_vacancies(temp_vacancies_file):
    """тестирует загрузку вакансий из json-файла"""
    vacancies = load_vacancies(temp_vacancies_file)
    assert len(vacancies) == 3
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Developer"


def test_load_vacancies_file_not_found():
    """тестирует загрузку вакансий при отсутствии файла"""
    vacancies = load_vacancies("nonexistent.json")
    assert vacancies == []


def test_filter_vacancies_by_salary(temp_vacancies_file):
    """тестирует фильтрацию вакансий по минимальной зарплате"""
    vacancies = load_vacancies(temp_vacancies_file)
    filtered = filter_vacancies_by_salary(vacancies, min_salary=150000, currency="RUR")
    assert len(filtered) == 1
    assert filtered[0].title == "Java Developer"


def test_filter_vacancies_by_keywords(temp_vacancies_file):
    """тестирует фильтрацию вакансий по ключевым словам"""
    vacancies = load_vacancies(temp_vacancies_file)
    filtered = filter_vacancies_by_keywords(vacancies, ["Python"])
    assert len(filtered) == 1
    assert filtered[0].title == "Python Developer"


def test_sort_vacancies(temp_vacancies_file):
    """тестирует сортировку вакансий по зарплате"""
    vacancies = load_vacancies(temp_vacancies_file)
    sorted_vac = sort_vacancies(vacancies)
    assert sorted_vac[0].title == "Java Developer"
    assert sorted_vac[1].title == "Python Developer"
    assert sorted_vac[2].title == "Manager"


def test_get_top_vacancies(temp_vacancies_file):
    """тестирует получение топ-n вакансий"""
    vacancies = load_vacancies(temp_vacancies_file)
    top_vac = get_top_vacancies(sort_vacancies(vacancies), 2)
    assert len(top_vac) == 2
    assert top_vac[0].title == "Java Developer"
    assert top_vac[1].title == "Python Developer"


def test_main(mocker, temp_vacancies_file):
    """тестирует основную функцию main"""
    mocker.patch("builtins.input", side_effect=["100000", "RUR", "python", "2"])
    mocker.patch("builtins.print")
    mocker.patch("data.hh.load_vacancies", return_value=load_vacancies(temp_vacancies_file))
    main()
