from flask import Flask, jsonify, request
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
LED= 18
GPIO.setup(LED_PIN, GPIO.OUT)

@app.route('/turnon', methods=['POST'])
def turnOn():
    GPIO.output(LED,GPIO.HIGH)
    return "ON"

@app.route('/turnoff', methods=['POST'])
def turnOff():
    GPIO.output(LED,GPIO.HIGH)
    return "OFF"

if __name__ == '__main__':
    app.run(debug=True, port=5000)