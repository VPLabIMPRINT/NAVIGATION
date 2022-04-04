import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.ndimage as ndimage
import os
import time
from IPython.display import Image, display, Javascript, clear_output
from google.colab.output import eval_js
from base64 import b64decode
from IPython.utils import io
from shutil import copyfile
import glob

def initialize_graph():
  font_size=20
  fig, axs = plt.subplots(2, 4, figsize=(30,12))
  fig.patch.set_visible(False)
  for ax_ in axs:
    for ax in ax_:
      ax.set_xticks([])
      ax.set_yticks([])
      
  axs[0,0].set_title("Input",fontsize=font_size)
  axs[0,1].set_title("Floor vs Non-floor Segmentation",fontsize=font_size)
  axs[0,2].set_title("Depth Map",fontsize=font_size)
  axs[1,0].set_title("SFD",fontsize=font_size)
  axs[1,1].set_title("ASFDS",fontsize=font_size)
  axs[1,2].set_title("Direction of maximum freespace",fontsize=font_size)
  axs[0,3].axis("off")
  axs[1,3].axis("off")
  # fig.suptitle('GUI', fontsize=30) 
  plt.subplots_adjust(wspace=0.1, hspace=0.2)
  return fig,axs 
 
# def take_photo(filename='photo.jpg', quality=0.8):
#   js = Javascript('''
#     async function takePhoto(quality) {
#       const div = document.createElement('div');
#       const capture = document.createElement('button');
#       capture.textContent = 'Capture';
#       div.appendChild(capture);
 
#       const video = document.createElement('video');
#       video.style.display = 'block';
#       const stream = await navigator.mediaDevices.getUserMedia({video: true});
 
#       document.body.appendChild(div);
#       div.appendChild(video);
#       video.srcObject = stream;
#       await video.play();
 
#       google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);
 
#       new Promise((resolve) => capture.onclick = resolve);
 
#       const canvas = document.createElement('canvas');
#       canvas.width = video.videoWidth;
#       canvas.height = video.videoHeight;
#       canvas.getContext('2d').drawImage(video, 0, 0);
#       stream.getVideoTracks()[0].stop();
#       div.remove();
#       return canvas.toDataURL('image/jpeg', quality);
#     }
#     ''')
#   display(js)
#   data = eval_js('takePhoto({})'.format(quality))
#   binary = b64decode(data.split(',')[1])
  
#   return binary
 
def initialize_graph_production():
  font_size=20
  fig = plt.gcf()
  fig.set_size_inches(24, 10)
  plt.title("Production Mode")
  a1 = plt.subplot2grid((4,12),(0,0),colspan=4,rowspan=3)
  a1.set_xticks([])
  a1.set_yticks([])
  a2 = plt.subplot2grid((4,12),(0,4),colspan=4,rowspan=3)
  a2.set_xticks([])
  a2.set_yticks([])
  a3 = plt.subplot2grid((4,12),(0,8),colspan=4,rowspan=3)
  a3.set_xticks([])
  a3.set_yticks([])
  a4 = plt.subplot2grid((4,12),(3,4), colspan = 4)
  a4.set_xticks([])
  a4.set_yticks([])
  a1.set_title("Input",fontsize=font_size)
  a2.set_title("Maximum Freespace Direction",fontsize=font_size)
  a3.set_title("Object Detection",fontsize=font_size)
  return a1,a2,a3,a4

def initialize_graph_production_without_obj_det():
  font_size=20
  fig = plt.gcf()
  fig.set_size_inches(18, 10)
  plt.title("Production Mode")
  a1 = plt.subplot2grid((4,8),(0,0),colspan=4,rowspan=3)
  a1.set_xticks([])
  a1.set_yticks([])
  a2 = plt.subplot2grid((4,8),(0,4),colspan=4,rowspan=3)
  a2.set_xticks([])
  a2.set_yticks([])
  a3 = plt.subplot2grid((4,8),(3,3), colspan = 2)
  a3.set_xticks([])
  a3.set_yticks([])
  a1.set_title("Input",fontsize=font_size)
  a2.set_title("Maximum Freespace Direction",fontsize=font_size)
  return a1,a2,a3

 
