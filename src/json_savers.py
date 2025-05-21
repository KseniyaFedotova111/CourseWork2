from abc import ABC, abstractmethod
import json
import os
from typing import Dict, Any, List


class FileWorker(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_vacancies(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> None:
        pass


class JSONSaver(FileWorker):
    def __init__(self, filename: str = "vacancies.json"):
        """инициализирует JSONSaver с указанным именем файла"""
        self.__filename = os.path.join(os.path.dirname(__file__), "..", "data", filename)
        os.makedirs(os.path.dirname(self.__filename), exist_ok=True)

    def __load_vacancies(self) -> List[Dict[str, Any]]:
        """загружает вакансии из json-файла"""
        if not os.path.exists(self.__filename):
            return []
        with open(self.__filename, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def __save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """сохраняет вакансии в json-файл"""
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=2)  # type: ignore

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """добавляет вакансию в json-файл, если она не дублируется по url"""
        vacancies = self.__load_vacancies()
        formatted_vacancy = {
            "title": vacancy.get("name", ""),
            "company": vacancy.get("employer", {}).get("name", ""),
            "salary_from": vacancy.get("salary", {}).get("from") or 0,
            "salary_to": vacancy.get("salary", {}).get("to") or 0,
            "currency": vacancy.get("salary", {}).get("currency", "Не указано"),
            "url": vacancy.get("alternate_url", "")
        }
        if not any(v['url'] == formatted_vacancy['url'] for v in vacancies):
            vacancies.append(formatted_vacancy)
            self.__save_vacancies(vacancies)

    def get_vacancies(self) -> List[Dict[str, Any]]:
        """возвращает список всех вакансий из json-файла"""
        return self.__load_vacancies()

    def delete_vacancy(self, vacancy_id: str) -> None:
        """удаляет вакансию из json-файла по url"""
        vacancies = self.__load_vacancies()
        vacancies = [v for v in vacancies if v.get("url") != vacancy_id]
        self.__save_vacancies(vacancies)
