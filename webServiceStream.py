import time
from flask import Flask, Response
from flask_cors import CORS
import numpy, random
from datetime import datetime, timedelta
import json
from RandomDealData import *

app = Flask(__name__)
CORS(app)

rdd = None

@app.route('/')
def index():
    return "Data Generator is running..."

@app.route('/testservice')
def testservice():
    deal = rdd.createRandomData( rdd.createInstrumentList() )
    return Response( deal, status=200, mimetype='application/json')

@app.route('/streamTest')
def stream():
    instrList = rdd.createInstrumentList()
    def eventStream():
        while True:
            #nonlocal instrList
            yield rdd.createRandomData(instrList) + "\n"
    return Response(eventStream(), mimetype="text/event-stream")

@app.route('/streamTest/sse')
def sse_stream():
    instrList = rdd.createInstrumentList()
    def eventStream():
        while True:
            #nonlocal instrList
            yield 'data:{}\n\n'.format(rdd.createRandomData(instrList))
    return Response(eventStream(), mimetype="text/event-stream")


def get_time():
    """this could be any function that blocks until data is ready"""
    time.sleep(1.0)
    s = time.ctime(time.time())
    return s

def bootapp():
    global rdd 
    rdd = RandomDealData()
    app.run(debug=True, port=8080, threaded=True, host=('0.0.0.0'))

if __name__ == '__main__':
     bootapp()

