import yaml
from yaml import Loader
from operator import itemgetter
import csv
from tqdm import tqdm

stream_read_yaml = open('document.yaml', 'r')
loaded_people = yaml.load(stream_read_yaml, Loader=Loader)

for person in tqdm(loaded_people):
    person['publishes'].sort(key=itemgetter('date'), reverse=True)


stream_write_people = open('people.csv', 'w')
people_writer = csv.writer(stream_write_people)
people_header = ['id', 'name', 'email', 'reg_date', 'last_log_date', 'status', 'birthday_date', 'sex']
people_writer.writerow(people_header)

stream_write_publishes = open('publishes.csv', 'w')
publishes_writer = csv.writer(stream_write_publishes)
publishes_header = ['id', 'name', 'description', 'pages_count', 'category', 'date', 'author_id']
publishes_writer.writerow(publishes_header)

stream_write_comments = open('comments.csv', 'w')
comments_writer = csv.writer(stream_write_comments)
comments_header = ['publish_id', 'person_id', 'text']
comments_writer.writerow(comments_header)

all_publishes = []
persons_id = []
publish_id_count = 1
for person in tqdm(loaded_people):
    people_writer.writerow([person[index] for index in people_header])
    for publish in person['publishes']:
        all_publishes.append(publish)
        persons_id.append(person['id'])
        #publishes_writer.writerow([publish_id_count] + [publish[index] for index in publishes_header[1:-1]] + [person['id']])
        for comment in publish['comments']:
            comments_writer.writerow([publish_id_count] + [comment[index] for index in comments_header[1:]])
        publish_id_count += 1

stream_write_people.close()
stream_write_comments.close()

sorted_publishes = sorted(all_publishes, key=lambda item: item['date'], reverse=True)
index = 0
for publish in sorted_publishes:
    publishes_writer.writerow([publish_id_count] + [publish[index] for index in publishes_header[1:-1]] + [persons_id[index]])
    index += 1

stream_write_publishes.close()


