

 # -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 17:15:39 2018

@author: jmidv
"""

import os
import numpy as np
import matplotlib.image as mpimg
import cv2
import csv

# Given a list of ids, return a dict
# Indicating whether given ID is a 
# Left or right eye
def extractText(path):
    ids = []
    curr_id = ""
    F = open(path, 'r')
    for line in F:
        line = line.split('\t')
        #print(line)
        if line[0] == 'id':
            ids.append(line[2].strip())
    cache = {}
    for elem in ids:
        cache[elem] = {}
    curr_id = ids[0]
    count = -1
    F = open(path, 'r')
    for line in F:
        if len(line) < 3:
            continue
        line = line.split('\t')
        if line[0] == 'id':
            count += 1
            curr_id = ids[count]
            continue
        cache[curr_id][line[0]] = line[2].strip()
    out = {}
    for key in cache:
        try:
            seqID = cache[key]['sequenceid']
            out[seqID + ".tiff"] = cache[key]['eye']
        except:
            continue
    return out

# given an folder containing iris images
# return the left and right iris images 
def getLeftAndRightEyes(path, curr_num):
    files = os.listdir(path + "/" + curr_num)
    
    # get Left or Right eye for all the files in the current directory
    eyes = extractText(path + "/" + curr_num + "/" + curr_num + ".txt")
    
    # get list of .tiff images from working directory
    images = []
    for file in files:
        if ".tiff" == file[len(file)-5:]:
            images.append(file)
    
    if len(images) > 2:
        images = images[:2]        
    
    # get Left and Right images
    left = []
    right = []
    for elem in images:
        # check to see if nosie in images to be sure
        try:
            #if (elem + "-noise.jpg") in files:
                if eyes[elem] == 'Left':
                    left.append(elem)
                else:
                    right.append(elem)
        except:
            continue
    return left, right

#------------------------------------------------------------------------------
def calHammingDist(template1, mask1, template2, mask2):
    hd = np.nan
    

    # Shift template left and right, use the lowest Hamming distance
    for shifts in range(-8,8):
        template1s = shiftbits(template1, shifts)
        mask1s = shiftbits(mask1, shifts)

        mask = np.logical_or(mask1s, mask2)
        nummaskbits = np.sum(mask == 1)
        totalbits = template1s.size - nummaskbits

        C = np.logical_xor(template1s, template2)
        C = np.logical_and(C, np.logical_not(mask))
        bitsdiff = np.sum(C==1)

        if totalbits==0:
            hd = np.nan
        else:
            hd1 = bitsdiff / totalbits
            if hd1 < hd or np.isnan(hd):
                hd = hd1

	# Return
    return hd


#------------------------------------------------------------------------------
def shiftbits(template, noshifts):
	# Initialize
	templatenew = np.zeros(template.shape)
	width = template.shape[1]
	s = 2 * np.abs(noshifts)
	p = width - s

	# Shift
	if noshifts == 0:
		templatenew = template

	elif noshifts < 0:
		x = np.arange(p)
		templatenew[:, x] = template[:, s + x]
		x = np.arange(p, width)
		templatenew[:, x] = template[:, x - p]

	else:
		x = np.arange(s, width)
		templatenew[:, x] = template[:, x - s]
		x = np.arange(s)
		templatenew[:, x] = template[:, p + x]

	# Return
	return templatenew

def processArray(mask):
    A = []
    mask = mask.tolist()
    for row in mask:
        curr = []
        for col in row:
            if col == 0:
                curr.append(0)
            else:
                curr.append(1)
        A.append(curr)
    return np.array(A)

def classifyFolders(f1, f2):
        
    distances = []
    # f1 as 2 images: [AB]
    # f2 as 2 images: [CD]
    # get HD for [AC, AD, BC, BD]
    images = os.listdir(f1)
    f1_ids = []
    for row in images:
        if "-" not in row:
            f1_ids.append(row)
    images = os.listdir(f2)
    f2_ids = []
    for row in images:
        if "-" not in row:
            f2_ids.append(row)
         
    for elem in f1_ids:
        p1 = f1 + elem + "-polar.jpg"
        m1 = f1 + elem + "-polarnoise.jpg"
        
        p1 = mpimg.imread(p1)
        m1 = mpimg.imread(m1)
        
            
        threshi, p1_bw = cv2.threshold(p1, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        threshi, m1_bw = cv2.threshold(m1, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        p1_bw = processArray(p1_bw)
        m1_bw = processArray(m1_bw)
        
        for word in f2_ids:
            p2 = f2 + word + "-polar.jpg"
            m2 = f2 + word + "-polarnoise.jpg"
            
            m2 = mpimg.imread(m2)
            p2 = mpimg.imread(p2)
                        
            threshi, m2_bw = cv2.threshold(m2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            threshi, p2_bw = cv2.threshold(p2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            
            m2_bw = processArray(m2_bw)
            p2_bw = processArray(p2_bw)
            
            
            
            hd = calHammingDist(p1_bw, m1_bw, p2_bw, m2_bw)
            
            
            distances.append(hd)
            
    #print(distances)
            
    # make classification
    return min(distances)
    



def test(train, test):
    
    test_files = os.listdir(test)
    train_files = os.listdir(train) 
    
    test_files = test_files
    train_files = train_files
    
    # make trues and falses for two folders:
    trues = []
    falses = []
    for elem in test_files:
        if elem in train_files:
            trues.append(elem)
        else:
            falses.append(elem)
    
    el = 0
    er = 0
    ert = 0
    out = {}
    list_out = []
    tt_train_files = ["DownTest/RightTrain"]
    tt_train_files.extend(train_files)
    list_out.append(tt_train_files)
    # each folder has 2 LEFTS and 2 RIGHTS
    # for each LEFT and RIGHT folder
    # see if either image is in the database of Lefts or Rights
    t1 = 0
    
    print("---------------------------------------------------")
    print("--------------------- TESTING ---------------------")
    print("---------------------------------------------------")
    
    for test_folder in test_files:
        t1 += 1
        # paths for folders containing testing L and R images
        test_left = test + "/" + test_folder +"/left_eyes/"
        test_right = test + "/" + test_folder + "/right_eyes/"
        done = [False]
        
        print("\t\t Testing: " + test_folder + " (" + str(t1) + "/" + str(len(test_files)) +  ")")
        
        curr = [test_folder]
        
        prev = ""
        t2 = 0
        for train_folder in train_files:
            t2 += 1

            train_left = train + "/" + train_folder +"/left_eyes/"
            train_right = train + "/" + train_folder + "/right_eyes/"
            
            # error when classifying
            
            try:
                left_hd  = classifyFolders(test_left, train_left)
            except:
                print("error left")
                el += 1
                left_hd = 100
            
            try:
                right_hd = classifyFolders(test_right, train_right)
            except:
                print("error right")
                er += 1
                right_hd = 100
            
            
            if left_hd == 100 and right_hd == 100:
                hd = -3 # error during processing
                ert += 1
            else:
                hd = min(left_hd, right_hd)
                hd = round(hd, 4)
                
                if np.isnan(hd):
                    hd = -2
                    # -2 for nan
                    
            
                # -1 implies overfit result
                if hd == 0.0:
                    hd = -1
                
            curr.append(hd)
            
            #print(test_folder, train_folder, hd, "(" + str(t2) + "/" + str(len(train_files)) + ")")
                
        out[test_folder] = curr
        list_out.append(curr)
        
        
    # -- find error threshold -- #
    thresh = []
    nums = list_out[0]
    #print(nums)
    for row in list_out[1:]:
        #print(row)
        if row[0] in nums:
            ind = nums.index(row[0])
         #   print(row[0], "in nums at", ind, "appending", row[ind])
            thresh.append(row[ind])
            
    thresh_clean = []
    for elem in thresh:
        if elem > 0:
            thresh_clean.append(elem)
            
    thresh_val = sum(thresh_clean) / len(thresh_clean)
            
    print(thresh_clean)
    print(thresh_val)
    
    print("--------------------------------------------")
    print("---------------- ANALYZING -----------------")
    print("--------------------------------------------")
    
    
    # now have threshold, need to find false reject/false accept rate
    
    false_reject = 0 # rejects a claim that is a true claim
    false_accept = 0 # accepts a claim that is a false claim
    true_accept = 0  # accepts a claim that is a true claim
    true_reject = 0  # rejects a claim that is a false claim
    
    inds = {}
    kk = 0
    for elem in nums[1:]:
        inds[kk] = elem
        kk += 1
        
    #print(inds)
    
    #print(list_out)
    
    for row in list_out[1:]:
        for i in range(1, len(row)):
            accept = False
            curr = row[i]
            if curr < thresh_val and curr > 0:
                accept = True
                
            if accept == True:
                # a true claim is accepted
                if row[0] == inds[i-1]:
                    print("\ttrue_accept", "(", row[0], inds[i-1], ")", "val", curr)
                    true_accept += 1
                # a false claim is accepted
                else:
                    print("\tfalse accept!", "(", row[0], inds[i-1], ")", "val", curr)
                    false_accept += 1
            else:
                # a true claim is rejected
                if row[0] == inds[i-1]:
                    false_reject += 1
                # a false claim is rejected
                else:
                    true_reject += 1
                
    print("\n")
    print("\tthreshold:", thresh_val)
    print(thresh_clean)
    print("\tfalse reject:", false_reject)
    print("\tfalse accept:", false_accept)
    print("\ttrue accept:", true_accept)
    print("\ttrue reject:", true_reject)
    print("\tnum actual true:", len(trues))
    
    
        

    
    
    
        
    #print("left errors:", el)
    #print("right errors:", er)
    #print("total -3 errors", ert)
        
    with open("test2_results.csv","w+") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(list_out)
    
    return

def main(train, test1, test2):
    
    #print("Testing Classifier on test1:")
    
    #test(train, test1)
    test(train, test2)
    
    
    return

if __name__ == "__main__":
    # training
    root1 = 'C:/Users/jmidv/Documents/Fall 2018/EECS 395 - Biometrics/Assignments/HW2/Iris/LG2200-2008-03-11_13/2008-03-11_13'
    
    # testing
    root2 = "C:/Users/jmidv/Documents/Fall 2018/EECS 395 - Biometrics/Assignments/HW2/Iris/LG2200-2010-04-27_29/2010-04-27_29"
    root3 = "C:/Users/jmidv/Documents/Fall 2018/EECS 395 - Biometrics/Assignments/HW2/Iris/LG4000-2010-04-27_29/2010-04-27_29"
    main(root1, root2, root3)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    