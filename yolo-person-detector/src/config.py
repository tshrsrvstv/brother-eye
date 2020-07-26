import os

KAFKA_URI = ['localhost:9092']
BASE_DIRECTORY = r'C:\JBM_Assignment\yolo-person-detector'
YOLO_WEIGHTS_PATH = os.path.join(BASE_DIRECTORY, 'yolo', 'yolov3.weights')
YOLO_CONFIG_PATH = os.path.join(BASE_DIRECTORY, 'yolo', 'yolov3.cfg')
YOLO_LABELS_PATH = os.path.join(BASE_DIRECTORY, 'yolo', 'coco.names')
CONFIDENCE_PROBABILITY = 0.5
NON_MAXIMA_SUPPRESSION_THRESHOLD = 0.3
