import requests
from abc import ABC, abstractmethod
import pprint
import json
from abstract import Base_class
from operator import itemgetter, attrgetter


class HeadHunterAPI(Base_class):

    def get_request(self, search_word, page):
        """
        Метод для получения информации о вакансиях с сайта.
        В аргументы принимаются ключевое слово и количество страниц.
        """

        params = {
            "text": search_word,
            "page": page,
            "per_page": 100
        }
        return requests.get("https://api.hh.ru/vacancies?only_with_salary=true", params=params).json()['items']

    def get_vacancies(self, search_word, page=2):
        """
        Метод для передачи данных в метод 'get_request'
        В аргументы принимаются ключевое слово и количество страниц.
        В процессе вызывает 'get_request', передает ему полученные аргументы.
        Возвращает информацию о количестве вакансий.
        """
        pages = 0
        response = []

        for i in range(page):
            print(f"Парсинг страницы {i + 1}", end=": ")
            values = self.get_request(search_word, i)
            print(f"Найдено {len(values)} вакансий.")
            response.extend(values)

        return response


class Vacancy:

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
        Возвращает экземпляры для класса Vacancy.
        """

        with open(self.__filename, encoding='utf-8') as file:
            vacancies = json.load(file)
            return vacancies

    def show_vacancies_info(self):
        """
        Метод для вывода информации по вакансиям
        """

        result = []

        for row in self.get_vacancy:

            salary_min = 'Не указана' if not row['salary'].get('from') else row['salary'].get('from')
            salary_max = 'Не указана' if not row['salary'].get('to') else row['salary'].get('to')

            result.append(f"\nНаименование вакансии: {row['name']}\n"
                          f"ЗП: {salary_min} - {salary_max} {row['salary']['currency']}\n"
                          f"Работодатель: {row['employer']['name']}\n"
                          f"Ссылка на вакансию: {row['alternate_url']}.")

        return result

    def show_vacancies_full_info(self):

        result = []

        for row in self.get_vacancy:

            salary_min = 'Не указана' if not row['salary'].get('from') else row['salary'].get('from')
            salary_max = 'Не указана' if not row['salary'].get('to') else row['salary'].get('to')

            if salary_min is None and salary_max is None:
                salary_min = "Не указана"

            result.append(f"\nНаименование вакансии: {row['name']}\n"
                          f"Город: {row['area']['name']}\n"
                          f"Требования: {row['snippet']['requirement']}\n"
                          f"Задачи: {row['snippet']['responsibility']}\n"
                          f"Работодатель: {row['employer']['name']}\n"
                          f"ЗП: {salary_min} - {salary_max} {row['salary']['currency']}\n"
                          f"Ссылка на вакансию: {row['alternate_url']}.")

        return result

    def min_to_max_salary(self):
        """
        Метод: показывает вакансии по возрастанию ЗП.
        """
        result = []

        for row in self.get_vacancy:
            if row['salary']['from'] is None or row['salary']['to'] is None:
                continue

            else:
                salary_min = row['salary']['from']
                salary_max = row['salary']['to']
                salary_currency = row['salary']['currency']
                if salary_currency and salary_currency == "USD":
                    salary_min = salary_min * 82 if salary_min else None
                    salary_max = salary_max * 82 if salary_max else None
                elif salary_currency and salary_currency == "UZS":
                    salary_min = salary_min * 0.0071 if salary_min else None
                    salary_max = salary_max * 0.0071 if salary_max else None
                elif salary_currency and salary_currency == "EUR":
                    salary_min = salary_min * 89 if salary_min else None
                    salary_max = salary_max * 89 if salary_max else None
                elif salary_currency and salary_currency == "KZT":
                    salary_min = salary_min * 0.18 if salary_min else None
                    salary_max = salary_max * 0.18 if salary_max else None

                average_salary = round((salary_min + salary_max) / 2)
                result.append({"Наименование вакансии": row['name'],
                                     "Средняя заработная плата": average_salary,
                                     "Ссылка на вакансию": {row['alternate_url']}})
        sorted_data = sorted(result, key=itemgetter("Средняя заработная плата"), reverse=True)
        pprint.pprint(sorted_data[0:], width=110)

    def max_to_min_salary(self):
        """
        Метод: показывает вакансии по убыванию ЗП.
        """
        result = []

        for row in self.get_vacancy:
            if row['salary']['from'] is None or row['salary']['to'] is None:
                continue

            else:
                salary_min = row['salary']['from']
                salary_max = row['salary']['to']
                salary_currency = row['salary']['currency']
                if salary_currency and salary_currency == "USD":
                    salary_min = salary_min * 82 if salary_min else None
                    salary_max = salary_max * 82 if salary_max else None
                elif salary_currency and salary_currency == "UZS":
                    salary_min = salary_min * 0.0071 if salary_min else None
                    salary_max = salary_max * 0.0071 if salary_max else None
                elif salary_currency and salary_currency == "EUR":
                    salary_min = salary_min * 89 if salary_min else None
                    salary_max = salary_max * 89 if salary_max else None
                elif salary_currency and salary_currency == "KZT":
                    salary_min = salary_min * 0.18 if salary_min else None
                    salary_max = salary_max * 0.18 if salary_max else None


                average_salary = round((salary_min + salary_max) / 2)

                result.append({"Наименование вакансии": row['name'],
                               "Средняя заработная плата": average_salary,
                               "Ссылка на вакансию": {row['alternate_url']}})

        sorted_data = sorted(result, key=itemgetter("Средняя заработная плата"), reverse=False)
        pprint.pprint(sorted_data[0:], width=110)