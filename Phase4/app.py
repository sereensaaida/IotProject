from flask import Flask, send_from_directory, request, jsonify
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from time import sleep
import datetime
import os
import smtplib
import email
import imaplib
from email.message import EmailMessage
import time
from Freenove_DHT import DHT
from motor import turn_on_fan, turn_off_fan
import sqlite3
from database import initialize_db, select_user, initialize_cursor

app = Flask(__name__)

light_intensity = 0
rfid_tag = ""
GPIO.cleanup()
emailRead = False
lightEmailSent = False
userEmailSent = False
userTemp = 0
userLight = 0
fanRunning = False

DHTPin = 20  # Define the pin of DHT11
latest_temperature = None

DB_FILE = "users.db"

#initialize MQTT client
mqtt_client = mqtt.Client()

def on_message(client,userdata,msg):
    topic = msg.topic
    if topic == "lightintensity":
        global light_intensity
        light_intensity = msg.payload.decode("utf-8")
        print(f"Light Intensity: {light_intensity}")
        #TODO: verify topic name with one used to publish the rfid tag
    elif topic == "rfidtag":
        global rfid_tag
        rfid_tag = msg.payload.decode("utf-8")
        print(f"RFID Tag: {rfid_tag}")
    #elif topic == "led/status":
      #  led_status = msg.payload.decode("utf-8")
        #print(f"LED Status: {led_status}")
        #if led_status == "on":
         #   send_notification_email()

#set up the connection and subscribe to the light topic that is published from the code for the esp32
def mqtt_setup():
    mqtt_client.connect('localhost',1883)
    #subscribe to light intensity topic
    mqtt_client.subscribe("lightintensity")
    #subscribe to rfid tag topic
    mqtt_client.subscribe("rfidtag")
    # LED status changes
    #mqtt_client.subscribe("led/status")
    #handle incoming messages from the light topic -> called automatically by paho-mqtt
    mqtt_client.on_message = on_message
    #listen for messages
    mqtt_client.loop_start()
    
mqtt_setup()

# Function to read temperature and humidity using DHT11
def read_temperature_and_humidity():
    dht = DHT(DHTPin)
    time.sleep(1)
    for i in range(15):
        chk = dht.readDHT11()  # Read DHT11 and check if data read is normal
        if chk == 0:
            temperature = dht.getTemperature()
            humidity = dht.getHumidity()
            return temperature, humidity
        time.sleep(0.1)
    return None, None

# Function to read the latest email and check if it contains "yes"
def check_email_for_yes():
    email_id = 'testingthis2283@gmail.com'
    password = 'gsyx yxmi rnaq lwud'
    SERVER = 'imap.gmail.com'

    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(email_id, password)
    mail.select('inbox')

    # Search for unseen emails
    status, data = mail.search(None, '(UNSEEN)')
    mail_ids = data[0].split()

    if not mail_ids:
        return False  # No new emails

     #if there is a new email we change the readStatus to true so as to not accept any other responses
    global emailRead 
    emailRead = True

    # Select the first unseen email
    last_email_id = mail_ids[0]
    status, data = mail.fetch(last_email_id, '(RFC822)')
    raw_email = data[0][1]

    # Parse email to get content
    message = email.message_from_bytes(raw_email)
    mail_content = ''
    if message.is_multipart():
        for part in message.get_payload():
            if part.get_content_type() == 'text/plain':
                mail_content += part.get_payload()
    else:
        mail_content = message.get_payload()

    mail_content = mail_content.lower()
    print(f'Content of latest email: {mail_content}')



    # Check if "yes" is in the content to turn on the fan
    if 'yes' in mail_content:
        turn_on_fan()  # Turn on fan
        return jsonify({'fan_status': 'on'})

        return True
    else:
        return False

def turn_on_led():
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM) # Use BCM Addressing pin numbering
    LED=27
    GPIO.setup(LED, GPIO.OUT)
    GPIO.output(LED, GPIO.HIGH)
    print("LED is on")
    
 
