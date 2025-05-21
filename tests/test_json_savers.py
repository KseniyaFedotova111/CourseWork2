import pytest
from src.json_savers import JSONSaver


@pytest.fixture
def json_saver(tmp_path):
    filename = tmp_path / "test_vacancies.json"
    return JSONSaver(filename=str(filename))


@pytest.fixture
def vacancy():
    return {
        "name": "Test Vacancy",
        "employer": {"name": "Test Company"},
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        "alternate_url": "http://example.com"
    }


def test_add_vacancy(json_saver, vacancy):
    json_saver.add_vacancy(vacancy)
    vacancies = json_saver.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Test Vacancy"
    assert vacancies[0]["company"] == "Test Company"
    assert vacancies[0]["salary_from"] == 100000
    assert vacancies[0]["salary_to"] == 150000
    assert vacancies[0]["currency"] == "RUR"
    assert vacancies[0]["url"] == "http://example.com"


def test_get_vacancies_empty(json_saver):
    vacancies = json_saver.get_vacancies()
    assert vacancies == []


def test_delete_vacancy(json_saver, vacancy):
    json_saver.add_vacancy(vacancy)
    json_saver.delete_vacancy("http://example.com")
    vacancies = json_saver.get_vacancies()
    assert len(vacancies) == 0


def test_add_vacancy_duplicate(json_saver, vacancy):
    json_saver.add_vacancy(vacancy)
    json_saver.add_vacancy(vacancy)
    vacancies = json_saver.get_vacancies()
    assert len(vacancies) == 1
