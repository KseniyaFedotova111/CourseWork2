from abc import ABC, abstractmethod
import requests
import time
from typing import List, Dict, Any


class Parser(ABC):
    @abstractmethod
    def connect_to_api(self) -> None:
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        pass


class HH(Parser):
    def __init__(self, file_worker: Any) -> None:
        self.__url: str = 'https://api.hh.ru/vacancies'
        self.__headers: Dict[str, str] = {'User-Agent': 'HH-User-Agent'}
        self.__params: Dict[str, Any] = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies: List[Dict[str, Any]] = []
        self.__file_worker = file_worker

    def connect_to_api(self) -> None:
        response = requests.get(self.__url, headers=self.__headers, params={'per_page': 1})
        if response.status_code != 200:
            raise ConnectionError(f"Ошибка подключения к API: {response.status_code}")

    def load_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        self.connect_to_api()
        self.__params['text'] = keyword
        self.__params['page'] = 0
        self.__vacancies = []

        try:
            while True:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                response.raise_for_status()
                data = response.json()
                self.__vacancies.extend(data['items'])
                if self.__params['page'] >= data['pages'] - 1:
                    break
                self.__params['page'] += 1
                time.sleep(0.5)
        except requests.RequestException as e:
            print(f"Ошибка при загрузке вакансий: {e}")
            return []

        for vacancy in self.__vacancies:
            self.__file_worker.add_vacancy(vacancy)

        return self.__vacancies
