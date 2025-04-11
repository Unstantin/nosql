from jsonschema import validate, ValidationError
import json
from jsonschema import Draft7Validator
from jsonschema import FormatChecker


with open("schema.json") as file:
    schema = json.load(file)

with open("correct.json") as file:
    data = json.load(file)
    try:
        validate(instance=data, schema=schema)
        print("Корректно")
    except ValidationError as e:
        print(f"Ошибка employers, {e}")

print()

with open("uncorrect.json") as file:
    data = json.load(file)

validator = Draft7Validator(schema)
errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

if not errors:
    print("Корректно")
else:
    for error in errors:
        print(f"Ошибка: {error.message} (путь: {error.path})")
    print(f"\nВсего ошибок: {len(errors)}")

