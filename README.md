# brother-eye
In times of COVID 19 it is very important for everyone to maintain a proper social distance and follow all the safety norms and precautions, to help humanity fight the battle against the deadly virus AI/ML can be leveraged to track any breach in social distance practices in various places of public gathering. Brother Eye is a Real Time Person Detection System conceptualized for assisting offices, hotels, restaurants and other places of public gatherings to detect number of individuals within a frame and point out the breach scenarios. The implementation uses a pre trained YOLOv3 (You Only Look Once) model over COCO dataset for person detection. Other technologies involved for developing the application are RTSP, Apache Kafka, Python Flask, OpenCV, Numpy, Angular JS, ChartJs, Bootstrap, HTML, CSS, etc.

# brother-eye Components
Brother Eye have primarily below components.
1. `video-stream-producer`
   Responsible for getting feed from the configured camera and send it over kafka streams.
2. `yolo-person-detector`
   Responsible for reading video from the kafka stream, detecting persons in every 50th frame from the stream and running a flask server to host angular JS app and host relevant APIs.
    
# Quick Installation Instructions on Windows for Demo
For demo purposes we can feed video stream from laptop webcam, apache kafka and yolo detector on same machine.
1. Install python 3 preferably version 3.7.7 or above. You can get Python 3.7.7 from [here](https://www.python.org/downloads/release/python-377/).
2. Download Apache Kafka from [here](https://www.apache.org/dyn/closer.cgi?path=/kafka/2.5.0/kafka_2.12-2.5.0.tgz). Once kafka is downloaded untar the downloaded file within a directory and run below commands in cmd Terminal to start kafka broker at 9092 port.

   ```bat
   cd <UNTAR_DIR>\kafka_2.12-2.5.0
   ```
   
   ```bat
   bin\windows\zookeeper-server-start.bat config\zookeeper.properties
   ```
   You might have to open up a new Terminal for running below command.
   
   ```bat
   bin\windows\kafka-server-start.bat config\server.properties
   ```
3. Install Git Bash from [here](https://git-scm.com/downloads) and clone the repository using below command within some directory.

   ```bat
   git clone https://github.com/tshrsrvstv/brother-eye.git
   ```
4. To install python dependency packages run below commands.
   
   ```bat
   cd <CLONE_DIR>\brother-eye
   ```
   
   ```bat
   pip install -r requirements.txt
   ```
5. Downloads Pre trained YOLO weights from [here](https://pjreddie.com/media/files/yolov3.weights) and keep it inside `<CLONE_DIR>\brother-eye\yolo-person-detector\yolo` directory.
6. Edit `config.py` kept inside folder `<CLONE_DIR>\brother-eye\yolo-person-detector\src`, change value for **BASE_DIRECTORY** to `<CLONE_DIR>\brother-eye\yolo-person-detector`.
7. Run `yolo-person-detector` using below commands.

   ```bat
   cd <CLONE_DIR>\brother-eye\yolo-person-detector\src
   ```
   
   ```bat
   python video_consumer.py
   ```
8. Run `video-stream-producer` using below commands.

   ```bat
   cd <CLONE_DIR>\brother-eye\video-stream-producer\src
   ```
   
   ```bat
   python video_reader.py
   ```
 9. Go to [URL](http://localhost:9000/), Brother Eye Live Feed Dashboard should be loaded with webcam feed and Person Count chart.
 
# Distributed System
Brother Eye can also take a live feed from a IP Cam over a network. Please read this [link](http://help.angelcam.com/en/articles/372646-how-to-find-a-rtsp-address-for-an-onvif-compatible-camera-nvr-dvr) to obtain RTSP address for the IP Cam in the network. Edit `config.py` kept inside folder `<CLONE_DIR>\brother-eye\video-stream-producer\src`, update **IP_CAM_URI** value with the RTSP address.
**video-stream-producer**, **Kafka** and **yolo-person-detector** can also be run on distributed servers over network by changing `config.py` for both components.
