from HeadHunter import HeadHunterAPI, Vacancy


def main():

    #search_word = input("Введите ключевое слово для поиска ")
    search_word = "Python"

    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()
    #superjob_api = SuperJobAPI()

    # Получение вакансий с разных платформ
    hh_vacancies = hh_api.get_vacancies(search_word)

    # Сохранение информации о вакансиях в файл
    json_saver = Vacancy(search_word)
    json_saver.add_vacancy(hh_vacancies)
    #data = json_saver.show_vacancies_info()
    #data = json_saver.show_vacancies_full_info()
    #data = json_saver.get_vacancy()

    data = json_saver.min_to_max_salary()

    #for i in data:
       # print(i)

    # json_saver.delete_vacancy(vacancy)

    #superjob_vacancies = superjob_api.get_vacancies("Python")

    # Функция для взаимодействия с пользователем
    #def user_interaction():
        #platforms = ["HeadHunter", "SuperJob"]
        #search_query = input("Введите поисковый запрос: ")
        #top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        #filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
        #filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)

        #if not filtered_vacancies:
            #print("Нет вакансий, соответствующих заданным критериям.")
            #return

        #sorted_vacancies = sort_vacancies(filtered_vacancies)
        #top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
        #print_vacancies(top_vacancies)

if __name__ == "__main__":
    main()
