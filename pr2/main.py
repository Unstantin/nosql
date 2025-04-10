import re
import json
from datetime import datetime

from jsonschema import validate, ValidationError
import json

with open("employers_schema.json") as file:
    employers_schema = json.load(file)
with open("vacancy_schema.json") as file:
    vacancy_schema = json.load(file)
with open("reviews_schema.json") as file:
    reviews_schema = json.load(file)

with open("employers.json") as file:
    data = json.load(file)
    try:
        validate(instance=data, schema=employers_schema)
        print("Корректно employers")
    except ValidationError as e:
        print(f"Ошибка employers, {e}")

with open("vacancy.json") as file:
    data = json.load(file)
    try:
        validate(instance=data, schema=vacancy_schema)
        print("Корректно vacancy")
    except ValidationError as e:
        print(f"Ошибка vacancy, {e}")

with open("reviews.json") as file:
    data = json.load(file)
    try:
        validate(instance=data, schema=reviews_schema)
        print("Корректно reviews")
    except ValidationError as e:
        print(f"Ошибка reviews, {e}")


print("ТЕПЕРЬ С ОШИБКАМИ")
with open("employers_with_error.json") as file:
    data = json.load(file)
    try:
        validate(instance=data, schema=employers_schema)
        print("Корректно employers")
    except ValidationError as e:
        print(f"Ошибка employers, {e}")

with open("vacancy_with_error.json") as file:
    data = json.load(file)
    try:
        validate(instance=data, schema=vacancy_schema)
        print("Корректно vacancy")
    except ValidationError as e:
        print(f"Ошибка vacancy, {e}")

with open("reviews_with_error.json") as file:
    data = json.load(file)
    try:
        validate(instance=data, schema=reviews_schema)
        print("Корректно reviews")
    except ValidationError as e:
        print(f"Ошибка reviews, {e}")