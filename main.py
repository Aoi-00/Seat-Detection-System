import argparse
import numpy as np
import torch
from PIL import Image
import cv2
import os
import json


def load_model():
    global model
    # for PIL/cv2/np inputs and NMS
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s',
                           pretrained=True)


def _parse_args():
    '''Read CLI arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, default=os.path.expanduser("test.jpg"),
                        help="Path to the image to run the file on.")

    args = parser.parse_args()

    return args

def initialiseBB():
    f = open('initBB.json')
    initBbox = json.load(f)
    return initBbox

def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
	return iou


def main(args):
    load_model()
    img_path = args.image
    if not os.path.isfile(img_path):
        raise ValueError(
            "background_subtractor: {} is not a file".format(img_path))

    # cap = cv2.VideoCapture(vid_path)  # Open the video file
    # if not cap.isOpened():  # Check if the file is opened successfully
    #     raise ValueError("background_subtractor: VideoCapture failed to open file {}".format(vid_path))

    image = cv2.imread(img_path)  # OpenCV Image (BGR to RGB)
    frame = cv2.imread(img_path)
    # image = Image.open(img_path) # OR use PIL image, both method works
    imgs = [image]  # a batch of imgs

    # Inference
    results = model(imgs, size=640)

    # Results
    #results.print() #print in terminal
    results.show() #display pic
    results.save() #save pic

    # Data
    coords = results.pandas().xyxy[0].to_dict(orient="records")
    predefinedBBox = initialiseBB()
    occupancy = [0,0,0,0]              
    for coord in coords:  # Iterate through results
        con = coord['confidence']
        cs = coord['class']
        name = coord['name']
        x1 = int(coord['xmin'])
        y1 = int(coord['ymin'])
        x2 = int(coord['xmax'])
        y2 = int(coord['ymax'])
        if name == 'person' or name == 'laptop' or name == 'book' or name == 'cup' or name == 'suitcase' or name == 'bottle':
            boxA = [x1,y1,x2,y2] #Calculate overlap against each bbox 
            for index, coord in enumerate(predefinedBBox): 
                x1 = int(coord['xmin'])
                y1 = int(coord['ymin'])
                x2 = int(coord['xmax'])
                y2 = int(coord['ymax'])
                boxB = [x1,y1,x2,y2]
                cv2.putText(frame, 'Seat{0}'.format(index), (x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(36,255,12),2 )
                if occupancy[index] != 1:
                    intersect_area = bb_intersection_over_union(boxA,boxB) #Lower overlap requirement for items?
                    if intersect_area > 0.01:
                        cv2.rectangle(frame,(x1+1, y1+1), (x2+1, y2+1), (0, 0, 255), 2)
                        occupancy[index] = 1
                        print(intersect_area,occupancy)
                    else:
                        cv2.rectangle(frame,(x1+1, y1+1), (x2+1, y2+1), (0, 255, 0), 2)
                        print(intersect_area,occupancy)

                
    #print('\n', coords)  # Print img predictions in following format:
    #          x1 (pixels)  y1 (pixels)  x2 (pixels)  y2 (pixels)   confidence  class name

    cv2.imshow('img', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    args = _parse_args()
    main(args)
