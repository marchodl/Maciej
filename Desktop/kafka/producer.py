from kafka import KafkaConsumer, KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
import json
import json_lines


# create a producer
# The key_serializer and value_serializer is required because we need to send data to kafka in
# bytes OR in a type that can be serialized (ASCII, UTF-8, etc).
# We turn it to JSON (encoded in UTF-8) since it's a common message format

producer = KafkaProducer(bootstrap_servers='localhost:9092', acks= 1, 
                         key_serializer=lambda v: json.dumps(v).encode('utf-8'), # taking a json -> string
                         value_serializer=lambda v: json.dumps(v).encode('utf-8')
                         )
consumer = KafkaConsumer('books', # This is the Kafka topic name to consume from
                         auto_offset_reset='earliest', # everytime this consumer connect I reset to begininig
                         group_id='book-filter', # consumer group id
                         enable_auto_commit=False, # I dont want to keep track
                         bootstrap_servers=['localhost:9092'],
                         key_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         value_deserializer=lambda m: json.loads(m.decode('utf-8'))
                         )
                         
# run this first alone
# with open('books.json','rb') as f:
#     for item in json_lines.reader(f):
#         future = producer.send(topic='books', 
#                                key = item['bookID'], value = item)
#         result = future.get(timeout=100)
#         # print(item)

# Process messages
for message in consumer:
    try:
        book_rating = float(message.value['average_rating'])
        
        if book_rating > 4.1:
            print(f"Good book found! Rating: {book_rating}, Title: {message.value['title']}")
            
            # Send to best_books topic
            future = producer.send(
                topic='best_books',
                key=message.key,
                value=message.value
            )
            
            # Optional: Wait for confirmation
            future.get(timeout=10)
            
    except (KeyError, ValueError) as e:
        print(f"Skipping malformed message: {e}")
        continue