
from base.function import filter_vacancies, get_vacancies_by_salary_range, sort_vacancies, get_top_vacancies, print_vacancies
from base.classy import HeadHunterAPI, JSONSaver

hh_api = HeadHunterAPI()

def user_interaction():
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат (например, 100000 - 150000): ")

    hh_vacancies = hh_api.get_vacancies(search_query)

    filtered_vacancies = filter_vacancies(hh_vacancies, filter_words)

    salary_filtered_vacancies = get_vacancies_by_salary_range(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(salary_filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print_vacancies(top_vacancies)

    json_saver = JSONSaver()
    json_saver.dump_to_file(top_vacancies)


if __name__ == '__main__':
    user_interaction()