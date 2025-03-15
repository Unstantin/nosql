import re
import json
from datetime import datetime


def check_employers(employers: list):
    count_of_incorrect = 0
    for emp in employers:
        # если нет хотя бы одной буквы
        name_pattern = re.compile(r'[а-яА-Яa-zA-Z]')
        name_check = not name_pattern.search(emp['name'])

        # если не в диапазоне
        score_check = not (1 <= emp['average_score'] <= 5)

        if name_check or score_check:
            count_of_incorrect += 1
            print(emp)

    return count_of_incorrect


def check_vacancy(vacancy: list):
    count_of_incorrect = 0
    for vac in vacancy:
        # если нет хотя бы одной буквы
        name_pattern = re.compile(r'[а-яА-Яa-zA-Z]')
        name_check = not name_pattern.search(vac['name'])

        # если не положительное и целое число
        salary_check = type(vac['salary']) != int or vac['salary'] < 0

        # если не один символ или он цифра
        currency_pattern = re.compile(r'[0-9]')
        currency_check = len(vac['currency']) != 1 or currency_pattern.search(vac['currency'])

        # если есть цифры
        metro_pattern = re.compile(r'[0-9]')
        metro_check = metro_pattern.search(vac['metro'])

        # если дата позже сегодня
        date_of_publish_check = datetime.today() < datetime.fromisoformat(vac['date_of_publish'])

        # если не положительное и целое число
        count_of_responses_check = type(vac['count_of_responses']) != int or vac['count_of_responses'] < 0

        # если не булевое
        without_experience_check = type(vac['without_experience']) != bool

        # если не булевое
        with_distance_check = type(vac['with_distance']) != bool

        # если не список
        key_skills_check = type(vac['key_skills']) != list

        if name_check or salary_check or metro_check \
                or date_of_publish_check or count_of_responses_check \
                or without_experience_check or with_distance_check \
                or currency_check or key_skills_check:
            count_of_incorrect += 1
            print(vac)

        return count_of_incorrect


def check_reviews(reviews: list):
    count_of_incorrect = 0
    for rew in reviews:
        # если не целое положительное число
        work_duration_check = type(rew['work_duration']) != int or rew['work_duration'] < 0

        # если есть цифры
        measure_of_work_duration_pattern = re.compile(r'0-9')
        measure_of_work_duration_check = measure_of_work_duration_pattern.search(rew['measure_of_work_duration'])

        # если позже сегодня
        date_of_publish_check = datetime.today() < datetime.fromisoformat(rew['date_of_publish'])

        # если не в диапозоне и не целое
        score_check = type(rew['score']) != int or not 0 <= rew['score'] <= 5

        if work_duration_check or measure_of_work_duration_check \
                or date_of_publish_check or score_check:
            count_of_incorrect += 1
            print(rew)

    return count_of_incorrect


with open('employers.json', 'r') as file:
    print('employers')
    print(check_employers(json.load(file)))

with open('employers_with_error.json', 'r') as file:
    print('employers_with_error')
    print(check_employers(json.load(file)))

with open('vacancy.json', 'r') as file:
    print('vacancy')
    print(check_vacancy(json.load(file)))

with open('vacancy_with_error.json', 'r') as file:
    print('vacancy_with_error')
    print(check_vacancy(json.load(file)))

with open('reviews.json') as file:
    print('reviews')
    print(check_reviews(json.load(file)))

with open('reviews_with_error.json') as file:
    print('reviews_with_error')
    print(check_reviews(json.load(file)))
