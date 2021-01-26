from kafka.producer import KafkaProducer
import json
import csv
from time import sleep


producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
with open('blacklist.csv') as file:
    reader = csv.DictReader(file, delimiter=",")
    for row in reader:
        producer.send(topic='blacklist', value=row)
        producer.flush()
        sleep(1)





