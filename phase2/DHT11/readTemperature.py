from flask import Flask,send_from_directory,request,jsonify
import time
from Freenove_DHT import DHT
import os
import smtplib
from email.message import EmailMessage


app = Flask(__name__)

DHTPin = 17     #define the pin of DHT11

# function to read temperature and humidity using DHT11
def read_temperature_and_humidity():
    dht = DHT(DHTPin)
    time.sleep(1)
    for i in range(0,15):            
            chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            if (chk == 0):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                temperature= dht.getTemperature()
                humidity = dht.getHumidity()
                return temperature,humidity
            time.sleep(0.1)
    return None,None

# function to send the user an email if the temperature is more than 24 degrees celsius
def send_email(temperature):
    to=["jpizzuco22@gmail.com"]
    message="The current temperature is %.2f °C. Would you like to turn on the fan?"%(temperature)
        
    email_id='testingthis2283@gmail.com'
    email_pass='gsyx yxmi rnaq lwud'

    msg=EmailMessage()
    msg['Subject']='Sending Email'
    msg['From']=email_id
    msg['To']= to
    msg.set_content(message)

    with smtplib.SMTP_SSL('smtp.gmail.com',465)as smtp:
            smtp.login(email_id,email_pass)
            smtp.send_message(msg)
            smtp.quit()

#set the root as the html file, put html file on Flask's server
@app.route('/')
def index():
    return send_from_directory('../','main.html')

#serve the image files
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../',filename)

#check temperature and send email if temperature is greater than 24 degrees celsius
@app.route('/checktemperature')
def check_temperature():
    temperature,humidity = read_temperature_and_humidity();
    
    if temperature is not None:
        if temperature > 24:
            send_email(temperature)
            
        return jsonify({'temperature':temperature,'humidity': humidity})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True,)