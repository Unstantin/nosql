from faker import Faker
from Employer import Employer
from State import State

fake = Faker()
state = State()


def put_employers(employers: list[Employer]):
    for emp in employers:
        name_check = '0123456789' in emp.name
        score_check = 1 < emp.average_score < 5

        if '0123456789' in emp.name or emp.average_score:
            continue

    with open('employers', "r") as file:


