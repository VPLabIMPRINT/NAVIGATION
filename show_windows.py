import os
from shutil import copyfile
import cv2
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ['MKL_THREADING_LAYER'] = 'GNU'

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


offsety = 200
offsetmid = 0
offsety2 = 10
folder_name = sys.argv[1].split("/")[-1]

# width_ori = int(sys.argv[9])
# width = (int(sys.argv[9]) - 160) / 3
# offsetx = int((width_ori - width * 3) / 2)
# height = int(width * 9 / 16)
# width = int(width)

width_ori = int(sys.argv[5])
width = (int(sys.argv[5]) - 260) / 2
offsetx = int((width_ori - width * 2) / 2)
height = int(width * 9 / 16)
width = int(width)

# cx = [offsetx,offsetx + width,offsetx + 2*width,offsetx,offsetx + width,offsetx + 2*width]
# cy = [offsety,offsety,offsety,offsety + offsety2 + height,offsety + offsety2 + height,offsety + offsety2 + height]

cx = [offsetx,offsetx + width,offsetx + 2*width]
cy = [offsety,offsety,offsety]


if folder_name == "webcam":
    number_of_frames = 20
    vid = cv2.VideoCapture(0)
else:
    list_of_images = os.listdir(sys.argv[1])
    list_of_images.sort(key=natural_keys)
    # print(list_of_images)
    # list_of_images = sorted(os.listdir(sys.argv[1]))
    number_of_frames = len(list_of_images)

for im in os.listdir("input"):
    os.remove("input/" + im)

