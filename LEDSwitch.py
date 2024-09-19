from flask import Flask,send_from_directory,request
import RPi.GPIO as GPIO

app = Flask(__name__)

# set GPIO pin 18 to output
GPIO.setmode(GPIO.BCM)
LED= 18
GPIO.setup(LED, GPIO.OUT)

#set the root as the html file, put html file on Flask's server
@app.route('/')
def index():
    return send_from_directory('.','main.html')

#serve the image files
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.',filename)

#if the value received through post is turn_on, turn the LED on
@app.route('/turn_on', methods=['POST'])
def turnOn():
    GPIO.output(LED,GPIO.HIGH)
    return "ON"


#if the value received through post is turn_off, turn the LED off
@app.route('/turn_off', methods=['POST'])
def turnOff():
    GPIO.output(LED,GPIO.LOW)
    return "OFF"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True,)