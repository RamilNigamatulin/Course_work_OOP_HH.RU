import requests
from pprint import pprint
import json
from abc import ABC, abstractmethod

class Vacancy:

    def __init__(self, title, url, salary):
        self.title = title
        self.url = url
        self.salary = salary or 0

    def __str__(self):
        return f'{self.title}, {self.url}, {self.salary}'

    def __repr__(self):
        return f'{self.title}, {self.url}, {self.salary}'

    def __gt__(self, other):
        return self.salary > other.salary

    def to_json(self):
        return {
            'title': self.title,
            'url': self.url,
            'salary': self.salary
        }



class HeadHunterAPI:

    def __init__(self) -> object:
        self.url = 'https://api.hh.ru/'

    def get_vacancies(self, title):
        params = {
            'text': title,
            'area': '1',
            'per_page': '100'
        }
        response = requests.get(f'{self.url}vacancies', params=params)
        vac = []
        for item in response.json()['items']:
            vac.append(
                Vacancy(
                    title=item.get('name'),
                    url=item.get('url'),
                    salary=(item.get('salary', {}) or {}).get('to', 0)
                )
            )

        return vac


class JSONSaver:
    def dump_to_file(self, vacancies):
        with open('data.json', mode='w', encoding='utf-8') as file:
            json.dump([vac.to_json() for vac in vacancies], file, ensure_ascii=False, indent=4)



if __name__ == '__main__':
    pprint(sorted(HHClass().get_vacancies('python')))
    vac = sorted(HHClass().get_vacancies('python'))
    JSONSaver().dump_to_file(vac)