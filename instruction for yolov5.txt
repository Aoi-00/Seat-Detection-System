TO RUN:
1. cd yolov5
2. pip install -r requirements.txt
Note: classes 0,56 = detect only human&chair(low accuracy chair), source 0 = from webcam
3. python detect.py --classes 0 56 --source ../Videos/vid3.mp4
python detect.py --source 0  # webcam
                          img.jpg  # image
                          vid.mp4  # video
                          path/  # directory
                          path/*.jpg  # glob
                          'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                          'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream