# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 20:22:49 2018

@author: jmidv
"""
import os
import temp
import shutil

def makeLeftAndRightDirs(path):
    folders = os.listdir(path)
    for folder in folders:
        curr_path = path + "/" + folder + "/"
        files = os.listdir(curr_path)
        left, right = temp.getLeftAndRightEyes(path, folder)
        
        if len(right) < 2:
            print("error")
        
        left_images = []
        right_images = []
        for elem in left:
            if len(left_images) >= 6:
                break
            else:
                if elem in files:
                    left_images.append(elem)
                    left_images.append(elem + "-polar.jpg")
                    left_images.append(elem + "-polarnoise.jpg")
        for elem in right:
            if len(right_images) >= 6:
                break
            else:
                if elem in files:
                    right_images.append(elem)
                    right_images.append(elem + "-polar.jpg")
                    right_images.append(elem + "-polarnoise.jpg")
        
        # make left and right eyes directory
        shutil.rmtree(curr_path + "left_eyes")
        shutil.rmtree(curr_path + "right_eyes")
        
        
        
        try:
            os.mkdir(curr_path + "left_eyes")
        except:
            pass
        try:
            os.mkdir(curr_path + "right_eyes")
        except:
            pass
        try:    
            for elem in left_images:
                shutil.copy(curr_path + elem, curr_path + "left_eyes/")
            for elem in right_images:
                shutil.copy(curr_path + elem, curr_path + "right_eyes/")
        except:
            pass

    return



def checkFolders(path):
    files = os.listdir(path)
    for file in files:
        curr_path = path + "/" + file + "/"
        left_eyes = os.listdir(curr_path + "left_eyes/")
        right_eyes = os.listdir(curr_path + "right_eyes/")
        left, right = temp.getLeftAndRightEyes(path, file)
        
        good_left = list(set(left) - set(left_eyes))
        good_right = list(set(right) - set(right_eyes))
        
        
        if len(left_eyes) < 2:
            diff = 2 - len(left_eyes)
            if diff == 1:
                shutil.copy(curr_path + good_left[0], curr_path + "left_eyes/")
            print("error left", "diff", diff)
        if len(right_eyes) < 2:
            diff = 2 - len(right_eyes)
            if diff == 1:
                shutil.copy(curr_path + good_right[0], curr_path + "right_eyes/")
            print("error right", "diff", diff)
        
        
        
    
    
    
    return



def main(path):
    
    checkFolders(path)
    
    #makeLeftAndRightDirs(path)    
    return

if __name__ == "__main__":
    root1 = 'C:/Users/jmidv/Documents/Fall 2018/EECS 395 - Biometrics/Assignments/HW2/Iris/LG2200-2008-03-11_13/2008-03-11_13'
    # testing
    root2 = "C:/Users/jmidv/Documents/Fall 2018/EECS 395 - Biometrics/Assignments/HW2/Iris/LG2200-2010-04-27_29/2010-04-27_29"
    root3 = "C:/Users/jmidv/Documents/Fall 2018/EECS 395 - Biometrics/Assignments/HW2/Iris/LG4000-2010-04-27_29/2010-04-27_29"
    
    root4 = "C:/Users/jmidv/Documents/Fall 2018/EECS 395 - Biometrics/Assignments/HW2/unused/middle"
    
    main(root2)