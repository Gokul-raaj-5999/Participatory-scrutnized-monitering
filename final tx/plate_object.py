import cv2
import pytesseract
import numpy as np
import argparse
import subprocess
import time
import os
import sqlite3
#from yolo_utils import infer_image
conn = sqlite3.connect('tx.sqlite')
cur = conn.cursor()
cur.executescript('''
DROP TABLE IF EXISTS obj;
CREATE TABLE obj(
ind INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
detected TEXT
);
''')
conn.commit()
cur.close()

FLAGS = []
def generate_boxes_confidences_classids(outs, height, width, tconf):
    boxes = []
    confidences = []
    classids = []

    for out in outs:
        for detection in out:
            #print (detection)
            #a = input('GO!')

            # Get the scores, classid, and the confidence of the prediction
            scores = detection[5:]
            classid = np.argmax(scores)
            confidence = scores[classid]

            # Consider only the predictions that are above a certain confidence level
            if confidence > tconf:
                # TODO Check detection
                box = detection[0:4] * np.array([width, height, width, height])
                centerX, centerY, bwidth, bheight = box.astype('int')

                # Using the center x, y coordinates to derive the top
                # and the left corner of the bounding box
                x = int(centerX - (bwidth / 2))
                y = int(centerY - (bheight / 2))

                # Append to list
                boxes.append([x, y, int(bwidth), int(bheight)])
                confidences.append(float(confidence))
                classids.append(classid)

    return boxes, confidences, classids
parser = argparse.ArgumentParser()
parser.add_argument('-w', '--weights',
    type=str,
    default='/home/psmtx/Desktop/final/yolov3.weights',
    help='Path to the file which contains the weights \
            for YOLOv3.')
parser.add_argument('-cfg', '--config',
    type=str,
    default='/home/psmtx/Desktop/final/yolov3.cfg',
    help='Path to the configuration file for the YOLOv3 model.')

parser.add_argument('-v', '--video-path',
    type=str,
    default="/home/psmtx/Desktop/final/im1.jpg",#'/home/psmtx/Desktop/final/t2.mp4',
    help='The path to the video file')

parser.add_argument('-l', '--labels',
    type=str,
    default='/home/psmtx/Desktop/final/coco1',
    help='Path to the file having the \
                labels in a new-line seperated way.')

parser.add_argument('-c', '--confidence',
    type=float,
    default=0.5,
    help='The model will reject boundaries which has a \
            probabiity less than the confidence value. \
            default: 0.5')

parser.add_argument('-th', '--threshold',
    type=float,
    default=0.3,
    help='The threshold to use when applying the \
            Non-Max Suppresion')

frameWidth = 640    #Frame Width
frameHeight = 480   # Frame Height

plateCascade = cv2.CascadeClassifier("/home/psmtx/Desktop/final/haarcascade_russian_plate_number.xml")
minArea = 500

cap =cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150)

while True:

    success , img  = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)
    cv2.imwrite("/home/psmtx/Desktop/final/im1.jpg",img)
    print("IMAGE CAPTURED")
    FLAGS, unparsed = parser.parse_known_args()
	# Get the labels
    labels = open(FLAGS.labels).read().strip().split('\n')
	# Load the weights and configutation to form the pretrained YOLOv3 model
    net = cv2.dnn.readNetFromDarknet(FLAGS.config, FLAGS.weights)
	# Get the output layer names of the model
    layer_names = net.getLayerNames()
    layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    if not success:
        break
    # Contructing a blob from the input image
    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416),
                    swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(layer_names)
    #objt= infer_image(net, layer_names, frameHeight,frameWidth, img, labels,FLAGS)
    boxes, confidences, classids = generate_boxes_confidences_classids(outs, frameHeight, frameWidth, FLAGS.confidence)
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, FLAGS.confidence, FLAGS.threshold)
    if len(idxs) > 0:
        for i in idxs.flatten():
            text = "{}: {:4f}".format(labels[classids[i]], confidences[i])
            print(text)
            a = "obj"+str(text)
            conn = sqlite3.connect('tx.sqlite')
            cur = conn.cursor()
            cur.execute('''SELECT ind FROM obj ''')
            row=cur.fetchall()
            cur.execute('''INSERT OR IGNORE INTO obj(detected) VALUES(?)''',(a,))
            cur.close()


    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img,"NumberPlate",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            imgRoi = img[y:y+h,x:x+w]
            cv2.imwrite("/home/psmtx/Desktop/final/pl.jpg",imgRoi)
            #pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
            try:
                text = pytesseract.image_to_string("/home/psmtx/Desktop/final/pl.jpg")
                text = text.split('\n')
                for i in text:
                    for j in i:
                        if(j==' '):
                            break
                    if (len(i)==10 and i[0:2].isalpha() and i[2:4].isdigit() and i[4:6].isalpha() and i[6:10].isdigit()):
                        print(i)
                        a = "npl"+str(i)
                        conn = sqlite3.connect('tx.sqlite')
                        cur = conn.cursor()
                        cur.execute('''SELECT ind FROM obj ''')
                        row=cur.fetchall()
                        cur.execute('''INSERT OR IGNORE INTO obj(detected) VALUES(?)''',(a,))
                        cur.close()
            except:
                print('Error')
    conn.commit()
