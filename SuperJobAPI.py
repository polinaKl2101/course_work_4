import json
import os.path
import pprint
import datetime
from operator import itemgetter
import requests
from abstract import Base_class


class SuperJobAPI(Base_class):

    def __init__(self):
        self.__vacancies_list = []

    def get_request(self, search_word, city, page):
        """
        Метод для получения информации о вакансиях с сайта.
        В аргументы принимаются ключевое слово и количество страниц.
        """
        header = {
            'X-Api-App-Id': 'v3.r.137498737.ff3db599ac69b9e24cc1ee8e0b72e8574c771f18.b71917e577dcebfb286f773fe631a1dfc60f1d41'
        }

        params = {
            "keywords": search_word.title(),
            "town": city,
            "page": page,
            "count": 100,
            "more": True
        }
        return requests.get("https://api.superjob.ru/2.0/vacancies/?", headers=header, params=params).json()['objects']

    def get_vacancies(self, search_word, city, page=10):
        """
        Метод для передачи данных в метод 'get_request'
        В аргументы принимаются ключевое слово и количество страниц.
        В процессе вызывает 'get_request', передает ему полученные аргументы.
        Возвращает информацию о количестве вакансий.
        """
        pages = 0

        for i in range(page):
            print(f"Парсинг страницы {i + 1}", end=": ")
            values = self.get_request(search_word, city, i)
            print(f"Найдено {len(values)} вакансий.")
            self.__vacancies_list.extend(values)

    @property
    def get_vacancies_list(self):
        """Метод для вывода собранных данных"""

        return self.__vacancies_list


class Vacancy_SJ:

    def __init__(self, search_word: str):
        self.__filename = f"{search_word.title().strip()}.json"

    def add_vacancy(self, data):
        """"
        Метод, для записи полученных данных в формат JSON.
        В качестве аргумента передаем данные для записи.
        """
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @property
    def get_vacancy(self):
        """
        Метод для получения данных из JSON файла.
        """

        with open(self.__filename, encoding='utf-8') as file:
            vacancies = json.load(file)
            return vacancies

    def show_vacancies_info(self):
        """
        Метод для вывода информации по вакансиям
        """

        result_info = []

        for row in self.get_vacancy:
            salary_min = 'Не указана' if row['payment_from'] == 0 else row['payment_from']
            salary_max = 'Не указана' if row['payment_to'] == 0 else row['payment_to']

            result_info.append(f"\nНаименование вакансии: {row['profession']}\n"
                               f"ЗП: {salary_min} - {salary_max} {row['currency']}\n"
                               f"Ссылка на вакансию: {row['link']}.")

        return '\n'.join(result_info)

    def show_vacancies_full_info(self):

        result_info = []

        for row in self.get_vacancy:

            salary_min = 'Не указана' if row['payment_from'] == 0 else row['payment_from']
            salary_max = 'Не указана' if row['payment_to'] == 0 else row['payment_to']

            if salary_min is None and salary_max is None:
                salary_min = "Не указана"

            result_info.append(f"\n\nНаименование вакансии: {row['profession']}\n"
                               f"Город: {row.get('town')['title']}\n"
                               f"ЗП: {salary_min} - {salary_max} {row['currency']}\n"
                               f"Требования: {row.get('candidat')}"
                               f"Ссылка на вакансию: {row['link']}.")

        return '\n'.join(result_info)

    def min_to_max_salary(self):
        """
        Метод: показывает вакансии по возрастанию ЗП.
        """
        result_info = []

        for row in self.get_vacancy:
            average_salary = round((row['payment_from'] + row['payment_to']) / 2)

            if row['payment_from'] is None or row['payment_to'] is None:
                continue
            else:
                result_info.append({"Наименование вакансии": row['profession'],
                                    "Средняя заработная плата": average_salary,
                                    "Ссылка на вакансию": {row['link']}})

        sorted_data = sorted(result_info, key=itemgetter("Средняя заработная плата"), reverse=True)
        pprint.pprint(sorted_data[:100], width=110)

    def max_to_min_salary(self):
        """
        Метод: показывает вакансии по убыванию ЗП.
        """
        result_info = []

        for row in self.get_vacancy:
            average_salary = round((row['payment_from'] + row['payment_to']) / 2)

            if row['payment_from'] is None or row['payment_to'] is None:
                continue
            else:
                result_info.append({"Наименование вакансии": row['profession'],
                                    "Средняя заработная плата": average_salary,
                                    "Ссылка на вакансию": {row['link']}})

        sorted_data = sorted(result_info, key=itemgetter("Средняя заработная плата"), reverse=True)
        pprint.pprint(sorted_data[0:], width=110)