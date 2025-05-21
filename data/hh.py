import json
import os
from src.vacancy import Vacancy
from src.utils import validate_currency, format_salary

VACANCIES_FILE = os.path.join(os.path.dirname(__file__), "vacancies.json")


def load_vacancies(filename: str) -> list:
    """загружает вакансии из json-файла"""
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден.")
        return []

    with open(filename, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            return [Vacancy.from_dict(item) for item in data]
        except json.JSONDecodeError:
            print("Ошибка чтения JSON-файла.")
            return []


def filter_vacancies_by_salary(vacancies: list, min_salary: float, currency: str = "RUR") -> list:
    """фильтрует вакансии по минимальной зарплате и валюте"""
    filtered = []
    for vacancy in vacancies:
        if vacancy.currency != currency:
            continue
        salary = vacancy.salary_from if vacancy.salary_from else vacancy.salary_to
        if salary >= min_salary:
            filtered.append(vacancy)
    return filtered


def filter_vacancies_by_keywords(vacancies: list, keywords: list) -> list:
    """фильтрует вакансии по ключевым словам"""
    if not keywords:
        return vacancies
    return [v for v in vacancies if any(k.lower() in v.title.lower() for k in keywords)]


def sort_vacancies(vacancies: list) -> list:
    """фильтрует вакансии по зарплате по убыванию"""
    return sorted(vacancies, key=lambda v: v.get_salary(), reverse=True)


def get_top_vacancies(vacancies: list, top_n: int) -> list:
    """возвращает топ n вакансий"""
    return vacancies[:top_n]


def print_vacancies(vacancies: list) -> None:
    """выводит вакансии в консоль"""
    if not vacancies:
        print("Нет подходящих вакансий.")
        return

    for idx, vacancy in enumerate(vacancies, 1):
        print(f"{idx}. {vacancy.title}")
        print(f"   Компания: {vacancy.company}")
        print(f"   {format_salary(vacancy.salary_from, vacancy.salary_to, vacancy.currency)}")
        print(f"   Ссылка: {vacancy.url}")
        print("-" * 60)


def main() -> None:
    """основная функция для взаимодействия с пользователем"""
    vacancies = load_vacancies(VACANCIES_FILE)
    if not vacancies:
        return

    try:
        min_salary = float(input("Введите минимальную желаемую зарплату: "))
    except ValueError:
        print("Ошибка: введите числовое значение.")
        return

    currency = input("Введите валюту (RUR, KZT, UZS, USD, или пусто для RUR): ").strip() or "RUR"
    currency = validate_currency(currency)
    if currency == "RUR" and currency != input:
        print("Ошибка: некорректная валюта. Используется RUR.")

    keywords = input("Введите ключевые слова (через пробел): ").strip().split()
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
