import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
import os
import numpy as np
import cv2
from PIL import Image
import pickle

def authorize():
    auth_manager = SpotifyClientCredentials(client_id='a112aa48ef534bbcafb9baba352d9f67', client_secret='b86043b0686f454b9f53e70e6ba72e7e')
    sp = spotipy.Spotify(auth_manager=auth_manager)
    pass

def play_song(url):
    webbrowser.open(url)

def close_browser():
    os.system("killall -9 'Google Chrome'")

def trainner():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, "images")

    face_cascade = cv2.CascadeClassifier('/usr/local/lib/python3.8/site-packages/cv2/data/haarcascades/haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    label_ids = {}
    x_train = []
    y_labels = []
    #goes through image directory and gets a label for each image
    for root,dirs,files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                path = os.path.join(root,file)
                label = os.path.basename(os.path.dirname(path)).replace(" ","-").lower()

                #give people folders unique label
                if label not in label_ids:
                    label_ids[label] = current_id
                    current_id += 1

                id_ = label_ids[label]

                pil_image = Image.open(path).convert("L") # "L" converts to gray
                size = (550,550)
                final_image = pil_image.resize(size, Image.ANTIALIAS)

                image_array = np.array(final_image, "uint8")
                faces = face_cascade.detectMultiScale(image_array, scaleFactor = 1.5, minNeighbors=5)

                for (x,y,w,h) in faces:
                    roi = image_array[y:y+h, x:x+w]
                    x_train.append(roi)
                    y_labels.append(id_)

    #Save labels
    with open("labels.pickle", 'wb') as f:
        pickle.dump(label_ids, f)

    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("trainner.yml")