for i in range(number_of_frames):
    if folder_name == "webcam":
        ret, frame = vid.read()
        cv2.imwrite("input/" + str(i) + ".jpg",frame)
        file = str(i) + ".jpg"
        
    else:
        file = list_of_images[i]

        copyfile("pipeline/" + folder_name + '/' + file, 'input/' + file)

    if int(sys.argv[2]) == 1:
        os.chdir('semantic-segmentation-pytorch')
        os.system('python3 -u test.py --output_folder {} --imgs ../input/ --gpu 1 --cfg config/GUI_ade20k-mobilenetv2dilated-c1_deepsup.yaml VAL.visualize True;'.format(folder_name))
        os.chdir('..')
        
        os.chdir('Revisiting_Single_Depth_Estimation')
        os.system('time python demo.py --gpu 0 --output_folder {}'.format(folder_name))
        os.chdir('..')
        
        os.chdir('Freespace_Map/version_4/')
        os.system('python freespace.py --output_folder {}'.format(folder_name))
        os.chdir('../..')

    if int(sys.argv[3]) == 1:
        os.chdir("pytorch-0.4-yolov3")
        os.system("python my_detect_GUI.py cfg/yolo_v3.cfg yolov3.weights ../input/ GUI/{} data/coco.names".format(folder_name))
        os.chdir("..")

    if int(sys.argv[4]) == 1:
        # execute CGL test file
        os.chdir("../semantic-segmentation-pytorch")
        os.system("python3 -u CGL_test.py --imgs ../IMPRINT_project/input --gpu 0 --cfg config/cglncgl_ade20k-hrnetv2_medium.yaml --output GUI/{} VAL.visualize True".format(folder_name))
        os.chdir("../IMPRINT_project")

    c = -1

    # if int(sys.argv[2]) == 1:
    #     c+= 1
    #     if i == 0:
    #         cv2.namedWindow("Input Image")
    #         cv2.resizeWindow("Input Image",width, height)
    #         cv2.moveWindow("Input Image",cx[c],cy[c])
        
    #     lf = cv2.imread('input/' + file)
    #     lf = cv2.resize(lf, (width, height))
    #     cv2.imshow("Input Image",lf)
    
    if int(sys.argv[2]) == 1:
        c += 1
        # if i == 0:
        # cv2.startWindowThread()
        cv2.namedWindow("Maximal freespace direction")
        cv2.resizeWindow("Maximal freespace direction",width, height + 50)
        cv2.moveWindow("Maximal freespace direction",cx[c]+10,cy[c])
       
        # cv2.putText("Maximal freespace direction", "Hello World")
        # print("0")
        lf = cv2.imread('Freespace_Map/version_4/GUI/output/' + folder_name + "/" + file)
        lf = cv2.resize(lf, (width, height))
        # print(lf.shape)
        # print(np.full((height, 50,3), 255).shape)
        lf2 = cv2.imread("white.png")
        lf2 = cv2.resize(lf2, (width, 50))
        
        # cv2.imwrite('white.png',np.full((50, width,3), 255))
        lf = cv2.vconcat([lf2, lf])

        text = "Maximal freespace direction"
        textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)[0]
        textX = (lf.shape[1] - textsize[0]) / 2
        lf = cv2.putText(lf, text, (int(textX), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow("Maximal freespace direction",lf)
        
        cv2.namedWindow("Maximal freespace direction Legend")
        cv2.moveWindow("Maximal freespace direction Legend",int(cx[c] + (width) - 200 + 30),int(cy[c] + height + offsety))
        
        lf = cv2.imread('table_2.PNG')
        cv2.imshow("Maximal freespace direction Legend",lf)
        # cv2.waitKey(3000)    
        # print("2")
        # Image.fromarray(lf[:,:,::-1]).show()

    if int(sys.argv[3]) == 1:
        c += 1
        # if i == 0:
        cv2.namedWindow("Object Detection")
        cv2.resizeWindow("Object Detection",width, height + 500)
        cv2.moveWindow("Object Detection",cx[c] + 50,cy[c])
        

        lf = cv2.imread('pytorch-0.4-yolov3/GUI/' + folder_name + "/" + file)
        lf = cv2.resize(lf, (width, height))
        lf2 = cv2.imread("white.png")
        lf2 = cv2.resize(lf2, (width, 50))
        # print(lf.shape)
        # print(lf2.shape)
        # cv2.imwrite('white.png',np.full((50, width,3), 255))
        lf = cv2.vconcat([lf2, lf])
        text = "Object Detection"
        textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)[0]
        textX = (lf.shape[1] - textsize[0]) / 2
        
        lf = cv2.putText(lf, text, (int(textX), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow("Object Detection",lf)
        # cv2.waitKey(3000)

    if int(sys.argv[4]) == 1:
        c += 1
        # if i == 0:
        cv2.namedWindow("Covert Geo-Location (CGL) Detection")
        cv2.resizeWindow("Covert Geo-Location (CGL) Detection",width, height + 500)
        cv2.moveWindow("Covert Geo-Location (CGL) Detection",cx[c] + 50,cy[c])
        
        lf = cv2.imread('../semantic-segmentation-pytorch/GUI/' + folder_name + "/" + file)
        lf = cv2.resize(lf, (width, height))
        lf2 = cv2.imread("white.png")
        lf2 = cv2.resize(lf2, (width, 50))
        # print(lf.shape)
        # print(lf2.shape)
        # cv2.imwrite('white.png',np.full((50, width,3), 255))
        lf = cv2.vconcat([lf2, lf])
        text = "Covert Geo-Location (CGL) Detection"
        textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)[0]
        textX = (lf.shape[1] - textsize[0]) / 2
        
        lf = cv2.putText(lf, text, (int(textX), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow("Covert Geo-Location (CGL) Detection",lf)

    # if int(sys.argv[4]) == 1:
        # c += 1
    #     if i == 0:
    #         cv2.namedWindow("Maximal freespace direction")
    #         cv2.resizeWindow("Maximal freespace direction",width, height)
    #         cv2.moveWindow("Maximal freespace direction",cx[c],cy[c])
        
    #     lf = cv2.imread('Freespace_Map/version_4/GUI/output/' + folder_name + "/" + file)
    #     lf = cv2.resize(lf, (width, height))
    #     cv2.imshow("Maximal freespace direction",lf)
    
    # if int(sys.argv[3]) == 1:
    #     c+= 1
    #     if i == 0:
    #         cv2.namedWindow("Segmentation Map")
    #         cv2.resizeWindow("Segmentation Map",width, height)
    #         cv2.moveWindow("Segmentation Map",cx[c],cy[c])

    #     lf = cv2.imread('semantic-segmentation-pytorch/GUI/' + folder_name + "/" + file)
    #     lf = cv2.resize(lf, (width, height))
    #     cv2.imshow("Segmentation Map",lf)
    

    # if int(sys.argv[4]) == 1:
    #     c+= 1
    #     if i == 0:
    #         cv2.namedWindow("Depth Map")
    #         cv2.resizeWindow("Depth Map",width, height)
    #         cv2.moveWindow("Depth Map",cx[c],cy[c])

    #     lf = cv2.imread('Revisiting_Single_Depth_Estimation/GUI/' + folder_name + "/" + file)
    #     lf = cv2.resize(lf, (width, height))
    #     cv2.imshow("Depth Map",lf)

    # if int(sys.argv[5]) == 1:
    #     c+= 1
    #     if i == 0:
    #         cv2.namedWindow("SFD")
    #         cv2.resizeWindow("SFD",width, height)
    #         cv2.moveWindow("SFD",cx[c],cy[c])

    #     lf = cv2.imread('Freespace_Map/version_4/GUI/SFD/' + folder_name + "/" + file)
    #     lf = cv2.resize(lf, (width, height))
    #     cv2.imshow("SFD",lf)
    
    # if int(sys.argv[6]) == 1:
    #     c+= 1
    #     if i == 0:
    #         cv2.namedWindow("ASFDS")
    #         cv2.resizeWindow("ASFDS",width, height)
    #         cv2.moveWindow("ASFDS",cx[c],cy[c])

    #     lf = cv2.imread('Freespace_Map/version_4/GUI/ASFDS/' + folder_name + "/" + file)
    #     lf = cv2.resize(lf, (width, height))
    #     cv2.imshow("ASFDS",lf)
    
    # if int(sys.argv[7]) == 1:
    #     c+= 1
    #     if i == 0:
    #         cv2.namedWindow("Output")
    #         cv2.resizeWindow("Output",width, height)
    #         cv2.moveWindow("Output",cx[c],cy[c])

    #     lf = cv2.imread('Freespace_Map/version_4/GUI/output/' + folder_name + "/" + file)
    #     lf = cv2.resize(lf, (width, height))
    #     cv2.imshow("Output",lf)
    
    # if int(sys.argv[8]) == 1:
    #     c+= 1
    #     if i== 0:
    #         cv2.namedWindow("Object Detection")
    #         cv2.resizeWindow("Object Detection",width, height)
    #         cv2.moveWindow("Object Detection",cx[c],cy[c])

    #     lf = cv2.imread('Freespace_Map/version_4/GUI/output/' + folder_name + "/" + file)
    #     lf = cv2.resize(lf, (width, height))
    #     cv2.imshow("Object Detection",lf)
    
    if i == number_of_frames - 1:
        cv2.waitKey(0)
    else:
        cv2.waitKey(3000)
        
    os.remove('input/' + file)
    
cv2.waitKey(10)
