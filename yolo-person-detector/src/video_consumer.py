import threading
from datetime import datetime
from time import time
from flask import Response
from flask import Flask
from flask import render_template
from kafka import KafkaConsumer
import numpy as np
import cv2
from config import KAFKA_URI, YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, CONFIDENCE_PROBABILITY, \
    NON_MAXIMA_SUPPRESSION_THRESHOLD, YOLO_LABELS_PATH

outputFrame = None
lock = threading.Lock()
app = Flask(__name__)
num_persons = 0


@app.route('/')
def index():
    return render_template('index.html')


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/persons")
def get_persons():
    global num_persons
    return {'count': num_persons, 'time': datetime.now().strftime('%H:%M:%S')};


def detect_persons():
    global outputFrame, lock, num_persons
    # starting Kafka consumer to get video stream
    consumer = KafkaConsumer('frame', bootstrap_servers=KAFKA_URI)
    # YOLO Class Labels store
    LABELS = open(YOLO_LABELS_PATH, 'r').read().strip().split("\n")
    np.random.seed(42)
    # Picking a random color for boxing detected persons
    COLORS = np.random.randint(0, 255, size=(1, 3), dtype="uint8")
    # Reading YOLO model from disk
    net = cv2.dnn.readNetFromDarknet(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH)
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    count = 50
    boxes = []
    confidences = []
    classIDs = []
    persons = 0
    # looping on kafka consumer stream
    for msg in consumer:
        nparr = np.fromstring(msg.value, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        isFrameChecked = False
        persons = 0
        # Picking up every 50th frame from stream for person detection
        if count == 50:
            isFrameChecked = True
            boxes = []
            confidences = []
            classIDs = []
            count = 0
            (H, W) = img_np.shape[:2]
            # Resampling Blob of 320x320 resolution from image
            blob = cv2.dnn.blobFromImage(img_np, 1 / 255.0, (320, 320), swapRB=True, crop=False)
            net.setInput(blob)
            layerOutputs = net.forward(ln)
            for output in layerOutputs:
                for detection in output:
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]
                    # filtering class labels in output for person class
                    if confidence > CONFIDENCE_PROBABILITY and classID == 0:
                        # updating person count
                        persons = persons + 1
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype('int')
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))
                        # storing bounding box coordinates and confidence
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_PROBABILITY, NON_MAXIMA_SUPPRESSION_THRESHOLD)
        # Drawing boxes in the frame from video stream
        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(img_np, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                cv2.putText(img_np, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        with lock:
            outputFrame = img_np.copy()
            if isFrameChecked:
                num_persons = persons
        cv2.waitKey(1)
        count = count + 1


if __name__ == '__main__':
    # starting person detection in a daemon thread
    t = threading.Thread(target=detect_persons)
    t.daemon = True
    t.start()
    # starting flask container
    app.run(host='0.0.0.0', port=9000, debug=True, threaded=True, use_reloader=False)
