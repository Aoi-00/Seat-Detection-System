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
5. Go to my-app and type 'npm start' to run the website.

