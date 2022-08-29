#import test
from flask import Flask,jsonify
import json
from multiprocessing import Process, Value
import time
app = Flask(__name__)

value = [0,0,0,0]
print (test.data)
def record_loop(loop_on):
    while True:
        if loop_on.value == True:
            print("loop running", value)
            value[0]+=1
        time.sleep(1)

@app.route("/")
def get_result():
    #return "Hello World"
    f = open('data.json')
    data = json.load(f)
    return jsonify({'seats': data['occupancy'], 'coord': data['coord']})


if __name__ == "__main__":
    #recording_on = Value('b',True)
    #p = Process(target=record_loop, args=(recording_on,))
    #p.start() 
    app.run(host='localhost', port=5000, debug=True,)#use_reloader=False)
    #p.join()