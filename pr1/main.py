from datetime import datetime
from datetime import timedelta
from faker import Faker
import yaml
from tqdm import tqdm

fake = Faker()

n = 1000
people = []
categories = [fake.word() for _ in range(10)]

for i in tqdm(range(n), colour='white'):
    person = dict()
    person['id'] = i
    person['name'] = fake.name()
    person['email'] = [fake.email() for _ in range(1, 3)]
    person['reg_date'] = fake.date()
    person['last_log_date'] = fake.date_between_dates(datetime.fromisoformat(person['reg_date']), datetime.today())
    person['status'] = fake.random_element(['confirmed', 'unconfirmed'])
    person['birthday_date'] = fake.date_between_dates(date_start= datetime.today() - timedelta(days=365 * 18), date_end=datetime.today())
    person['sex'] = fake.random_element(['male', 'female'])

    publishes = person['publishes'] = []
    for _ in range(fake.random_int(0, 10)):
        publish = dict()
        publish['name'] = fake.word() + " " + fake.word()
        publish['description'] = fake.text().replace("\n", " ")
        publish['pages_count'] = fake.random_int(1, 10)
        publish['category'] = fake.random_element(categories)
        publish['date'] = fake.date_between_dates(datetime.fromisoformat(person['reg_date']))

        comments = publish['comments'] = []
        for _ in range(fake.random_int(0, 5)):
            comment = dict()
            comment['person_id'] = fake.random_int(0, n - 1)
            comment['text'] = fake.text().replace("\n", " ")
            comments.append(comment)

        publishes.append(publish)

    people.append(person)


stream_write_yaml = open('document.yaml', 'w')
yaml.dump(people, stream_write_yaml)