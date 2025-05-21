import pytest
from unittest.mock import patch
from src.main import main


@pytest.fixture
def mock_inputs():
    """фикстура для имитации пользовательского ввода"""
    return ["Python", "100000", "RUR", "developer", "5"]


@pytest.fixture
def mock_hh_vacancies():
    """фикстура для имитации данных api"""
    return [
        {
            "name": "Python Developer",
            "employer": {"name": "Tech Corp"},
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "alternate_url": "http://example.com"
        }
    ]


@patch("builtins.input")
@patch("src.api.HH.load_vacancies")
@patch("src.json_savers.JSONSaver.get_vacancies")
def test_main(mock_get_vacancies, mock_load_vacancies, mock_input, mock_inputs, mock_hh_vacancies):
    """тестирует основную функцию main"""
    mock_input.side_effect = mock_inputs
    mock_load_vacancies.return_value = mock_hh_vacancies
    mock_get_vacancies.return_value = [
        {
            "title": "Python Developer",
            "company": "Tech Corp",
            "salary_from": 100000,
            "salary_to": 150000,
            "currency": "RUR",
            "url": "http://example.com"
        }
    ]
    with patch("builtins.print") as mock_print:
        main()
        assert mock_print.called
