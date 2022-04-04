# contains various functions to support freespace profile creation

import numpy as np
from skimage import data, draw
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt 
import cv2 
import math
from myconfig import *
import csv
import math
# returns the accuracy
def get_accuracy(error):  
	ee = abs(float(1)-error)
	accuracy = (ee*100)
	return accuracy

# divides the x axis into regular interval
def get_interval():
	theta_k = abs(range_1)
	tan_theta = math.tan(theta_k * (np.pi/180))

	den = 2*K-1
	interval_range = []
	interval_range_temp = []
	for i in range(1,K+1):
			num = (2*i -1)*tan_theta
			temp = num/den
			interval_range_temp.append(round(math.atan(temp)*(180/np.pi)*2))

	interval_range_temp.reverse()
	for i in range(0,len(interval_range_temp)):
		interval_range.append(-1*interval_range_temp[i])
	interval_range_temp.reverse()
	for i in range(0,len(interval_range_temp)):
		interval_range.append(interval_range_temp[i])		

		
	theta_range  = []
	theta_range.append(0)
	x = []
	strt = 0
	#theta_range =    [0,   11.4, 25, 41,  59.4, 79.6, 100.4, 120.6, 139, 155, 168.6, 180]	
	for i in range(1,len(interval_range)):
		if(interval_range[i-1]*interval_range[i] > 0):
			diff = abs(abs(interval_range[i])-abs(interval_range[i-1]))
		else:
			diff = abs(abs(interval_range[i])+abs(interval_range[i-1]))
		theta_range.append(round(strt+diff))
		strt = strt+diff;

	for i in range(0,len(interval_range)-1):
		x.append(int((interval_range[i]+interval_range[i+1])/2))

	return x, theta_range

	

