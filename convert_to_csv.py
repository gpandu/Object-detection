# -*- coding: utf-8 -*-
import os
import pandas as pd
from PIL import Image
import re

def get_csv_data():
    file = open('train.csv','a')
    annot_list = []
    for filename in os.listdir("data/Annotation"):
        with open("data/Annotation/"+filename, 'r') as file1:
            image = filename.split('.')[0]
            im=Image.open("data/Images/"+image+".jpg")
            size = im.size
            for line in file1:
                rects = line.rstrip().split(' ')
                per_class = 'wihout_soil' if int(rects[0])==1 else 'carrying_soil'
                rects.pop(0)
                row = [image+".jpg", size[0], size[1], per_class]
                row.extend([int(rects[0]), int(rects[1]), int(rects[2]), int(rects[3])])
                annot_list.append(row)
            im.close()
                
    df = pd.DataFrame(annot_list, columns = ["filename", "width", "height", "class", "xmin", "xmax", "ymin", "ymax"])
    df.to_csv(file)
    file.close()        
            


def convert_to_csv():
    file = open('data/test.csv','a')
    annot_list = []
    for filename in os.listdir("data/val_annot"):
        with open("data/val_annot/"+filename, 'r') as file1:
            image = filename.split('.')[0]
            im=Image.open("data/Images/"+image+".png")
            size = im.size
            for line in file1:
                if(re.search('^Bounding box for object', line)):
                    box = line.split('(Xmax, Ymax) :',1)[1].replace(" ","").rstrip().split("-")
                    p1 = box[0][box[0].find("(")+1:box[0].find(")")].split(",")
                    p2 = box[1][box[1].find("(")+1:box[1].find(")")].split(",")
                    annot_list.append([image+".png", size[0], size[1], 'person', int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1])])
            im.close()
            
    df = pd.DataFrame(annot_list, columns = ["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"])
    df.to_csv(file)
    file.close()     


if __name__ == '__main__':
    get_csv_data()