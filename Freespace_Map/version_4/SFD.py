# calculates the semantic floor depth (SFD) map

import numpy as np
from skimage import data, draw
import matplotlib
import matplotlib.pyplot as plt 
import cv2 
import math
from myconfig import *
import function
import os


# creates the semantic floor depth (SFD) map of an image
# image is the imput image
# depth is the depth map
# rgb is the floor vs non-floor segmentation
def get_sfd(img_name,output_folder):

    if not os.path.isdir("GUI/SFD/" + output_folder):
        os.mkdir("GUI/SFD/" + output_folder)
    if not os.path.isdir("GUI/ASFDS/" + output_folder):
        os.mkdir("GUI/ASFDS/" + output_folder)
    if not os.path.isdir("GUI/output/" + output_folder):
        os.mkdir("GUI/output/" + output_folder)
    # image = cv2.imread("image/"+img_name+'.png')
   
    image = cv2.imread("../../input/" + img_name )
    depth = cv2.imread("../../Revisiting_Single_Depth_Estimation/GUI/" + output_folder + "/" + img_name )
    # rgb = cv2.imread("../../../../semantic-segmentation-pytorch/GUI/" + img_name + ".png")
    rgb = cv2.imread("../../semantic-segmentation-pytorch/GUI/" + output_folder + "/" + img_name,cv2.IMREAD_GRAYSCALE)
    # rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    depth_inv = cv2.bitwise_not(depth)
    depth_inv_grey = cv2.cvtColor(depth_inv, cv2.COLOR_BGR2GRAY)
    #cv2.imwrite("SFD/"+img_name+"_depth_inv_grey.png", depth_inv_grey)
    # plt.imshow(rgb)
    # plt.show()



    '''
    ####Mask for RED color########
    # makes all nonfloor pixels 0 and floor 1
    hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
    lower_range = np.array([0,50,50])
    upper_range = np.array([10,255,255])
    mask = cv2.inRange(hsv, lower_range, upper_range)
    cv2.imwrite("SFD/"+img_name+"_mask.png", mask)
    '''
    # comment if seg is red and blue
    mask = 255 - rgb
    
    # Uncomment if segmentation is red and blue
    # mask = np.zeros((rgb.shape[0],rgb.shape[1]))
    # for i in range(rgb.shape[0]):
    #     for j in range(rgb.shape[1]):
    #         if(rgb[i,j,0] > rgb[i,j,2]):
    #             mask[i,j] = 0
    #         else:
    #             mask[i,j] = 1
    
    
    # sfd_map is floor*inverted depth map
    sfd_map = depth_inv_grey.copy()
    sfd_map[mask == 0] = 0
    # plt.imshow(sfd_map)
    # plt.show()
    # print(np.unique(mask))
    sfd_map[mask != 0] = depth_inv_grey[mask != 0]
    '''
    for x in range(0,image.shape[0]):
        for y in range(0,image.shape[1]):
            print(mask[x,y])
            p2 = mask[x,y]
            if(p2.all()==0):  # if nonfloor pixels then sfd at that pixel will be 0   
        	    sfd_map[x,y] = 0  
    '''   	
    cv2.imwrite("GUI/SFD/"+ output_folder + "/" + img_name,sfd_map)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()	




