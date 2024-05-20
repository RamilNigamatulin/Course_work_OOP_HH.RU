from base.classy import Vacancy, OutputAPI, HeadHunterAPI, JSONSaver

hh_api = HeadHunterAPI()

def filter_vacancies(vacancies, filter_words):
    """ Фильтрует список вакансий по ключевым словам."""
    return [vacancy for vacancy in vacancies if any(word.lower() in vacancy.title.lower() for word in filter_words)]


def get_vacancies_by_salary_range(vacancies, salary_range):
    """Фильтрует список вакансий по заданному диапазону зарплат."""
    try:
        min_salary, max_salary = map(int, salary_range.split('-'))
    except ValueError:
        print("Некорректный формат диапазона зарплат. Пожалуйста, введите его в формате 'мин - макс'.")
        return []

    filtered_vacancies = []
    for vacancy in vacancies:
        if vacancy.max_salary == "Максимальная зарплата не указана":
            continue
        try:
            max_salary_value = int(vacancy.max_salary)
            if min_salary <= max_salary_value <= max_salary:
                filtered_vacancies.append(vacancy)
        except ValueError:
            continue

    return filtered_vacancies


def sort_vacancies(vacancies):
    """Сортирует список вакансий по убыванию максимальной зарплаты."""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies, top_n):
    """Возвращает первые N вакансий из отсортированного списка."""
    return vacancies[:top_n]


def print_vacancies(vacancies):
    """Вывод информации о вакансиях."""
    for i, vacancy in enumerate(vacancies, start=1):
        print(f"{i}. Платформа поиска: {hh_api.platforms()}")
        print(f"   Название вакансии: {vacancy.title}")
        print(f"   Ссылка на вакансию API: {vacancy.url}")
        print(f"   Ссылка на вакансию URL: {vacancy.alternate_url}")
        print(f"   Зарплата: {vacancy.min_salary} - {vacancy.max_salary} {vacancy.currency}")
        print(f"   Регион: {vacancy.area}")