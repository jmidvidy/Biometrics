# -*- coding: utf-8 -*-
"""
EECS 395: Biometrics, Fall 2018
Assignment 3: Facial Recognition System 

@author: Jeremy Midvidy, jam658
@about: A Facial Recognition system implemented in Python 3.7 and OpenCV.
"""

import FacesTrain
import cv2
import os
import numpy as np
import matplotlib.image as mpimg

def test(test_dir, label_ids):
    # INIT face_cascade, recognizer, and read_recognizer from trained labels
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainner.yml")
    
    # keep track of FP rates
    true_reject = 0
    true_accept = 0
    false_reject = 0
    false_accept = 0
        
    # ITERATE through test folders and test files
    test_folders = os.listdir(test_dir)
    train_labels = list(label_ids.keys())
    count = 0
    for folder in test_folders:
        curr_path = test_dir + "\\" + folder
        images = os.listdir(curr_path)
        for image in images:
            image_path = curr_path + "\\" + image
            label = folder
            
            # extract current image
            A = mpimg.imread(image_path)
            img = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
            
            # extract ROI
            faces = face_cascade.detectMultiScale(img, 1.5, 5)
            fc = 0
            for (x,y,w,h) in faces:
                if fc == 1:
                    break
                
                # create the REGION OF INTEREST for each face
                roi = img[y:y+h, x:x+h]
                
                # classify based on current ROI
                out_id, conf = recognizer.predict(roi)
                out_label = ""
                for key in label_ids:
                    if label_ids[key] == out_id:
                        out_label = key
                        break
                
                print("-----------------------------------------------------")
                print("\t\t Testing:", label)
                
                in_train = ""
                if label in train_labels:
                    in_train = "Yes"
                else:
                    in_train = "No"

                predict_in_train = ""
                if conf > 5:
                    predict_in_train = "No"
                else:
                    predict_in_train = "Yes"

                print(" Test in Train?                  ", in_train)
                print(" Recognizer thinks test in train?", predict_in_train)
                
                # TRUE REJECT
                if predict_in_train == "No" and in_train == "No":
                    print(" Input Correctly Rejected!")
                    print("  Confidence:", round(conf, 4))
                    true_reject += 1
                    
                
                if predict_in_train == "Yes" and in_train == "Yes":
                    answer = ""
                    if label == out_label:
                        # TRUE ACCEPT
                        answer = "Correct"
                        true_accept += 1
                    else:
                        # FALSE ACCEPT
                        answer = " False "
                        false_accept += 1
                    print("\tClass:", answer)
                    print("\tActual:", label)
                    print("\tPredict:", out_label)
                    print("\tConfidence:", round(conf, 2))
                    
                
                if predict_in_train == "No" and in_train == "Yes":
                    false_reject += 1

                if predict_in_train == "Yes" and in_train == "No":
                    false_accept += 1
                
                
    
    
    print("\n","---Rates!---")
    print(" True Accept:", true_accept)
    print(" True Reject:", true_reject)
    print(" False Accept:", false_accept)
    print(" False Reject", false_reject)
                
                
    return

def main():
    
    # (1) Train the RECOGNIZER with the inputs in the Database in the specified path
    print("Training recognizer on training data!")
    label_ids = FacesTrain.main("images1\\train")
    print("Recognizer is trained!")
        
    # (2) Test inputs from TEST on CLASSIFIER --> see if results are correct
    print("Testing recognizer on testing data!")
    test_path = "images1\\test"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(base_dir, test_path)
    test(test_dir, label_ids)
    
    
    
    
    return

if __name__ == "__main__":
    main()

