# Created during MIC Summer Camp 2015 in Belgium
# https://github.com/micdevcamp/BeerStock

# VALV
import RPi.GPIO as GPIO
import time
import datetime
import MFRC522
import signal
import sys
import requests
import json

valvgpio = 26
HALL_SENSOR = 18  #  Hall Sensr

def boardConfiguration():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(valvgpio, GPIO.OUT)
    GPIO.setup(HALL_SENSOR, GPIO.IN)

def openValv():
    print "valv open"
    GPIO.output(valvgpio, 1)

def sendJsonData(Lrfid_uid_0, Lrfid_uid_1, Lrfid_uid_2, Lrfid_uid_3, pulse):
    try:
        url = "http://10.20.20.61:8000/api/v1/record_rfid/?format=json"
        data = '{"rfid_uid_0": '+Lrfid_uid_0+', "rfid_uid_1": '+Lrfid_uid_1+', "rfid_uid_2": '+Lrfid_uid_2+', "rfid_uid_3": '+Lrfid_uid_3+', "pulse": '+pulse+'}'
        print data
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        apiReturnCode = r.status_code
        print r.text
          
        if apiReturnCode == 200:
            print " API OK"
        else:
            print " API ERROR RC: "+str(apiReturnCode)

    except requests.exceptions.ConnectionError as e:
      print "ERROR Connection to remote server unavailable " + str(e)

def closeValv():
    print "valv close"
    GPIO.output(valvgpio, 0)
    GPIO.cleanup()

def flowMeasurement():
    new_pusle = False
    cpt = 0
    cpt_before = 0
    flow=True
    last_flow_change = datetime.datetime.now()
    print "flowmeter start"

    while flow:
            # HALL sensor is HIGH when there no magnet contact
            # and LOW when magnet is present.
            cpt_before=cpt
            if not GPIO.input(HALL_SENSOR):
                    new_pusle = True
            elif new_pusle:
                    cpt += 1
                    new_pusle = False
                    sys.stdout.write('|')
                    # print ('PUSLE (' + str(cpt) + ') :' + str(time.time()))
                    
            if (cpt!=cpt_before):
                sys.stdout.write('.') 
                last_flow_change = datetime.datetime.now()
                
            else:
                time_in_5sec = last_flow_change + datetime.timedelta(seconds=5)
                if( datetime.datetime.now() > time_in_5sec ):
                    print "no more flow"
                    flow=False

    print "flowmeter stop"
    return cpt


continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()


# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        rfid_uid_0 = str(uid[0])
        rfid_uid_1 = str(uid[1])
        rfid_uid_2 = str(uid[2])
        rfid_uid_3 = str(uid[3])
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"

        boardConfiguration()
        print "transaction: start"

        openValv()
        
        flowCount = flowMeasurement()

        print "flow consuption: " +str(flowCount)
        sendJsonData(rfid_uid_0, rfid_uid_1, rfid_uid_2, rfid_uid_3, str(flowCount))
        closeValv()
        
        print "transaction: stop"