def GUI(webcam,number_of_frames,gt_available,root_folder,output_folder,mode,ext=".png"):
  font_size = 20
  if webcam == False:
    list_of_images = os.listdir(root_folder)
    number_of_frames = len(list_of_images)
    
  for i in range(number_of_frames):
    try:
      if webcam == True:
        file = str(i) + "inpt"
        b = take_photo()
        with open(root_folder + file +ext, 'wb') as f:
          f.write(b)
      else:
        print(list_of_images)
        file = list_of_images[i].split(".")[0]
      
      with io.capture_output() as captured:
        copyfile(root_folder + file +ext, "./GUI/input/"  + file +  ext)
 
      if mode == "production":
        clear_output()
        a1,a2,a3 = initialize_graph_production_without_obj_det()
        img = cv2.imread(root_folder + file + ext)[:, :, [2, 1, 0]]
        a3.axis("off")
        a1.imshow(img)
        a2.text(0.5, 0.5, 'Estimating segmentation map...', horizontalalignment='center',verticalalignment='center')
        plt.show()

      if mode != "production":
        start_time = time.time()
        clear_output()
        fig,axs = initialize_graph()
        axs[0,0].imshow(cv2.imread("./GUI/input/" + file + ext)[:, :, [2, 1, 0]])
        axs[0,1].text(0.5, 0.5, 'Processing...', horizontalalignment='center',verticalalignment='center')
        axs[0,2].text(0.5, 0.5, 'Processing...', horizontalalignment='center',verticalalignment='center')
        axs[1,0].text(0.5, 0.5, 'Processing...', horizontalalignment='center',verticalalignment='center')
        axs[1,1].text(0.5, 0.5, 'Processing...', horizontalalignment='center',verticalalignment='center')
        axs[1,2].text(0.5, 0.5, 'Processing...', horizontalalignment='center',verticalalignment='center')
        time1 = str(round(time.time() - start_time,3))
        axs[0,0].set_xlabel("Processing time: " + time1 + "seconds" , labelpad = 10,fontsize=font_size)
        plt.show()
        start_time = time.time()
 
      
      with io.capture_output() as captured:
        %cd /content/drive/My\ Drive/semantic-segmentation-pytorch
        !python3 -u test.py --imgs /content/drive/My\ Drive/GUI/input --gpu 0 --cfg config/GUI_ade20k-mobilenetv2dilated-c1_deepsup.yaml VAL.visualize True;
        %cd /content/drive/My\ Drive/
      
      if mode == "production":
        clear_output()
        a1,a2,a3 = initialize_graph_production_without_obj_det()
        img = cv2.imread(root_folder + file + ext)[:, :, [2, 1, 0]]
        a3.axis("off")
        a1.imshow(img)
        a2.text(0.5, 0.5, 'Estimating Depth map...', horizontalalignment='center',verticalalignment='center')
        plt.show()

      if mode != "production":
        fig,axs = initialize_graph()
        clear_output()
        axs[0,0].imshow(cv2.imread("./GUI/input/" + file +ext)[:, :, [2, 1, 0]])
        axs[0,1].imshow(cv2.imread("./semantic-segmentation-pytorch/GUI/" + file + ext))
        axs[0,2].text(0.5, 0.5, 'Processing...', horizontalalignment='center',verticalalignment='center')
        axs[1,0].text(0.5, 0.5, 'Processing...', horizontalalignment='center',verticalalignment='center')
        axs[1,1].text(0.5, 0.5, 'Processing...', horizontalalignment='center',verticalalignment='center')
        axs[1,2].text(0.5, 0.5, 'Processing...', horizontalalignment='center',verticalalignment='center')
        axs[0,0].set_xlabel("Processing time: " + time1 + "seconds", labelpad = 10,fontsize=font_size)
        time2 = str(round(time.time() - start_time,3))
        axs[0,1].set_xlabel("Processing time: " + time2 + "seconds", labelpad = 10,fontsize=font_size)
        plt.show()
        start_time = time.time()
      
      with io.capture_output() as captured:
        %cd /content/drive/My\ Drive/Revisiting_Single_Depth_Estimation
        !time python demo.py;
        %cd /content/drive/My\ Drive/
      
      if mode == "production":
        clear_output()
        a1,a2,a3 = initialize_graph_production_without_obj_det()
        img = cv2.imread(root_folder + file + ext)[:, :, [2, 1, 0]]
        a3.axis("off")
        a1.imshow(img)
        a2.text(0.5, 0.5, 'Estimating Maximum freespace direction...', horizontalalignment='center',verticalalignment='center')
        plt.show()

      if mode != "production":
        fig,axs = initialize_graph()
        clear_output() 
        axs[0,0].imshow(cv2.imread("./GUI/input/" + file +ext)[:, :, [2, 1, 0]])
        axs[0,1].imshow(cv2.imread("./semantic-segmentation-pytorch/GUI/"+ file + ext))
        axs[0,2].imshow(cv2.imread("./Revisiting_Single_Depth_Estimation/GUI/"+ file + ext))
        axs[1,0].text(0.5, 0.5, 'Processing...', horizontalalignment='center',verticalalignment='center')
        axs[1,1].text(0.5, 0.5, 'Processing...', horizontalalignment='center',verticalalignment='center')
        axs[1,2].text(0.5, 0.5, 'Processing...', horizontalalignment='center',verticalalignment='center')
        axs[0,3].imshow(cv2.imread("./GUI/" + "color_bar.PNG"))
        axs[0,0].set_xlabel("Processing time: " + time1 + "seconds", labelpad = 10,fontsize=font_size)
        axs[0,1].set_xlabel("Processing time: " + time2 + "seconds", labelpad = 10,fontsize=font_size)
        time3 = str(round(time.time() - start_time,3))
        axs[0,2].set_xlabel("Processing time: " + time3 + "seconds", labelpad = 10,fontsize=font_size)
        plt.show()
        start_time = time.time()
      
      
      with io.capture_output() as captured:
        %cd /content/drive/My\ Drive/project_work/Neha_MTP_2020/Freespace_Map/version_4/
        !python freespace.py --output_folder $output_folder; 
        %cd /content/drive/My\ Drive/
      
      

      if mode != "production":
        fig,axs = initialize_graph()
        
        axs[0,0].imshow(cv2.imread("./GUI/input/" + file +ext)[:, :, [2, 1, 0]])
        axs[0,1].imshow(cv2.imread("./semantic-segmentation-pytorch/GUI/"+ file + ext))
        axs[0,2].imshow(cv2.imread("./Revisiting_Single_Depth_Estimation/GUI/"+ file +ext))
        axs[0,3].imshow(cv2.imread("./GUI/" + "color_bar.PNG"))
 
      
        
      with io.capture_output() as captured:
        %cd /content/drive/My\ Drive/project_work/Neha_MTP_2020/Freespace_Map/version_4/GUI/SFD
 
     
      
      if mode != "production":  
        axs[1,0].imshow(cv2.imread(output_folder + file + ext))

      with io.capture_output() as captured:
        %cd ../ASFDS/
      
      if mode != "production":  
        axs[1,1].imshow(cv2.imread(output_folder + file + ext))
      
      with io.capture_output() as captured:
        %cd ../output/
      
      if mode == "production":
        a1,a2,a3 = initialize_graph_production_without_obj_det()
        img = cv2.imread(output_folder + file + ext)[:, :, [2, 1, 0]]
        a2.imshow(img)
        

      if mode != "production":  
        axs[1,2].imshow(cv2.imread(output_folder + file + ext)[:, :, [2, 1, 0]])
      
      with io.capture_output() as captured:
        %cd /content/drive/My\ Drive
        
      if mode == "production":
        a1.imshow(cv2.imread("./GUI/input/" + file +ext)[:, :, [2, 1, 0]])
        a3.imshow(cv2.imread("./GUI/" + "table_2.PNG")[:, :, [2, 1, 0]])  
        clear_output()
        plt.show()
        time.sleep(1)

      with io.capture_output() as captured:
        os.remove("./GUI/input/" + file + ext)

      if mode != "production":  
        if gt_available == True:
          axs[1,3].imshow(cv2.imread("./GUI/" + "table.PNG")[:, :, [2, 1, 0]])    
        else:
          axs[1,3].imshow(cv2.imread("./GUI/" + "table_2.PNG")[:, :, [2, 1, 0]])    
        clear_output()
        axs[0,0].set_xlabel("Processing time: " + time1 + "seconds", labelpad = 10,fontsize=font_size)
        axs[0,1].set_xlabel("Processing time: " + time2 + "seconds", labelpad = 10,fontsize=font_size)
        time3 = str(round(time.time() - start_time,3))
        axs[0,2].set_xlabel("Processing time: " + time3 + "seconds", labelpad = 10,fontsize=font_size)
        axs[1,1].axis("off")
        plt.show()
      

      
    except Exception as err:
      print(str(err))