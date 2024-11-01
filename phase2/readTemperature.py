from flask import Flask,send_from_directory,request,jsonify
import time
from Freenove_DHT import DHT
import os
import smtplib
import email
import imaplib
from email.message import EmailMessage
from motor import turn_on_fan


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
    to=["iotclient26@gmail.com"]
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
            
        
#function to read email, checks latest email in inbox for 'yes'
def check_email_for_yes():
    email_id = 'testingthis2283@gmail.com'
    password = 'gsyx yxmi rnaq lwud'
    SERVER = 'imap.gmail.com'

    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(email_id, password)
    mail.select('inbox')

    #search for unseen emails
    status, data = mail.search(None,'(UNSEEN)')
    mail_ids = data[0].split()

    #select last email in inbox
    last_email_in_inbox = mail_ids[-1]
    status, data = mail.fetch(last_email_in_inbox, '(RFC822)')
    raw_email = data[0][1]

    #parse email into a message object so we can read it
    message = email.message_from_bytes(raw_email)
    mail_from = message['from']
    mail_subject = message['subject']

    if message.is_multipart():
                    mail_content = ''

    for part in message.get_payload():
                if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                            
    print(f'From: {mail_from}')
    print(f'Subject: {mail_subject}')
    print(f'Content: {mail_content}')
    
    mail_content = mail_content.lower()
    
    if 'yes' in mail_content:
        turn_on_fan()
        return True
    

    
#set the root as the html file, put html file on Flask's server
@app.route('/')
def index():
    return send_from_directory('.','main.html')

#serve the image files
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.',filename)

#check temperature and send email if temperature is greater than 24 degrees celsius
@app.route('/checktemperature')
def check_temperature():
    temperature,humidity = read_temperature_and_humidity();
    
    if temperature is not None:
        if temperature > 24:
            send_email(temperature)
            
            #wait 60 seconds before checking inbox
            sleep(60)
            
            for i in range(10):
                email_response = check_email_for_yes()
                #method only returns True if yes has been found in the email
                if email_response:
                    #response is json array containing fan status that we need for the main.html
                    return  jsonify({'temperature': temperature,'humidity': humidity,'fan_status': 'on'})
                
                sleep(10) #check again in 10 seconds
                
        return jsonify({'temperature':temperature,'humidity': humidity,'fan_status': 'off'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True,)