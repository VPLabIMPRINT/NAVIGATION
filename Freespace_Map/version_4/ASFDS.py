#creates the angular SFD sectors (ASFDS) profile
import numpy as np
from skimage import data, draw
import matplotlib.pyplot as plt 
import cv2 
import math
from myconfig import *
import function

# creates the angular SFD sectors (ASFDS) profile
# image is the input image
# mask is the sfd map
def get_asfds(img_name,output_folder):
    
    
    image = cv2.imread("../../input/" + img_name )
    mask = cv2.imread("GUI/SFD/"+ output_folder + "/" + img_name)
    mask_grey = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    r0 = image.shape[0]
    w0 = image.shape[1]
    c0 = image.shape[1]/2
    R = r0*1.414
    x,theta_range = function.get_interval()
    regions = 2*K-1
    theta0 = np.deg2rad(0)  
    theta1 = np.deg2rad(theta_range[1]) 
    region_pixels_sum = []
    
    for region in range(0,regions):
        theta0 = np.deg2rad(theta_range[region])  
        theta1 = np.deg2rad(theta_range[region+1]) 
        r1, c1 = r0 - 1.5 * R * np.sin(theta0), c0 + 1.5 * R * np.cos(theta0)
        r2, c2 = r0 - 1.5 * R * np.sin(theta1), c0 + 1.5 * R * np.cos(theta1)
        mask_poly = np.zeros(image.shape[:2], dtype=np.uint8)
        rr, cc = draw.polygon([r0, r1, r2, r0],[c0, c1, c2, c0], shape=mask_poly.shape)
        mask_poly[rr, cc] = 1
        sect_seg = mask_grey.copy()
        sect_seg[mask_poly == 0] = 0
        sect_seg[mask_poly != 0] = mask_grey[mask_poly != 0]
        pi_count = np.count_nonzero(sect_seg != 0)
        s = np.sum(sect_seg)
        region_pixels_sum.append(s)
        #region_pixels_sum.append(s/pi_count)
        #cv2.imwrite("SFD/"+img_name+"_sector_mask_"+str(regions-region+1)+".png", sect_seg)
        #Uncomment below to see the sectors creation in image
        #sect_img = image.copy()
        #sect_img[mask_poly == 0] = 0
        #sect_img[mask_poly != 0] = image[mask_poly != 0]
        #cv2.imwrite("SFD/"+img_name+"_sector_image_"+str(regions - region)+".png", sect_img)
    region_pixels_sum.reverse()
    y = region_pixels_sum
    sec_diff=[]
    for i in range(0,len(theta_range)-1):
        sec_diff.append(theta_range[i+1]- theta_range[i])
    reslt_min = np.where(sec_diff == np.amin(sec_diff))
    reslt_max = np.where(sec_diff == np.amax(sec_diff))
    min_index = int(reslt_min[0][0])
    max_index = int(reslt_max[0][0])
    sec_angle = int((sec_diff[min_index]+sec_diff[max_index])/2)
    gt = function.get_GT(img_name)  #gets GT
    direction = function.closed_form(y,x,sec_angle) #gets the predicted direction
    #error = function.get_error(direction,gt) #gets the error b/w GT and predicted 
    #accuracy = function.get_accuracy(error) #gets the accuracy
    # function.plot_dir_gt(direction,gt,img_name,'GUI/output/' + output_folder) #plots gt and direction vector on image
    #function.plot_dir(direction, img_name, 'ASFDS')
    #y = function.normalise_arr(y)
    #np.save('ASFDS/'+img_name+'_asfds_x', x)
    #np.save('ASFDS/'+img_name+'_asfds_y', y)
    # plots the AFSDS bar chart
    y_pos = np.arange(len(x))
    plt.bar(y_pos,y,align='center')
    plt.xticks(y_pos, x)
    plt.title("Angular SFD Sectors")
    plt.xlabel('Angles')
    plt.ylabel('Pixels Sum (Normalized)')
    plt.savefig("GUI/ASFDS/"+ output_folder + "/" + img_name)
    plt.close()

    function.plot_dir_gt(direction,gt,img_name,'GUI/output/' + output_folder)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #return direction
    #return accuracy
    #return direction, gt, accuracy
	
	
	