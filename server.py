import enum
import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np
import time
import numpy as np
import torch
from PIL import Image
import cv2
import json
import base64
from collections import deque
import math


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist
# calculate Intersection over union values of 2 Boxes (Seat & Person/Item)


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


def predict(img_batch):
    results = model(img_batch, size=640)
    # Results
    # results.print() #print in terminal
    # results.show() #display pic
    # results.save() #save pic
    return results


def base64_pil(base64_str):
    image = base64.b64decode(base64_str)
    image = io.BytesIO(image)
    image = Image.open(image)
    return image


def updateBB(chairs, Bbox, persons):
    allChairs = np.array(chairs)
    chairExists = []
    # Find whether a chair/human exists in seat
    for index, bbox in enumerate(Bbox):
        boxA = [int(bbox['xmin']), int(bbox['ymin']),
                int(bbox['xmax']), int(bbox['ymax'])]
        chairExists.append(False)
        for chair in chairs:
            boxB = [int(chair['xmin']), int(chair['ymin']),
                    int(chair['xmax']), int(chair['ymax'])]
            if bb_intersection_over_union(boxA, boxB) > 0:
                chairExists[index] = True
                break
        for person in persons:
            boxB = [int(person['xmin']), int(person['ymin']),
                    int(person['xmax']), int(person['ymax'])]
            if bb_intersection_over_union(boxA, boxB) > 0:
                chairExists[index] = True
                break

    if all(chairExists) == False:  # If there are bounding boxes without a chair in it
        # Find chairs not in any Bbox currently
        chairsNotInBbox = []
        for index, chair in enumerate(chairs):
            boxA = [int(chair['xmin']), int(chair['ymin']),
                    int(chair['xmax']), int(chair['ymax'])]
            chairsNotInBbox.append(True)
            for bbox in Bbox:
                boxB = [int(bbox['xmin']), int(bbox['ymin']),
                        int(bbox['xmax']), int(bbox['ymax'])]
                # Calculate if any chair overlaps with bbox
                if bb_intersection_over_union(boxA, boxB) > 0:
                    chairsNotInBbox[index] = False
                    break
        # Obtain chairs not in any bbox
        filter = np.array(chairsNotInBbox)
        availChairs = allChairs[filter].tolist()
        print("Filter:",filter)
        print("Chairs:", chairs)
        print("AvailChairs:", availChairs)
        if (len(availChairs)):
            for i, bbox in enumerate(Bbox):
                if chairExists[i] == False:
                    oldBboxCenter = [int(
                        Bbox[i]['xmax'])-int(Bbox[i]['xmin']), int(Bbox[i]['ymax'])-int(Bbox[i]['ymin'])]
                    dist = []
                    # Update bbox with nearest distance chair (that is not in any bbox yet)
                    for index, chair in enumerate(availChairs):
                        chairCenter = [
                            int(chair['xmax'])-int(chair['xmin']), int(chair['ymax'])-int(chair['ymin'])]
                        dist.append(calculateDistance(
                            oldBboxCenter[0], oldBboxCenter[1], chairCenter[0], chairCenter[1]))
                    Bbox[i] = availChairs[dist.index(min(dist))]
    return Bbox


def update_occupancy(occupancy, seat):

    for index, seatOccupancy in enumerate(occupancy):
        seat[index].pop(0)
        seat[index].append(seatOccupancy)
        occupancy[index] = 1 if all(
            occupied == 1 for occupied in seat[index]) else 0
    return occupancy


def drawBbox(occupancy, cv, predefinedBBox):
    for index, bbox in enumerate(predefinedBBox):
        if occupancy[index] == 1:  # Occupied, draw red
            cv2.rectangle(cv, (int(bbox['xmin'])+1, int(bbox['ymin'])+1),
                          (int(bbox['xmax'])+1, int(bbox['ymax'])+1), (0, 0, 255), 2)
        else:  # Vacant, draw green
            cv2.rectangle(cv, (int(bbox['xmin'])+1, int(bbox['ymin'])+1),
                          (int(bbox['xmax'])+1, int(bbox['ymax'])+1), (0, 255, 0), 2)
    return cv


# Iniitialise model and seat bounding boxes
model = torch.hub.load('ultralytics/yolov5', 'yolov5s',
                       pretrained=True)
f = open('initBB.json')  # either initialDemoChair.json/ initBB.json
predefinedBBox = json.load(f)
seat = [[0, 0] for _ in range(len(predefinedBBox))]

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')

try:
    while True:
        start = time.time()
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack(
            '<L', connection.read(struct.calcsize('<L')))[0]
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

        # Group into Batch of images & Predict
        results = predict([image])

        # Display
        cv_image = np.array(image)
        # cv2.imshow('Stream',cv_image)
        # print("Image time:" + str(time.time() - start))

        # Check for occupancy
        coords = results.pandas().xyxy[0].to_dict(orient="records")
        chairs = [coord for coord in coords if coord['name'] == 'chair']
        persons = [coord for coord in coords if coord['name'] == 'person']
        occupancy = [0 for _ in range(len(predefinedBBox))]
        for coord in coords:  # Iterate through results
            con = coord['confidence']
            cs = coord['class']
            name = coord['name']
            x1 = int(coord['xmin'])
            y1 = int(coord['ymin'])
            x2 = int(coord['xmax'])
            y2 = int(coord['ymax'])
            # If any of these classes identified
            if name == 'person' or name == 'backpack' or name == 'suitcase' or name == 'bottle':
                boxA = [x1, y1, x2, y2]  # Calculate overlap against each bbox
                # Updated Bbox
                #predefinedBBox = updateBB(chairs, predefinedBBox, persons)
                for index, coord in enumerate(predefinedBBox):
                    x1 = int(coord['xmin'])
                    y1 = int(coord['ymin'])
                    x2 = int(coord['xmax'])
                    y2 = int(coord['ymax'])
                    boxB = [x1, y1, x2, y2]  # Label seats based on Bbox
                    cv2.putText(cv_image, 'Seat{0}'.format(
                        index), (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)

                    if occupancy[index] != 1:
                        intersect_area = bb_intersection_over_union(
                            boxA, boxB)  # Lower overlap requirement for items?
                        if intersect_area > 0.01:  # Occupied
                            # cv2.rectangle(cv_image, (x1+1, y1+1),
                            #               (x2+1, y2+1), (0, 0, 255), 2)

                            occupancy[index] = 1
                            #print(intersect_area, occupancy)

                        # else: #Unoccupied
                        #     cv2.rectangle(cv_image, (x1+1, y1+1),
                        #                   (x2+1, y2+1), (0, 255, 0), 2)
                        #     #print(intersect_area, occupancy)
        occupancy = update_occupancy(occupancy, seat)
        cv_image = drawBbox(occupancy, cv_image, predefinedBBox)
        
        # Write to data.json file
        data = {
            'occupancy': occupancy,
            "coord": predefinedBBox
        }
        with open('data.json','w') as f:
            json.dump(data,f,indent=6)
        cv2.imshow('Stream', cv_image)
        print("Image time:" + str(time.time() - start))

        # finish = time.time()
        # print('fps = %.2ffps' % (1/(finish-start)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    connection.close()
    server_socket.close()
