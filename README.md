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
   
   

  
