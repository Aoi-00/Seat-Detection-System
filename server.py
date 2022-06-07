import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np
import time
import argparse
import numpy as np
import torch
from PIL import Image
import cv2
import os
import json
import pyAesCrypt
import base64

def bb_intersection_over_union(boxA, boxB): #calculate Intersection over union values of 2 Boxes (Seat & Person/Item)
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

def predict(img_batch):
    results = model(img_batch, size=640)
    # Results
    #results.print() #print in terminal
    #results.show() #display pic
    #results.save() #save pic
    return results

def base64_pil(base64_str):
    image = base64.b64decode(base64_str)
    image = io.BytesIO(image)
    image = Image.open(image)
    return image

def decrypt(image,key):
    # convert to byte array for simple encryption on numeric data
    image = bytearray(image)
    # Perform XOR on each value of bytearray
    for index, values in enumerate(image):
        image[index] = values ^ key
    return image


# Iniitialise model and seat bounding boxes
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s',
#                            pretrained=True)
# f = open('initBB.json')
# predefinedBBox = json.load(f)

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
key = 34

try:
    while True:
        start = time.time()
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        # Decrypt Image 
        print("decrypting..")
        image = decrypt(image,key)

        # Group into Batch of images & Predict
        #results = predict([image])

        # Display
        cv_image = np.array(image)


        # Check for occupancy
        # coords = results.pandas().xyxy[0].to_dict(orient="records")
        # occupancy = [0,0,0,0]              
        # for coord in coords:  # Iterate through results
        #     con = coord['confidence']
        #     cs = coord['class']
        #     name = coord['name']
        #     x1 = int(coord['xmin'])
        #     y1 = int(coord['ymin'])
        #     x2 = int(coord['xmax'])
        #     y2 = int(coord['ymax'])
        #     if name == 'person' or name == 'laptop' or name == 'book' or name == 'cup' or name == 'suitcase' or name == 'bottle':
        #         boxA = [x1,y1,x2,y2] #Calculate overlap against each bbox 
        #         for index, coord in enumerate(predefinedBBox): 
        #             x1 = int(coord['xmin'])
        #             y1 = int(coord['ymin'])
        #             x2 = int(coord['xmax'])
        #             y2 = int(coord['ymax'])
        #             boxB = [x1,y1,x2,y2]
        #             cv2.putText(cv_image, 'Seat{0}'.format(index), (x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(36,255,12),2 )
        #             if occupancy[index] != 1:
        #                 intersect_area = bb_intersection_over_union(boxA,boxB) #Lower overlap requirement for items?
        #                 if intersect_area > 0.01:
        #                     cv2.rectangle(cv_image,(x1+1, y1+1), (x2+1, y2+1), (0, 0, 255), 2)
        #                     occupancy[index] = 1
        #                     print(intersect_area,occupancy)
        #                 else:
        #                     cv2.rectangle(cv_image,(x1+1, y1+1), (x2+1, y2+1), (0, 255, 0), 2)
        #                     print(intersect_area,occupancy)
        cv2.imshow('Stream',cv_image)
        
        # finish = time.time()
        # print('fps = %.2ffps' % (1/(finish-start)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    connection.close()
    server_socket.close()