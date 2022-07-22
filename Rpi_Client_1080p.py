import io
import socket
import struct
import time
import picamera

client_socket = socket.socket()
client_socket.connect(('192.168.26.14', 8000))
connection = client_socket.makefile('wb')
try:
    with picamera.PiCamera() as camera: # Camera settings
        camera.resolution = (1920, 1080)
        camera.framerate = 2 
        camera.rotation = 180
        time.sleep(2)
        start = time.time()
        count = 0
        stream = io.BytesIO()
        # Use the video-port for captures...
        for foo in camera.capture_continuous(stream, 'jpeg',
                                             use_video_port=True):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            count += 1
            #if time.time() - start > 30:
            #    break
            stream.seek(0)
            stream.truncate()
    connection.write(struct.pack('<L', 0))
  
except KeyboardInterrupt:
    connection.close()
    client_socket.close()
    finish = time.time()
print('Sent %d images in %d seconds at %.2ffps' % (
    count, finish-start, count / (finish-start)))