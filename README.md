## What is this?
This is my Final Year Project on Seat Vacancy Detection System through image recognition.

## Technologies used
- yolov5
- OpenCV
- PyTorch
- Backend Python FLASK
- Cors-anywhere
- React with Redux (with middleware thunk) and other frontend libraries

## Startup
1. Startup the RPI. (Remote access IP: 192.168.26.1. RPI: pi, raspberry)
2. Connect image processing PC to the RPI Wifi network (Name: HyFYP, password: HyFYP2022)
3. Run Rpi_Client_1080p.py (OR rpi_trial.py which uses split frame but since we only require 2fps on this project, the Rpi_Client_1080p is sufficient) on RPI & server.py on PC.
4. Run app.py for python FLASK backend to fetch results.
5. Go to my-app and type 'npm install' to install relevant dependencies and 'npm start' to run the website.

## Demos
### Web Demo
https://github.com/Aoi-00/Seat-Detection-System/assets/61011887/720f5018-64dc-44d7-8cea-371a412a8ada

### Email notification feature
https://github.com/Aoi-00/Seat-Detection-System/assets/61011887/5b39e32d-fa02-4894-877b-bd04c2097e71

### Update Bounding box if seat moves feature
https://github.com/Aoi-00/Seat-Detection-System/assets/61011887/e5bd597c-1edf-4785-b59a-c3de9e45e118



