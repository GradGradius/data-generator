import time
from flask import Flask, Response
from flask_cors import CORS
import numpy, random
from datetime import datetime, timedelta
from Instrument import *
import json

instruments = ("Astronomica", "Borealis", "Celestial", "Deuteronic", "Eclipse",
			"Floral", "Galactia", "Heliosphere", "Interstella", "Jupiter", "Koronis", "Lunatic")
counterparties = ("Lewis", "Selvyn", "Richard", "Lina", "John", "Nidia")
NUMBER_OF_RANDOM_DEALS = 2000
TIME_PERIOD_MILLIS = 3600000
EPOCH = datetime.now() - timedelta(days = 1)

app = Flask(__name__)
CORS(app)

def createInstrumentList():
    f = open('initialRandomValues.txt', 'r')
    instrumentId = 1000
    instrumentList = []
    for instrumentName in instruments:
        hashedValue = int(f.readline())
        isNegative = hashedValue < 0
        basePrice = (abs(hashedValue) % 10000) + 90.0
        drift = ((abs(hashedValue) % 5) * basePrice) / 1000.0
        drift = 0 - drift if isNegative else drift
        variance = (abs(hashedValue) % 1000) / 100.0
        variance = 0 - variance if isNegative else variance
        instrument = Instrument(instrumentId, instrumentName, basePrice, drift, variance)
        instrumentList.append(instrument)
        instrumentId += 1
    return instrumentList

@app.route('/')
def index():
    return "Data Generator is running..."

@app.route('/testservice')
def testservice():
    deal = createRandomData( createInstrumentList() )
    return Response( deal, status=200, mimetype='application/json')

@app.route('/streamTest')
def stream():
    instrList = createInstrumentList()
    def eventStream():
        while True:
            #nonlocal instrList
            yield createRandomData(instrList) + "\n"
    return Response(eventStream(), mimetype="text/event-stream")

@app.route('/streamTest/sse')
def sse_stream():
    instrList = createInstrumentList()
    def eventStream():
        while True:
            #nonlocal instrList
            yield 'data:{}\n\n'.format(createRandomData(instrList))
    return Response(eventStream(), mimetype="text/event-stream")


def get_message():
    """this could be any function that blocks until data is ready"""
    time.sleep(1.0)
    s = time.ctime(time.time())
    return s

def createRandomData( instrumentList ):
    time.sleep(random.uniform(1,30)/100)
    dealId = 20000
    instrument = instrumentList[numpy.random.randint(0,len(instrumentList))]
    cpty = counterparties[numpy.random.randint(0,len(counterparties))]
    type = 'B' if numpy.random.choice([True, False]) else 'S'
    quantity = int( numpy.power(1001, numpy.random.random()))
    dealTime = datetime.now() - timedelta(days = 1)
    dealId += 1
    deal = {
        'instrumentName' : instrument.name,
        'cpty' : cpty,
        'price' : instrument.calculateNextPrice(type),
        'type' : type,
        'quantity' : quantity,
        'time' : dealTime.strftime("%d-%b-%Y (%H:%M:%S.%f)"),
        }
    return json.dumps(deal)

if __name__ == '__main__':
     app.run(port=8080, threaded=True, host=('0.0.0.0'))

