#include <WiFi.h>
#include <WiFiMulti.h>
#include <PubSubClient.h> // Include PubSubClient for MQTT
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 5 // SDA Pin on RC522
#define RST_PIN 4 // RST Pin on RC522
MFRC522 rfid(SS_PIN, RST_PIN); // Create MFRC522 instance

// Wi-Fi and MQTT configuration
WiFiMulti wifiMulti;
//const char* mqttServer = "192.168.0.181"; // Replace with your broker's address
//const char* mqttServer = "192.168.2.198";
const char* mqttServer = "192.168.231.99";
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
    //wifiMulti.addAP("TP-Link_2AD8", "14730078");
    wifiMulti.addAP("Galaxy A237E91", "beepbeep");
    //wifiMulti.addAP("BELL986", "766371C4");

    // Attempt to connect to a Wi-Fi network
    Serial.print("Connecting to Wi-Fi");
    while (wifiMulti.run() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("Connected to Wi-Fi");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    delay(500);

    // Configure MQTT server
    client.setServer(mqttServer, mqttPort);

    // Reconnect to MQTT broker
    reconnect();

    SPI.begin(); // Initialize SPI bus
    rfid.PCD_Init(); // Initialize MFRC522 reader
    Serial.println("Place your RFID card near the reader...");
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
    //handleThreshold();

    // Publish light intensity to MQTT broker
    publishLightIntensity();

    delay(1000); // Delay for stability
    handleRFID();
    delay(1000);
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

void handleRFID(){
    // Look for new cards
  if (!rfid.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if (!rfid.PICC_ReadCardSerial()) {
    return;
  }

  // Format the UID into a string
    String uidString = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
        if (rfid.uid.uidByte[i] < 0x10) {
            uidString += "0"; // Add leading zero for single-digit bytes
        }
        uidString += String(rfid.uid.uidByte[i], HEX); // Convert to hexadecimal
        if (i < rfid.uid.size - 1) {
            uidString += " "; // Add separator
        }
    }

    // Print UID to serial monitor
    Serial.print("Card UID: ");
    Serial.println(uidString);

    // Publish UID to MQTT topic
    if (client.publish("rfidtag", uidString.c_str())) {
        Serial.println("RFID UID published successfully.");
    } else {
        Serial.println("Failed to publish RFID UID.");
    }

    // Halt PICC
    rfid.PICC_HaltA();
}
