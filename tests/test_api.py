import pytest
import requests
from src.api import HH
from src.json_savers import JSONSaver


@pytest.fixture
def json_saver(mocker):
    """создаёт мок-объект JSONSaver для тестов"""
    return mocker.Mock(spec=JSONSaver)


@pytest.fixture
def hh(json_saver):
    """создаёт объект HH для тестов"""
    return HH(json_saver)


def test_connect_to_api_success(hh, mocker):
    """тестирует успешное подключение к api HH"""
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 200
    hh.connect_to_api()
    assert True


def test_connect_to_api_failure(hh, mocker):
    """тестирует ошибку подключения к api HH"""
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 404
    with pytest.raises(ConnectionError):
        hh.connect_to_api()


def test_load_vacancies_success(hh, mocker, json_saver):
    """тестирует успешную загрузку вакансий с HH"""
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'items': [{'id': '1', 'name': 'Test Vacancy', 'alternate_url': 'http://example.com'}],
        'pages': 1
    }
    vacancies = hh.load_vacancies("Python")
    assert len(vacancies) == 1
    assert vacancies[0]['name'] == 'Test Vacancy'
    json_saver.add_vacancy.assert_called_once()


def test_load_vacancies_empty(hh, mocker):
    """тестирует загрузку пустого списка вакансий"""
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'items': [], 'pages': 1}
    vacancies = hh.load_vacancies("Python")
    assert len(vacancies) == 0


def test_load_vacancies_request_exception(hh, mocker):
    """тестирует обработку исключения при загрузке вакансий"""
    mock_get = mocker.patch('requests.get')
    mock_get.side_effect = [
        mocker.Mock(status_code=200),
        mocker.Mock(
            status_code=200,
            json=mocker.Mock(side_effect=requests.RequestException("Network error"))
        )
    ]
    vacancies = hh.load_vacancies("Python")
    assert vacancies == []
