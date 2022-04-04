import sys
import time
from PIL import Image, ImageDraw
#from models.tiny_yolo import TinyYoloNet
from utils_GUI import *
from image import letterbox_image, correct_yolo_boxes
from darknet import Darknet
import os

namesfile=None
def detect(cfgfile, weightfile, img_folder, output_folder):
    m = Darknet(cfgfile)

    m.print_network()
    m.load_weights(weightfile)
    print('Loading weights from %s... Done!' % (weightfile))

    # if m.num_classes == 20:
    #     namesfile = 'data/voc.names'
    # elif m.num_classes == 80:
    #     namesfile = 'data/coco.names'
    # else:
    #     namesfile = 'data/names'
    
    use_cuda = torch.cuda.is_available()
    if use_cuda:
        m.cuda()

    # output_folder = "/media/vplab/Imprint_2/CGL_TRAINING/pytorch-0.4-yolov3/Imprint_Review_2_output/"
    # output_folder = os.path.join(output, img_folder)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    for imgfile in os.listdir(img_folder):
        img = Image.open(os.path.join(img_folder,imgfile)).convert('RGB')
        sized = letterbox_image(img, m.width, m.height)

        start = time.time()
        boxes = do_detect(m, sized, 0.5, 0.4, use_cuda)
        # print(boxes)
        correct_yolo_boxes(boxes, img.width, img.height, m.width, m.height)

        finish = time.time()
        print('%s: Predicted in %f seconds.' % (imgfile, (finish-start)))

        class_names = load_class_names(namesfile)
        # plot_boxes(img, boxes, 'predictions.jpg', class_names)
        save_result = os.path.join(output_folder, imgfile)
        
        plot_boxes(imgfile, img, boxes, savename=save_result, class_names=class_names)

def detect_cv2(cfgfile, weightfile, imgfile):
    import cv2
    m = Darknet(cfgfile)

    m.print_network()
    m.load_weights(weightfile)
    print('Loading weights from %s... Done!' % (weightfile))

    if m.num_classes == 20:
        namesfile = 'data/voc.names'
    elif m.num_classes == 80:
        namesfile = 'data/coco.names'
    else:
        namesfile = 'data/names'
    
    use_cuda = True
    if use_cuda:
        m.cuda()

    img = cv2.imread(imgfile)
    sized = cv2.resize(img, (m.width, m.height))
    sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)
    
    for i in range(2):
        start = time.time()
        boxes = do_detect(m, sized, 0.5, 0.4, use_cuda)
        finish = time.time()
        if i == 1:
            print('%s: Predicted in %f seconds.' % (imgfile, (finish-start)))

    class_names = load_class_names(namesfile)
    plot_boxes_cv2(img, boxes, savename='predictions.jpg', class_names=class_names)

def detect_skimage(cfgfile, weightfile, img_folder, output_folder):
    from skimage import io
    from skimage.transform import resize
    m = Darknet(cfgfile)

    m.print_network()
    m.load_weights(weightfile)
    print('Loading weights from %s... Done!' % (weightfile))

    if m.num_classes == 20:
        namesfile = 'data/voc.names'
    elif m.num_classes == 80:
        namesfile = 'data/coco.names'
    else:
        namesfile = 'data/names'
    
    use_cuda = True
    if use_cuda:
        m.cuda()
    # output_path = "/media/vplab/Imprint_2/CGL_TRAINING/pytorch-0.4-yolov3/Imprint_Review_2_output/"
    # output_folder = os.path.join(output_path, img_folder)
    if not exists(output_folder):
        os.mkdir(output_folder)
    for imgfile in os.listdir(img_folder):
        img = io.imread(imgfile)
        sized = resize(img, (m.width, m.height)) * 255
        
        for i in range(2):
            start = time.time()
            boxes = do_detect(m, sized, 0.5, 0.4, use_cuda)
            finish = time.time()
            if i == 1:
                print('%s: Predicted in %f seconds.' % (imgfile, (finish-start)))

        class_names = load_class_names(namesfile)
        save_result = os.path.join(output_folder, imgfile)
        plot_boxes_cv2(img, boxes, savename=save_result, class_names=class_names)

if __name__ == '__main__':
    if len(sys.argv) == 6:
        cfgfile = sys.argv[1]
        weightfile = sys.argv[2]
        imgfile = sys.argv[3]
        output_file = sys.argv[4]
        globals()["namesfile"] = sys.argv[5]
        detect(cfgfile, weightfile, imgfile, output_file)
        #detect_cv2(cfgfile, weightfile, imgfile)
        #detect_skimage(cfgfile, weightfile, imgfile)
    else:
        print('Usage: ')
        print('  python detect.py cfgfile weightfile imgfile outputfile names')
        #detect('cfg/tiny-yolo-voc.cfg', 'tiny-yolo-voc.weights', 'data/person.jpg', version=1)


