from kafka.consumer import KafkaConsumer

import psycopg2
import json

consumer = KafkaConsumer(
    'blacklist',
     bootstrap_servers=['localhost:9092'],
     value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    consumer_timeout_ms=5000
    # iter_timeout=10
)


conn = psycopg2.connect(dbname='beeline_db', user='rinatmirzagalamov', host='localhost')

def single_insert(conn, insert_req):
    cursor = conn.cursor()
    cursor.execute(insert_req)
    conn.commit()
    cursor.close()

for message in consumer:
    message = message.value
    query = "INSERT INTO blacklist(ctn, event_time) values (%s,'%s')" % (message['Номер телефона'], message['Время события'])
    single_insert(conn, query)
    print(message)

curs = conn.cursor()
curs.execute("CREATE INDEX ctn_index ON BLACKLIST(ctn);")
conn.commit()
curs.close()
print('end')