# returns the ground truth of image from GT.csv file
def get_GT(img_name):
	with open('GT.csv', 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			if(row[0] == img_name):
			    print(row[1])
			    print(float(row[1]))
			    return float(row[1])
	return -1

# returns the normalized array
def normalise_arr(y):
	amin, amax = min(y), max(y)
	for index, val in enumerate(y):
		y[index] = (val-amin) / (amax-amin)
	return y


# returns the direction using closed form solution
# x is the array containing angles
# y is value of ASFDS at each angle
def closed_form(y,x,sec_angle):
	if np.max(y) < 100:
	    return -200
	y = normalise_arr(y)
	result = np.where(y == np.amax(y))
	max_index = int(result[0][0])
	calangle = (x[max_index])
	#print(x[max_index]," at ", y[max_index])
	if(max_index == 0 or max_index == len(x)-1): #if peak occurs at the boundary
		return calangle
	else:
		efsp_b = y[max_index-1] #before peak
		efsp_p = y[max_index]	#at peak
		efsp_a = y[max_index+1]	#after peak
		num = (efsp_b - efsp_a)*sec_angle
		dem = 2*(efsp_b - 2*efsp_p + efsp_a)		
		direction = calangle+(num/dem)		
		return direction
		

# returns the error 
# y_gt is the ground truth value
# y_predict is the predicted direction
def get_error(y_predict,y_gt):
	#print("pppp",y_gt,y_predict)
	if((y_gt*y_predict) > 0):
		theta = abs(y_gt - y_predict)
		theta_a = abs(y_gt + y_predict)/2
		err = theta/theta_a
		#print(err)
		return err
	elif((y_gt*y_predict) < 0):
		theta = abs(y_gt - y_predict)
		err = theta/(abs(range_1)+range_2)
		return err
	else:
		return 0

def linedashed(image,x0, y0, x1, y1,color, dashlen=4, ratio=5): 
    # image = Image.open('../../../../GUI/input/'+image)
    # draw = ImageDraw.Draw(image)
    if color == "blue":
        fill = (255,0,0)
    elif color == "red":
        fill = (0,0,255)
    else:
        fill = (0,255,0)
    dx=x1-x0 
    dy=y1-y0 
    if dy==0: len=dx
    elif dx==0: len=dy
    else: len=math.sqrt(dx*dx+dy*dy) 
    xa=dx/len 
    ya=dy/len 
    step=dashlen*ratio 
    a0=0
    while a0<len:
        a1=a0+dashlen
        if a1>len: a1=len
        cv2.line(image,(int(x0+xa*a0), int(y0+ya*a0)), (int(x0+xa*a1), int(y0+ya*a1)), fill,4)
        a0+=step
    return image    
# plots the gt direction and predicted direction on image
# direction is the predicted direction
# gt is the ground truth direction
# path_to_save is the location to save the reslt image after plotting
# the resultant image will be image_name_reslt.png

def plot_dir_gt(direction,gt,img_name,path_to_save): ###############################
	
	direction = round(direction)
	ang_orig = direction
	direction = -1*direction
	direction = 90-direction
	arrow_angle = direction * (np.pi/180)
	c = math.cos(arrow_angle)
	s = math.sin(arrow_angle)
	gt_orig = gt
	if gt < 0:
	    gt = 90 - abs(gt)
	else:
	    gt = 90 + gt
	
	arrow_angle1 = gt * (np.pi/180)
	
	c1 = math.cos(arrow_angle1)
	s1 = math.sin(arrow_angle1)
	rgb = cv2.imread('../../input/'+img_name)

	if gt_orig != -1:
	    x0 = int(rgb.shape[1]/2 + c1 * 100)
	    y0 = int(rgb.shape[0]  + s1 * 100)
	    x1 = int(rgb.shape[1]/2 - c1 * 350)
	    y1 = int(rgb.shape[0] - s1 *350)
	    cv2.arrowedLine(rgb,(x0,y0),(x1,y1),(0,255,0), 4) 
	    x0 = rgb.shape[1]/2 + c1 * 1000
	    y0 = rgb.shape[0]  + s1 * 1000
	    x1 = rgb.shape[1]/2 - c1 * 3500
	    y1 = rgb.shape[0] - s1 * 3500
	    rgb = linedashed(rgb,x0,y0,x1,y1,"green")
	
	if ang_orig != -200:
	    cv2.arrowedLine(rgb, (int(rgb.shape[1]/2 + c * 100), int(rgb.shape[0]  + s * 100)),(int(rgb.shape[1]/2 - c * 350), int(rgb.shape[0] - s * 350)), (255,0,0), 4)
	    rgb = linedashed(rgb, int(rgb.shape[1]/2 + c * 1000), int(rgb.shape[0]  + s * 1000),int(rgb.shape[1]/2 - c * 3500), int(rgb.shape[0] - s * 3500),"blue")
	
	
    
	arrow_angle = 90 * (np.pi/180)
	c = math.cos(arrow_angle)
	s = math.sin(arrow_angle)
	cv2.arrowedLine(rgb, (int(rgb.shape[1]/2 + c * 100), int(rgb.shape[0]  + s * 100)),(int(rgb.shape[1]/2 - c * 150), int(rgb.shape[0] - s * 150)), (0,0,255), 4)
	rgb = linedashed(rgb, int(rgb.shape[1]/2 + c * 1000), int(rgb.shape[0]  + s * 1000),int(rgb.shape[1]/2 - c * 3500), int(rgb.shape[0] - s * 3500),"red")
	title= "Angle for robot movement = {:.2f}".format((ang_orig * 0.215))
	print(img_name,title," and GT is ",gt_orig )
	cv2.putText(rgb,title , (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),2,cv2.LINE_AA)
	cv2.imwrite(path_to_save+'/'+img_name, rgb)
	# cv2.namedWindow('object_detection_result', cv2.WINDOW_NORMAL)
	# cv2.imshow('object_detection_result', rgb)
    
	# # cv2.imshow("freespace",rgb)
	# cv2.waitKey(10)

# plots only the predicted direction on image
# direction is the predicted direction
# path_to_save is the location to save the reslt image after plotting
# the resultant image will be image_name_direction.png
def plot_dir(direction, img_name, path_to_save):
	direction = round(direction)
	ang_orig = direction
	direction = -1*direction
	direction = 90-direction
	arrow_angle = direction * (np.pi/180)
	c = math.cos(arrow_angle)
	s = math.sin(arrow_angle)
	
	rgb = cv2.imread('../../input/'+img_name+'.jpg')
	
	cv2.arrowedLine(rgb, (int(rgb.shape[1]/2 + c * 100), int(rgb.shape[0]  + s * 100)),\
		(int(rgb.shape[1]/2 - c * 380), int(rgb.shape[0] - s * 380)), (0,255,0), 3)

	#cv2.arrowedLine(rgb, (int(rgb.shape[1]/2 + c * 100), int(rgb.shape[0]  + s * 100)),\
	#	(int(rgb.shape[1]/2 - c * 500), int(rgb.shape[0] - s * 500)), (255,0,0), 5)
	arrow_angle = 90 * (np.pi/180)
	c = math.cos(arrow_angle)
	s = math.sin(arrow_angle)
	cv2.arrowedLine(rgb, (int(rgb.shape[1]/2 + c * 100), int(rgb.shape[0]  + s * 100)),\
		(int(rgb.shape[1]/2 - c * 150), int(rgb.shape[0] - s * 150)), (0,0,255), 3)
	title= "Angle for robot movement = {}".format((ang_orig * 0.215))
	print(img_name,title)
	cv2.putText(rgb,title , (10,10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),2,cv2.LINE_AA)
	cv2.imwrite('GUI/output/'+img_name+'.png', rgb)
