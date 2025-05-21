from src.api import HH
from src.json_savers import JSONSaver
from src.vacancy import Vacancy
from src.utils import validate_currency
from data.hh import filter_vacancies_by_salary, filter_vacancies_by_keywords, sort_vacancies, get_top_vacancies, \
    print_vacancies


def main() -> None:
    """основная функция для взаимодействия с пользователем"""
    file_worker = JSONSaver()
    hh_parser = HH(file_worker)

    keyword = input("Введите ключевое слово для поиска вакансий (например, Python): ").strip()
    if not keyword:
        print("Ошибка: ключевое слово не может быть пустым.")
        return

    try:
        print(f"Загрузка вакансий для '{keyword}'...")
        vacancies_data = hh_parser.load_vacancies(keyword)
        if not vacancies_data:
            print("Не удалось загрузить вакансии.")
            return
        print(f"Загружено {len(vacancies_data)} вакансий.")
    except Exception as e:
        print(f"Ошибка при загрузке вакансий: {e}")
        return

    vacancies = [Vacancy.from_dict(item) for item in file_worker.get_vacancies()]

    try:
        min_salary = float(input("Введите минимальную желаемую зарплату: "))
    except ValueError:
        print("Ошибка: введите числовое значение.")
        return

    currency = input("Введите валюту (RUR, KZT, UZS, USD, или пусто для RUR): ").strip() or "RUR"
    currency = validate_currency(currency)
    if currency == "RUR" and currency != input:
        print("Ошибка: некорректная валюта. Используется RUR.")

    keywords = input("Введите ключевые слова для фильтрации (через пробел): ").strip().split()
    try:
        top_n = int(input("Введите количество вакансий для вывода: "))
        if top_n <= 0:
            raise ValueError
    except ValueError:
        print("Ошибка: введите положительное число.")
        return

    suitable = filter_vacancies_by_salary(vacancies, min_salary, currency)
    suitable = filter_vacancies_by_keywords(suitable, keywords)
    suitable = sort_vacancies(suitable)
    suitable = get_top_vacancies(suitable, top_n)

    print_vacancies(suitable)


if __name__ == "__main__":
    main()
