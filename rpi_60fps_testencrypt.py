import io
import socket
import struct
import time
import picamera
import pyAesCrypt

# Using MJPEG Splitting from Rapid Capture and Processing: averages 69fps! With prediction, drops to 30fps

class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; send the old one's length
            # then the data
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                data = self.stream.read(size)
                encryptData = io.BytesIO()
                pyAesCrypt.encryptStream(data, encryptData, password, size)
                self.connection.write(encryptData.getvalue())
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)
password = "testencrypt"
client_socket = socket.socket()
client_socket.connect(('192.168.26.14', 8000))
connection = client_socket.makefile('wb')
try:
    output = SplitFrames(connection)
    with picamera.PiCamera(resolution='VGA', framerate=100) as camera:
        time.sleep(2)
        start = time.time()
        camera.start_recording(output, format='mjpeg')
    while True:
        try:
            camera.wait_recording(30)
            print ("30s has passed")
        except KeyboardInterrupt:
            camera.stop_recording()
            # Write the terminating 0-length to the connection to let the
            # server know we're done
            connection.write(struct.pack('<L', 0))
            break
finally:
    connection.close()
    client_socket.close()
    finish = time.time()
print('Sent %d images in %d seconds at %.2ffps' % (
    output.count, finish-start, output.count / (finish-start)))