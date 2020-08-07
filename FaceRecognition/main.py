# import the necessary packages
import numpy as np
import cv2
import pickle
import utils
import time
import os

utils.authorize()


face_cascade = cv2.CascadeClassifier('/usr/local/lib/python3.8/site-packages/cv2/data/haarcascades/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
to_train = input("Do you want to train your dataset [Y/n]:")
if to_train.lower() == 'y':
    utils.trainner()
else:
    if not os.path.exists("trainner.yml"):
        print("Training anyway")
        utils.trainner()
    else:
        pass

recognizer.read("trainner.yml")

temp_label  =  0
labels = {}
song_list = ['https://p.scdn.co/mp3-preview/8226164717312bc411f8635580562d67e191a754?cid=a112aa48ef534bbcafb9baba352d9f67',
            'https://p.scdn.co/mp3-preview/50e82c99c20ffa4223e82250605bbd8500cb3928?cid=a112aa48ef534bbcafb9baba352d9f67']
#Set label value to person name and to number
with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

if face_cascade.empty():
    raise Exception("your cascade is empty. are you sure, the path is correct ?")
# open webcam video stream
cap = cv2.VideoCapture(0)



while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # resizing for faster detection
    frame = cv2.resize(frame, (640, 480))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    #detect faces while camera is open (use frame increase scale factor for better results)
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors=5)
    #When face is seen create and image of it
    for (x,y,w,h) in faces:
        #region that we will use to recognize face
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        #recognize face through deep learning model
        id_, conf = recognizer.predict(roi_gray)
        if conf>= 45:
            # print(id_)
            # print(labels[id_])

            #Fix
            if temp_label == labels[id_]:
                print(time.time() -  start)
                if time.time() - start > 15:
                    utils.close_browser()
                pass
            else:
                if labels[id_] == "other":
                    utils.play_song(song_list[0])
                else:
                    utils.play_song(song_list[1])
                temp_label = labels[id_]
                start = time.time()


            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255,255,255)
            stroke = 2
            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

        #prints out image of recognized face
        # img_item = "5.png"
        # cv2.imwrite(img_item, roi_color)

        color  = (255, 0 , 0 ) #BGR
        stroke = 2
        cv2.rectangle(frame, (x,y),(x+w,y+h), color, stroke)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)
