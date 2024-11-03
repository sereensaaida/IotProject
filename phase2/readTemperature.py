from flask import Flask, send_from_directory, request, jsonify
import time
from Freenove_DHT import DHT
import os
import smtplib
import email
import imaplib
from email.message import EmailMessage
from motor import turn_on_fan  # Assuming `motor.py` has the function to control fan hardware

app = Flask(__name__)

DHTPin = 17  # Define the pin of DHT11
latest_temperature = None

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

# Function to send an email if temperature is more than 24°C
def send_email(temperature):
    to = ["iotclient26@gmail.com"]
    message = f"The current temperature is {temperature:.2f} °C. Would you like to turn on the fan?"

    email_id = 'testingthis2283@gmail.com'
    email_pass = 'gsyx yxmi rnaq lwud'

    msg = EmailMessage()
    msg['Subject'] = 'Temperature Alert'
    msg['From'] = email_id
    msg['To'] = to
    msg.set_content(message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id, email_pass)
        smtp.send_message(msg)
        
    print('Email sent asking if the fan should be turned on.')

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

    # Select the most recent email
    last_email_id = mail_ids[-1]
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
        return True

    return False

# Serve the main HTML file
@app.route('/')
def index():
    return send_from_directory('.', 'main.html')

# Serve static files like images, CSS, JavaScript
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# Endpoint to check temperature and humidity
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
@app.route('/sendemail')
def send_email_check_for_response():
    global latest_temperature
    
    # Send an email if temperature is above the threshold
    if latest_temperature is not None and latest_temperature > 24:
        send_email(latest_temperature)
        
        # Wait a bit before checking for a response
        time.sleep(60)

        # Check for a "yes" response in email periodically
        for _ in range(10):  # Check 10 times at 10-second intervals
            if check_email_for_yes():
                # Return fan status as "on" if "yes" was received
                return jsonify({'fan_status': 'on'})
            time.sleep(10)

    # Return fan status as "off" if no "yes" response was found
    return jsonify({'fan_status': 'off'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
