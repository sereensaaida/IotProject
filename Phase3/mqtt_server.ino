#include <WiFi.h>
#include <WiFiMulti.h>
#include <PubSubClient.h> // Include PubSubClient for MQTT

// Wi-Fi and MQTT configuration
WiFiMulti wifiMulti;
const char* mqttServer = "192.168.0.181"; // Replace with your broker's address
const int mqttPort = 1883; // Default MQTT port

// MQTT client
WiFiClient espClient;
PubSubClient client(espClient);

// Pin definitions
const int photoPin = 34; // Analog pin for photoresistor
const int ledPin = 2;    // Digital pin for LED

// Variables
int lightIntensity = 0; // Raw ADC value
bool emailSent = false;

// Function prototypes
void reconnect();
void readLightIntensity();
void publishLightIntensity();
void handleThreshold();

// Setup function
void setup() {
    // Initialize serial communication
    Serial.begin(115200);

    // Initialize LED and photoresistor
    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, LOW);

    // Add Wi-Fi networks to WiFiMulti
    wifiMulti.addAP("TP-Link_2AD8", "14730078");

    // Attempt to connect to a Wi-Fi network
    Serial.print("Connecting to Wi-Fi");
    while (wifiMulti.run() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("";)
    Serial.println("Connected to Wi-Fi");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    delay(500);

    // Configure MQTT server
    client.setServer(mqttServer, mqttPort);

    // Reconnect to MQTT broker
    reconnect();
}

// Main loop
void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();

    // Read light intensity
    readLightIntensity();

    // Handle threshold logic and LED status
    handleThreshold();

    // Publish light intensity to MQTT broker
    publishLightIntensity();

    delay(1000); // Delay for stability
}

// Function to reconnect to the MQTT broker
void reconnect() {
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        if (client.connect("ESP32Client")) { // No username/password needed
            Serial.println("connected");
            // Subscribe to any topics if needed
            client.subscribe("light/commands");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" retrying in 5 seconds...");
            delay(5000);
        }
    }
}

// Function to read light intensity
void readLightIntensity() {
    lightIntensity = analogRead(photoPin); // Get raw ADC value
    Serial.print("Light Intensity: ");
    Serial.println(lightIntensity);
}

// Function to handle LED status and email simulation
void handleThreshold() {
  if (lightIntensity < 400 && !emailSent) {
    digitalWrite(ledPin, HIGH);          // Turn LED on
    client.publish("led/status", "on");  // Notify RPi about LED status
    emailSent = true;                    // Simulate email sent
  } else if (lightIntensity >= 400) {
    digitalWrite(ledPin, LOW);            // Turn LED off
    client.publish("led/status", "off");  // Notify RPi about LED status
    emailSent = false;
  }
}

// Function to publish light intensity to MQTT broker
void publishLightIntensity() {
    char intensityStr[8];
    snprintf(intensityStr, sizeof(intensityStr), "%d", lightIntensity);
    client.publish("lightintensity", intensityStr);
    Serial.println("Published light intensity to MQTT.");
}
