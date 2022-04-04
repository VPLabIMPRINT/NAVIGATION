import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

classes = ['Backpack', 'Board', 'Book', 'Bottle', 'Box', 'Chair', 'Clock', 'CPU', 'Fire_Extinguisher', 
'Keyboard', 'Mouse', 'Phone', 'Potted_Plant', 'Printer', 'Refrigerator', 'Remote', 'Sofa', 
'Speakers', 'Switch', 'Table' , 'TV_Monitor', 'Water_Can']

# sets=[('DSC_1056', 'train'), ('DSC_1045', 'train'), ('DSC_1064', 'train'), ('DSC_1043', 'train'), ('DSC_1059', 'train'), ('DSC_1050', 'train'), ('DSC_1044', 'train'), ('DSC_1062', 'train'), ('DSC_1053', 'train'), ('DSC_0997', 'train'), ('DSC_0985', 'train'), ('DSC_0998', 'train'), ('DSC_1004', 'train'), ('DSC_0996', 'train'), ('DSC_0999', 'train'), ('DSC_0977', 'train'), ('DSC_1003', 'train'), ('DSC_0976', 'train'), ('DSC_1002', 'train'), ('DSC_0988', 'train'), ('DSC_0993', 'train'), ('DSC_0986', 'train'), ('DSC_0992', 'train'), ('DSC_1000', 'train'), ('DSC_0973', 'train'), ('DSC_0984', 'train'), ('DSC_0991', 'train'), ('DSC_0994', 'train'), ('DSC_0989', 'train'), ('DSC_1895', 'train'), ('DSC_1898', 'train'), ('DSC_1900', 'train'), ('DSC_1899', 'train'), ('DSC_0827', 'train'), ('DSC_1337', 'train'), ('DSC_0837', 'train'), ('DSC_0834', 'train'), ('DSC_0831', 'train'), ('DSC_0800', 'train'), ('DSC_0796', 'train'), ('DSC_0802', 'train'), ('DSC_0811', 'train'), ('DSC_0797', 'train'), ('DSC_0803', 'train'), ('DSC_0799', 'train'), ('DSC_0816', 'train'), ('DSC_0809', 'train'), ('DSC_0798', 'train'), ('DSC_1083', 'train'), ('DSC_1075', 'train'), ('DSC_1084', 'train'), ('DSC_1029', 'train'), ('DSC_1027', 'train'), ('DSC_1028', 'train'), ('DSC_0853', 'train'), ('DSC_0858', 'train'), ('DSC_0855', 'train'), ('DSC_0865', 'train'), ('DSC_0856', 'train'), ('DSC_0871', 'train'), ('DSC_0854', 'train'), ('DSC_0873', 'train'), ('DSC_0859', 'train'), ('DSC_1329', 'train'), ('DSC_0863', 'train'), ('DSC_0867', 'train'), ('DSC_0861', 'train'), ('DSC_0857', 'train'), ('DSC_0875', 'train')]
# sets = [('DSC_0864', 'train'), ('DSC_1901', 'train'), ('DSC_1058', 'train'), ('DSC_1031', 'train'), ('DSC_1014', 'train'), ('DSC_1087', 'train'), ('DSC_1060', 'train'), ('DSC_0874', 'train'), ('DSC_1015', 'train'), ('DSC_0869', 'train'), ('DSC_1013', 'train'), ('DSC_1001', 'train'), ('DSC_1005', 'train'), ('DSC_0819', 'train'), ('DSC_0840', 'train')]
print(type(sets))
# classes = ['AC', 'Backpack', 'Board', 'Book', 'Bottle', 'Box', 'Calendar', 'Chair', 'Clock', 'CPU', 'Cupboard', 'Dustbin', 'Fan', 'Fire_Extinguisher', 'Keyboard', 'Mouse', 'Pen_Stand', 'Phone', 'Potted_Plant', 'Printer', 'Refrigerator', 'Remote', 'Shelf', 'Sofa', 'Speakers', 'Switch', 'Table', 'TV_Monitor', 'Water_Can']
print(type(classes))
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(folder, image_id):
    base_file_name = 'metadata/%s/Annotations/'%(folder)
    eg_name = '%s.xml'
    in_file = open('metadata/%s/Annotations/%s_%s.xml'%(folder, folder, image_id))
    out_file = open('metadata/%s/labels/%s_%s.txt'%(folder, folder, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('height').text)
    h = int(size.find('width').text)
    isObject = 0
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        isObject += 1
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    if isObject == 0:
        return 0
    else:
        return 1

wd = getcwd()
print("Current working directory is :", wd)

for folder, image_set in sets:
    print(folder)
    if not os.path.exists('metadata/%s/labels/'%(folder)):
        os.makedirs('metadata/%s/labels/'%(folder))
    image_ids = open('metadata/%s/ImageSets/Main/%s.txt'%(folder, image_set)).read().strip().split()
    list_file = open('%s_%s.txt'%(folder, image_set), 'w')
    for image_id in image_ids:
        if convert_annotation(folder, image_id) == 1:
            list_file.write('%s/metadata/%s/JPEGImages/%s_%s.jpg\n'%(wd, folder, folder, image_id))
    list_file.close()

