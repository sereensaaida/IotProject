# Project Description
By utilizing sensors, actuators, motors, Single-board computers, and micro-controllers, students design and simulate a smart home. They capture environmental information and make a decision based on received data. They also develop access control and occupancy systems and transfer all data to the cloud or a local server. Finally, they design and develop a web-based IoT dashboard to control and monitor the system.

# PHASE 1
  Our Main intention was to complete research/Make use of flask (a python module that allows for application develop using an extendable core), in order to be able to make the parallel between our existing python code
  that manipulates our bread board and its visual output through an html live server.

  Our current submission includes css and html files corresponding to the visual aspect of the phase (manipulating the switch to toggle the lightbulb), assets containing images for our html and a python code
  allowing us to modify the physical light bulb's state when manipulating the visual one.

# Testing Phase 1
1) In order to test Phase 1, the user must have a simple LED circuit configured on their breadboard (connected to GPIO port 18) and have Flask installed

    Installing Flask can be done by running the command:
 
               pip install Flask

3) Next the LEDSwitch.py script must be run.
   
   This can be done by running navigating to the project's directory and running the command:
   
                 python3 LEDSwitch.py

4) To access the dashboard, the user must visit: http://localhost:5001/
   
5) Once the user has accessed the dashboard, they must simply click the switch to turn the LED on their breadboard on and off.
   
   # Phase 2
   The requirements of this phase are:
-  DHT 11 Temperature and Humidity sensor
-  Resistors
-  Wires
-  Breadboard
- Raspberry-Pi
-  DC motor and driver
This phase has the following steps:
-  Data capture
-  Data communication
- Data presentation
### Data Capture:
By a DHT-11 sensor, current temperature and humidity are captured.
### Data communication:
The captured data is transferred to an RPi
### Data Presentation:
Temperature and Humidity values are displayed on the dashboard using gauges

# Testing Phase 2 
In order to test Phase 2 the user must have the DHT11 (using GPIO port 18) and dc motor (using ports 22, 27 and 17) circuit properly configured on their breadboard 
1) The readTemperature.py script must be run.
   
   This can be done by running navigating to the project's directory and running the command:
   
                 python3 readTemperature.py

2) To access the dashboard, the user must visit: http://localhost:5001/

   The room's temperature and humidity levels will then be read. If the temperature exceeds 24°C , an email will be sent to the user :iotclient26@gmail.com asking them if they wish to turn on the fan. If the user replies 'yes' to this email, the fan (dc motor) will be turned on.
   


  
