def user_interaction(api_instance, api_interface, city=None):

    class_instance = api_instance()

    commands = {1: "Посмотреть краткую информацию о всех вакансиях",
                2: "Посмотреть расширенную информацию о всех вакансиях",
                3: "Посмотреть вакансии по возрастанию средней заработной платы",
                4: "Посмотреть вакансии по убыванию средней заработной платы",
                5: "Завершение программы"}

    view_commands = '\n'.join([f"{key}: {value}" for key, value in commands.items()])

    while True:
        search_word = input('Введите вакансию для поиска: ').title().strip()

        pages_for_search = input('Введите количество страниц по которым произвести парсинг: ').strip()
        print()

        if city is None:
            class_instance.get_vacancies(search_word, int(pages_for_search))
        else:
            class_instance.get_vacancies(search_word, city, int(pages_for_search))

        result_info = class_instance.get_vacancies_list

        filename = input("Введите названия для JSON файла: ").strip()

        api_interface = api_interface(filename)
        api_interface.add_vacancy(result_info)

        print("\nВыберите команду: ")
        print(view_commands)
        print("Введите номер команды: ")


        user_answer = input("\nВведите номер: ").title().strip()

        while user_answer != '5':

            if user_answer == "1":
                print(api_interface.show_vacancies_info())
            elif user_answer == "2":
                print(api_interface.show_vacancies_full_info())
            elif user_answer == "3":
                api_interface.min_to_max_salary()
            elif user_answer == "4":
                api_interface.max_to_min_salary()

            user_answer = input('\nВведите номер: ').title().strip()
        print(f'Данные сохранены в файл {filename.title()}.json')
        exit(0)


