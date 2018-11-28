# -*- coding: utf-8 -*-
"""
EECS 395: Biometrics, Fall 2018
Assignment 3: Facial Recognition System 

@author: Jeremy Midvidy, jam658
@about: A Facial Recognition system implemented in Python 3.7 and OpenCV.
"""

import cv2
from PIL import Image
import os
import numpy as np
import matplotlib.image as mpimg
import pickle

def main(image_folder_path):

    # ----------------------- Choose CV2 classifier tools --------------------- #
    
    # used for feature extraction
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    
    # used for classification
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir, image_folder_path)
    
    x_train = []
    y_labels = []
    label_ids = {}
    current_id = 0
    
    # ----------------------- ITERATE THROUGH DATABASE AND GATHER FACES ------------------------ #
    count = 0
    train_folders = os.listdir(image_dir)    
    for folder in train_folders:
        curr_path = image_dir + "\\" + folder + "\\"
        images = os.listdir(curr_path)
        for image in images:
            image_path = curr_path + "\\" + image
            label = folder
            # EXTRACT current facial features from the GIVEN current image
            A = mpimg.imread(image_path)
            img = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)

            # detect faces in the current image
            faces = face_cascade.detectMultiScale(img, 1.5, 5)
            #print(faces)
            fc = 0
            for (x,y,w,h) in faces:
                if fc == 1:
                    break
                # draw a rectangle
                color = (255, 0, 0) # BGR 0 -255
                stroke = 2
                end_cord_x = x + w
                end_cord_y = y + h
                
                # write the RECTANGLE on the INPUT image for creating the database
                cv2.rectangle(img, (x,y), (end_cord_x, end_cord_y), color, stroke)
                cv2.imwrite("results/img" + str(count) + ".png", img)
                
                # create the REGION OF INTEREST for each face
                roi = img[y:y+h, x:x+h]
                x_train.append(roi)
                if label not in label_ids:
                    label_ids[label] = current_id
                    current_id += 1
                this_id = label_ids[label]
                y_labels.append(this_id)
                
                fc += 1
                                
        
            # debugging for now
            if count == -1:
                return
            
            count += 1
            
            
#    print(x_train)
#    print(y_labels) 
#    print(label_ids)

    
    # -------------------------- TRAINING CLASSIFIER FROM GATHERED DATA ------------------- #
    with open("labels.pickle", "wb") as f:
        pickle.dump(label_ids, f)
        
    # train the openCV recognizer
    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("trainner.yml")
    
    return label_ids
    

if __name__ == "__main__":
    main("images1\\train")












            
