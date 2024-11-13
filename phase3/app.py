from flask import Flask, send_from_directory, request, jsonify
import paho.mqtt.client as mqtt


app = Flask(__name__)

light_intensity = 0

#initialize MQTT client
mqtt_client = mqtt.Client()

def on_message(client,userdata,msg):
    global light_intensity
    
    #get the value from the message
    light_intensity = msg.payload.decode("utf-8")
    print(light_intensity)

#set up the connection and subscribe to the light topic that is published from the code for the esp32
def mqtt_setup():
    mqtt_client.connect('localhost',1883)
    #change topic name once esp32 code has been written
    mqtt_client.subscribe("lightintensity")
    #handle incoming messages from the light topic -> called automatically by paho-mqtt
    mqtt_client.on_message = on_message
    #listen for messages
    mqtt_client.loop_start()
    
mqtt_setup()


# Serve the main HTML file
@app.route('/')
def index():
    return send_from_directory('.', 'main.html')

# Serve static files like images, CSS, JavaScript
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# get and return light intensity
@app.route('/light')
def get_light_intensity():
    return jsonify({'light_intensity' : light_intensity})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
