import time
#start_time = time.time()
import numpy as np
from skimage import data, draw
import matplotlib.pyplot as plt 
import cv2 
import math
from myconfig import *
import os
import ASFDS
import function
import SFD
import csv
# import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--output_folder",
    required=True,
    type=str,
    help="output folder"
)
args = parser.parse_args()
# print(args.output_folder) 

#to run for a single image
'''
image_name = sys.argv[1]
print("argym",image_name)#"ADE_val_00000198"
SFD.get_sfd(image_name)
ASFDS.get_asfds(image_name)
'''
#to run for a bulk of image and get accuracy

image_arr = []
image_name =[]
i = 0
# print(os.listdir("../../../../GUI/input/"))
for file in os.listdir("../../input/"): 
    #takes all png files from (.png)image folder
    #if file.endswith(".png") and i < no_of_samples:
    image_arr.append("../../input/"+file)
    # print("../../../../GUI/input/"+file)
    #image_name.append(file.replace('.png', ''))
    image_name.append(file)
    i=i+1
# print("xscdsc",image_arr)
# rows=[]
# row=[]
# start_time = time.time()
# accuracy = 0
# acc = 0
# row.append("Name")
# row.append("GT")
# row.append("Direction")
# rows.append(row)
no_of_samples = i
for i in range(0,no_of_samples): 
    #runs to get direction on samples
	#print(i,image_name[i])
    #row=[]
    # print(args.output_folder)
    SFD.get_sfd(image_name[i],args.output_folder)
    ASFDS.get_asfds(image_name[i],args.output_folder)
    #direction, gt, acc = ASFDS.get_asfds(image_name[i])
    
    #accuracy = accuracy + acc
    #row.append(image_name[i])
    #row.append(gt)
    #row.append(round(direction))
    #rows.append(row)

#print("accuracy for " + str(no_of_samples)+ " samples is "+ str(accuracy/no_of_samples))
#print("--- %s seconds ---" % (time.time() - start_time))

#with open('output.csv', 'w', newline='') as file:
    #writer = csv.writer(file)
    #writer.writerows(rows)
