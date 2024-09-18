import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED=18
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
lightState = pull from js

if lightState == 1:
    GPIO.output(LED,GPIO.HIGH)
elif lightState == 0:
    GPIO.output(LED,GPIO.LOW)

