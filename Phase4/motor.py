import RPi.GPIO as GPIO
from time import sleep
from flask import jsonify
# Pin configuration
Motor1 = 21  # Enable Pin
Motor2 = 12  # Input Pin
Motor3 = 25  # Input Pin

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(Motor1, GPIO.OUT)
    GPIO.setup(Motor2, GPIO.OUT)
    GPIO.setup(Motor3, GPIO.OUT)

def turn_on_fan():
    print('Fan turning on')
    setup_gpio()
    GPIO.output(Motor1, GPIO.HIGH)
    GPIO.output(Motor2, GPIO.LOW)
    GPIO.output(Motor3, GPIO.HIGH)
    return jsonify({'fan_status': 'on'})
    print('Fan is running...')

def turn_off_fan():
    print('Fan turning off')
    GPIO.output(Motor1, GPIO.LOW)
    GPIO.output(Motor2, GPIO.LOW)
    GPIO.output(Motor3, GPIO.LOW)
    GPIO.cleanup()
    return jsonify({'fan_status': 'off'})
    print('Fan stopped')

if __name__ == "__main__":
    try:
        turn_on_fan()
        # Keep running until interrupted
        while True:
            sleep(1)
    except KeyboardInterrupt:
        turn_off_fan()
