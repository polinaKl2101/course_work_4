from HeadHunter import HeadHunterAPI, Vacancy
from SuperJobAPI import SuperJobAPI, Vacancy_SJ
from user_interaction import user_interaction

if __name__ == '__main__':

    print("Программа для парсинга вакансий")
    platforms = input("Выберите платформу для поиска:\n"
                      "1. Head Hunter\n"
                      "2. Super Job\n"
                      "Введите номер: ").strip()

    while platforms not in ('1', '2'):
        platforms = input('Такой платформы не найдено. Повторите ввод: ').strip()

    if platforms == '1':
        print('\nВы выбрали платформу Super Job.')

        user_city = input('Введите город в котором хотите посмотреть вакансии: ').title().strip()

        while not user_city.replace(' ', '').isalpha():
            user_city = input('Название города введено некорректно.\n'
                                'Повторите ввод: ')

        print(user_interaction(SuperJobAPI, Vacancy_SJ, user_city))

    elif platforms == '2':

        print('Вами была выбрана платформа: HeadHunter\n Введите уточняющую информацию для поиска')
        print(user_interaction(HeadHunterAPI, Vacancy))