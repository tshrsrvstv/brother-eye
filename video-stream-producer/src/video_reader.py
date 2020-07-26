from kafka import KafkaProducer

import cv2

from config import IP_CAM_URI, KAFKA_URI

# Initializing Kafka Producer
producer = KafkaProducer(bootstrap_servers=KAFKA_URI)
# Initializing VideoCapture
video = cv2.VideoCapture(IP_CAM_URI if IP_CAM_URI is not None else 0)
# Reading video and streaming to kafka
while video.isOpened():
    success, frame = video.read()
    if not success:
        print('Something went wrong!!!')
        break
    ret, buffer = cv2.imencode('.jpg', frame)
    producer.send('frame', buffer.tobytes())
