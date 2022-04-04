import argparse
import torch
import torch.nn.parallel
# from models import modules, net, resnet, densenet, senet
import modules, net, resnet, densenet, senet
import numpy as np
import loaddata_demo as loaddata
import pdb
import os
import matplotlib.image
import matplotlib.pyplot as plt
import sys
plt.set_cmap("Greys")#colormap
#plt.set_cmap("jet")
import cv2 
import time
import numpy as np


def define_model(is_resnet, is_densenet, is_senet):
    if is_resnet:
        original_model = resnet.resnet50(pretrained = True)
        Encoder = modules.E_resnet(original_model) 
        model = net.model(Encoder, num_features=2048, block_channel = [256, 512, 1024, 2048])
    if is_densenet:
        original_model = densenet.densenet161(pretrained=True)
        Encoder = modules.E_densenet(original_model)
        model = net.model(Encoder, num_features=2208, block_channel = [192, 384, 1056, 2208])
    if is_senet:
        original_model = senet.senet154(pretrained='imagenet')
        Encoder = modules.E_senet(original_model)
        model = net.model(Encoder, num_features=2048, block_channel = [256, 512, 1024, 2048])

    return model
   

def main(output_folder):
    model = define_model(is_resnet=False, is_densenet=False, is_senet=True)
    
   
    if torch.cuda.is_available():
        model = torch.nn.DataParallel(model).cuda()
        map_location=lambda storage, loc: storage.cuda()
    else:
        model = torch.nn.DataParallel(model)
        map_location='cpu'
    
    model.load_state_dict(torch.load('./pretrained_model/model_senet',map_location=map_location))
    model = torch.nn.DataParallel(model)
    model.eval()
    file_names = []
    file_name = []
    count = 0
    for file in os.listdir("../input/"):
    # for file in os.listdir("/content/drive/My Drive/semantic-segmentation-pytorch/data/ADEChallengeData2016/images/validation/"):
        count += 1
        # if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".JPG"):
        file_name.append(file)
        #print(file)
                
        file_names.append("../input/"+file)
        # file_names.append("/content/drive/My Drive/semantic-segmentation-pytorch/data/ADEChallengeData2016/images/validation/"+file)
        if count == 8000:
            break
    # print(file_names)
    start_time = time.time()
    # print(len(file_name))
    for x in range(0,len(file_name)):#13
        # print(file_name[x])
        nyu2_loader = loaddata.readNyu2(file_names[x])
        input_image = cv2.imread(file_names[x])
        # print(np.shape(input_image))
        test(nyu2_loader, model,file_name[x],input_image.shape[1],input_image.shape[0],output_folder)
    end_time = time.time() - start_time
    print("Total time taken to evaluate" + str(len(file_name)) + "images : " + str(end_time))
    '''
    for x in range(6,10):#13
        nyu2_loader = loaddata.readNyu2('data/demo/'+str(x)+'.jpeg')
        
        input_image = cv2.imread('data/demo/'+str(x)+'.jpeg')
        
        
        test(nyu2_loader, model,x,input_image.shape[1],input_image.shape[0])

    '''    

def test(nyu2_loader, model,x,h,w,output_folder):

    for i, img in enumerate(nyu2_loader):     
        #image = torch.autograd.Variable(image, volatile=True)#.cuda()
        #image=torch.autograd.Variable(image,volatile=Volatile)
        print(type(img), img.size())
        image = img[:,0:3,:,:]
        image = torch.autograd.Variable(image, requires_grad=True)
        out = model(image)
        out = out.view(out.size(2),out.size(3)).data.cpu().numpy()
        
        
        stretch_near = cv2.resize(out, (h,w ),interpolation = cv2.INTER_CUBIC)#INTER_LANCZOS4) 
        #matplotlib.image.imsave('data/demo/'+str(x)+'.png', stretch_near)
        if not os.path.isdir("./GUI/" + output_folder):
            os.mkdir("./GUI/" + output_folder)
    
        # print("Image name", x,i)
        matplotlib.image.imsave("./GUI/" + output_folder+ "/" + x, stretch_near)
        # print(end_time)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Depth Estimation - Revisiting Single Depth Estimation"
    )
    parser.add_argument(
        "--gpu",
        default=0,
        type=int,
        help="gpu id for evaluation"
    )
    parser.add_argument(
        "--output_folder"
    )
    args = parser.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu)

    main(args.output_folder)
