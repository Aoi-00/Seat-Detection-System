import io
import socket
import struct
import time
import picamera
from PIL import Image

def encrypt(image,key):
    # convert to byte array for simple encryption on numeric data
    image = bytearray(image)
    # Perform XOR on each value of bytearray
    for index, values in enumerate(image):
        image[index] = values ^ key
    return image

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.26.14', 8000))
key = 34

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)

    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    start = time.time()
    stream = io.BytesIO()
    
    for foo in camera.capture_continuous(stream, 'jpeg'):
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        # Rewind the stream and send the image data over the wire
        stream.seek(0)

        # HOW TO ENCRYPT?? Doesnt work..
        # image = stream.read() 
        # image = encrypt(image,key)
        # connection.write(image)
        
        connection.write((stream.read()))
        time.sleep(1)
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
    # Write a length of zero to the stream to signal we're done, 1s delay between each pic
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
