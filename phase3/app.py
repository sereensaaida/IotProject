from flask import Flask, send_from_directory, request, jsonify
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep
import datetime
import os
import smtplib
import email
import imaplib


app = Flask(__name__)

light_intensity = 0
LED_PIN = 17

#initialize MQTT client
mqtt_client = mqtt.Client()

def on_message(client,userdata,msg):
    topic = msg.topic
    if topic == "lightintensity":
        global light_intensity
        light_intensity = msg.payload.decode("utf-8")
        print(f"Light Intensity: {light_intensity}")
    elif topic == "led/status":
        led_status = msg.payload.decode("utf-8")
        print(f"LED Status: {led_status}")
        if led_status == "on":
            send_notification_email()

#set up the connection and subscribe to the light topic that is published from the code for the esp32
def mqtt_setup():
    mqtt_client.connect('localhost',1883)
    #change topic name once esp32 code has been written
    mqtt_client.subscribe("lightintensity")
    # LED status changes
    mqtt_client.subscribe("led/status")
    #handle incoming messages from the light topic -> called automatically by paho-mqtt
    mqtt_client.on_message = on_message
    #listen for messages
    mqtt_client.loop_start()
    
mqtt_setup()

def turn_on_led():
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM) # Use BCM Addressing pin numbering
    GPIO.setup(LED_PIN, GPIO.OUT) # Set pin 17 to be an output pin
    print("LED is on")

    #DOUBLE CHECK THIS :redundant since the MQTT client loop handles continuous listening right?
    #while True: # Run forever
        #GPIO.output(LED_PIN, GPIO.HIGH)
    
    send_notification_email()
    

def send_notification_email():
    timestamp = datetime.datetime.now()
    to = ["iotclient26@gmail.com"]
    message = f"The light is on at {timestamp}."

    email_id = 'testingthis2283@gmail.com'
    email_pass = 'gsyx yxmi rnaq lwud'

    msg = EmailMessage()
    msg['Subject'] = 'Light Notification'
    msg['From'] = email_id
    msg['To'] = to
    msg.set_content(message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id, email_pass)
        smtp.send_message(msg)
        
        
    print('Email sent notifying user that light is on.')


# Serve the main HTML file
@app.route('/')
def index():
    return send_from_directory('.', 'main.html')

# Serve static files like images, CSS, JavaScript
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# get and return light intensity
@app.route('/light')
def get_light_intensity():
    return jsonify({'light_intensity' : light_intensity})


# turn on led and send email
@app.route('/led')
def turon_on_led_send_email():
    return jsonify({'led_status' : 'on' , 'email_sent' : True })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
