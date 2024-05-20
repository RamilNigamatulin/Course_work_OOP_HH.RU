import requests
import json
from abc import ABC, abstractmethod
import os


class Vacancy:
    """Класс для представления вакансии"""
    title: str
    url: str
    alternate_url: str
    min_salary: int
    max_salary: int
    currency: str
    area: str

    def __init__(self, title, url, alternate_url, min_salary, max_salary, currency, area):
        self.title = title
        self.url = url
        self.alternate_url = alternate_url
        self.min_salary = min_salary if min_salary is not None else "Минимальная зарплата не указана"
        self.max_salary = max_salary if max_salary is not None else "Максимальная зарплата не указана"
        self.currency = currency
        self.area = area


    def __str__(self):
        return f'{self.title}, {self.url}, {self.alternate_url}, {self.min_salary} - {self.max_salary} {self.currency}, {self.area}'

    def __repr__(self):
        return f'{self.title}, {self.url}, {self.alternate_url}, {self.min_salary} - {self.max_salary} {self.currency}, {self.area}'

    def __gt__(self, other):
        if isinstance(other, Vacancy):
            if self.max_salary == "Максимальная зарплата не указана":
                return False
            elif other.max_salary == "Максимальная зарплата не указана":
                return True
            else:
                return self.max_salary > other.max_salary
        return NotImplemented

    def to_json(self):
        """Преобразует объект вакансии в словарь для сериализации в JSON."""
        return {
            'title': self.title,
            'url': self.url,
            'alternate_url': self.alternate_url,
            'min_salary': self.min_salary,
            'max_salary': self.max_salary,
            'currency': self.currency,
            'area': self.area,
        }


class OutputAPI(ABC):
    """Абстрактный базовый класс для выходного API."""
    @abstractmethod
    def platforms(self):
        pass


class HeadHunterAPI(OutputAPI):
    """Класс для работы с API HeadHunter."""
    def __init__(self):
        self.url = 'https://api.hh.ru/'

    def platforms(self):
        return 'HeadHunter'

    def get_vacancies(self, title):
        """Получает список вакансий по запросу."""
        params = {
            'text': title,
            'area': '1',
            'per_page': '100'
        }
        try:
            response = requests.get(f'{self.url}vacancies', params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Произошла ошибка при запросе к API: {e}")
            return []

        vacancies = []
        for item in response.json()['items']:
            vacancies.append(
                Vacancy(
                    title=item.get('name'),
                    url=item.get('url'),
                    alternate_url=item.get('alternate_url'),
                    min_salary=(item.get('salary', {}) or {}).get('from', 'Минимальная зарплата не указана'),
                    max_salary=(item.get('salary', {}) or {}).get('to', 'Максимальная зарплата не указана'),
                    currency=(item.get('salary', {}) or {}).get('currency', {}),
                    area=item.get('area', {}).get('name'),
                )
            )
        return vacancies


class JSONSaver:
    """Класс для сохранения данных в формате JSON."""
    def __init__(self, directory='data'):
        self.directory = directory
        # Создаем папку, если ее еще нет
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def dump_to_file(self, vacancies):
        """Сохраняет список вакансий в файл JSON."""
        file_path = os.path.join(self.directory, 'data.json')
        with open(file_path, mode='w', encoding='utf-8') as file:
            json.dump([vac.to_json() for vac in vacancies], file, ensure_ascii=False, indent=4)