def turn_off_led():
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM) # Use BCM Addressing pin numbering
    LED=27
    GPIO.setup(LED, GPIO.OUT)
    GPIO.output(LED, GPIO.LOW)
    print("LED is off")
       

def send_notification_email(email_subject, email_message):
    to = ["iotclient26@gmail.com"]
    message = email_message

    email_id = 'testingthis2283@gmail.com'
    email_pass = 'gsyx yxmi rnaq lwud'

    msg = EmailMessage()
    msg['Subject'] = email_subject
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
    return send_from_directory('.', 'login.html')

# Serve static files like images, CSS, JavaScript
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# get and return light intensity
@app.route('/light')
def get_light_intensity():
    return jsonify({'light_intensity' : light_intensity})

# get and return the rfid tag
@app.route('/profile')
def profile():
    return jsonify({'rfid_tag' : rfid_tag})

#retrieve the user info from the dashoard
@app.route('/userinfo')
def user_info():
    #call initialize db function
    initialize_cursor()
    initialize_db()
    global rfid_tag
    print(rfid_tag)
    #if a card hasn't yet been scanned
    if(rfid_tag is ""):
        return jsonify({'user_exists' : 'not yet'})

    user = select_user(rfid_tag) 
    print(user)

    if(user is None):
        return jsonify({'user_exists' : 'false'})

    print(f"{user[1]} 'rfid' {user[0]}, 'db_temp': {user[2]}, 'db_light' {user[3]}")    

    global userTemp
    userTemp = user[2]

    global userLight
    userLight =user[3]
    
    global userEmailSent
    if userEmailSent ==False:
        timestamp = datetime.datetime.now()
        send_notification_email(f"Welcome { user[1]}",f"User { user[1]} entered on on {timestamp.strftime('%B %d,%Y at %I:%M %p')}.")
        userEmailSent =True

    return jsonify({'user_exists' : 'true', 'username' : user[1], 'rfid' : user[0], 'db_temp': user[2], 'db_light' : user[3]})
    
# turn on led and send email
@app.route('/led')
def turnon_on_led_send_email():
    turn_on_led()
    timestamp = datetime.datetime.now()
    send_notification_email(f"Light Notification",f"The light was turned on {timestamp.strftime('%B %d,%Y at %I:%M %p')}.")
    return jsonify({'led_status' : 'on' , 'email_sent' : 'true' })

# turn of led 
@app.route('/turnoffled')
def turnoff_led():
    turn_off_led()
    return jsonify({'led_status' : 'off'})

#check temperature and humidity
@app.route('/checktemperature')
def check_temperature():
    global latest_temperature
    temperature, humidity = read_temperature_and_humidity()

    if temperature is not None:
        latest_temperature = temperature
        return jsonify({
            'temperature': temperature,
            'humidity': humidity,
            'fan_status': 'off'
        })

# Endpoint to send email and check for response to turn on fan
@app.route('/sendfanemail')
def send_email_check_for_response():
    global latest_temperature
    global emailRead
    global userTemp
    print(latest_temperature)
    # Send an email if temperature is above the threshold
    if latest_temperature is not None and latest_temperature > userTemp:
        send_notification_email('Temperature Alert', f"The current temperature is {latest_temperature:.2f} °C. Would you like to turn on the fan?")
        
        # Wait a bit before checking for a response
        time.sleep(30)

        # Check for a "yes" response in email periodically
        for _ in range(10):  # Check 10 times at 10-second intervals
             #only read email the first email that the user replies with
            if emailRead == False:
                if check_email_for_yes():
                    # Return fan status as "on" if "yes" was received
                    return jsonify({'fan_status': 'on'})
                time.sleep(10)

    # Return fan status as "off" if no "yes" response was found
    return jsonify({'fan_status': 'off'})

@app.route('/update_user', methods=['POST'])
def update_user():
    rfid_tag = request.json.get('rfid_tag')
    temp_threshold = request.json.get('temp_threshold')
    light_threshold = request.json.get('light_threshold')

    # Call the function in database.py to update the database
    insert_or_update_temperature_and_light(rfid_tag, temp_threshold, light_threshold)
    
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001, debug=True)
    finally:
        GPIO.cleanup()
