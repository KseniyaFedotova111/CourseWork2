from src.utils import validate_url, clean_string


class Vacancy:
    """класс для представления вакансии"""
    __slots__ = ("title", "company", "salary_from", "salary_to", "currency", "url")

    def __init__(self, title: str, company: str, salary_from: float, salary_to: float, currency: str, url: str):
        self.title = clean_string(title) or "Без названия"
        self.company = clean_string(company) or "Неизвестный работодатель"
        try:
            self.salary_from = float(salary_from) if salary_from is not None else 0.0
            if self.salary_from < 0:
                raise ValueError("Зарплата не может быть отрицательной")
        except (ValueError, TypeError):
            self.salary_from = 0.0
        try:
            self.salary_to = float(salary_to) if salary_to is not None else 0.0
            if self.salary_to < 0:
                raise ValueError("Зарплата не может быть отрицательной")
        except (ValueError, TypeError):
            self.salary_to = 0.0
        self.currency = clean_string(currency) or "Не указано"
        self.url = validate_url(url)

    def __str__(self) -> str:
        """строковое представление вакансии"""
        return (f"{self.title}\n"
                f"   Компания: {self.company}\n"
                f"   Зарплата: от {self.salary_from} до {self.salary_to} {self.currency}\n"
                f"   Ссылка: {self.url}")

    def __lt__(self, other: "Vacancy") -> bool:
        """сравнение вакансий по зарплате (меньше)"""
        return self.get_salary() < other.get_salary()

    def __gt__(self, other: "Vacancy") -> bool:
        """сравнение вакансий по зарплате (больше)"""
        return self.get_salary() > other.get_salary()

    def to_dict(self) -> dict:
        """преобразует вакансию в словарь для json"""
        return {
            "title": self.title,
            "company": self.company,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "currency": self.currency,
            "url": self.url
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Vacancy":
        """создает вакансию из словаря"""
        salary_from = data.get("salary_from", 0)
        salary_to = data.get("salary_to", 0)
        try:
            salary_from = float(salary_from)
        except (ValueError, TypeError):
            salary_from = 0.0
        try:
            salary_to = float(salary_to)
        except (ValueError, TypeError):
            salary_to = 0.0
        return cls(
            title=data.get("title", ""),
            company=data.get("company", ""),
            salary_from=salary_from,
            salary_to=salary_to,
            currency=data.get("currency", "Не указано"),
            url=data.get("url", "")
        )

    def get_salary(self) -> float:
        """возвращает зарплату для сортировки"""
        return self.salary_from if self.salary_from else self.salary_to
