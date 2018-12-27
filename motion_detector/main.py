# ███╗   ██╗ ██████╗ ██████╗ ███████╗███╗   ███╗ ██████╗██╗   ██╗
# ████╗  ██║██╔═══██╗██╔══██╗██╔════╝████╗ ████║██╔════╝██║   ██║
# ██╔██╗ ██║██║   ██║██║  ██║█████╗  ██╔████╔██║██║     ██║   ██║
# ██║╚██╗██║██║   ██║██║  ██║██╔══╝  ██║╚██╔╝██║██║     ██║   ██║
# ██║ ╚████║╚██████╔╝██████╔╝███████╗██║ ╚═╝ ██║╚██████╗╚██████╔╝
# ╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═════╝

# File: main.py
# Author: Tommy Gingras
# Date: 2018-12-03
# License: All rights reserved Studio Webux S.E.N.C 2015-2018
# Source: https://github.com/MrPasty/esp8266-PIR/blob/master/main.py

# TODO: Add sleep mode at 5 seconds (But the tests crashed...)

import machine, esp, time
from utils import connectWIFI as WIFI
from umqtt.simple import MQTTClient

#MQTT CONFIGURATION
SERVER="192.168.2.27"
PORT=1883
USER="guest"
PASSWORD="guest"
CLIENT_ID=str(esp.flash_id())

# If the sensor is active or not.
State=""
activated = True

# D1 on the NodeMCU - PIR Input
INPUTPIN=5

# D2 on the NodeMCU - LED Output
OUTPUTPIN=4

print("Connected to pin %s" % (INPUTPIN))

# Connect to Wifi
print("wifi connecting,...")
WIFI.connect()

pin = machine.Pin(INPUTPIN, machine.Pin.IN)

def sub_cb(topic, msg):
    global Time
    print((topic, msg))
    command = msg.decode('ASCII') # convert bytestring back to string
    channel = topic.decode('ASCII') # convert bytestring back to string

    if channel == "CMD":
        if command == "on":
            activated = True
        if command == "off":
            activated = False

def main(server=SERVER, port=PORT, pwd=PASSWORD, user=USER):
    global CLIENT_ID, activated
    c = MQTTClient(CLIENT_ID, server, port, user, pwd, ssl=True)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe("CMD") # where we check if the script should run or not
    print("Connected to %s, subscribed to %s and %s topic" % (server, "CMD", "State"))
    if machine.reset_cause() == machine.SOFT_RESET:
        print('machine.SOFT_RESET')
        c.publish("State", CLIENT_ID + " Software reset")

    c.publish("State", CLIENT_ID + " Connected")
    try:
        motiondetected=0
        while activated:
            if pin.value() == 1 and motiondetected == 0:
                print("Motion Detected")
                motiondetected=1
                c.publish("State", CLIENT_ID + " Motion detected") # Motion detected !!
                machine.Pin(OUTPUTPIN, machine.Pin.OUT, value=1)
                time.sleep(1)

            if pin.value() == 0 and motiondetected == 1:
                print("Reset")
                motiondetected=0
                machine.Pin(OUTPUTPIN, machine.Pin.OUT, value=0)

            time.sleep(5)
    except OSError:
        print(sys.exc_info())

    finally:
        c.disconnect()

if __name__ == "__main__":
    try:
        main()
    except:
        print("An error occur, Rebooting machine")
        machine.reset()
