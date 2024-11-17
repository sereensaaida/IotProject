import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use BCM Addressing pin numbering
LED=17
GPIO.setup(LED, GPIO.OUT) # Set pin 17 to be an output pin
while True: # Run forever
GPIO.output(LED, GPIO.HIGH) # Turn on
sleep(1) # Sleep for 1 second
GPIO.output(LED, GPIO.LOW) # Turn off
sleep(1) # Sleep for 1 secondv