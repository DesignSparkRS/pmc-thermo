/*
 Basic MQTT example no Authentication

  - connects to an MQTT server
  - publishes "hello world" to the topic "test/out"
  - subscribes to the topic "test/in"
  - toggles I/O according to message payload
*/

#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>
#include <Arduino_MachineControl.h>
using namespace machinecontrol;

#define CH00 0

// Update these with values suitable for your network.
byte mac[] = { 0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0xED };
IPAddress ip(192, 168, 1, 61);  // PMC IP
IPAddress server(192, 168, 1, 60);  // Broker IP

void callback(char* topic, byte* payload, unsigned int length) {
  String buffer = "";
  for (int i = 0; i < length; i++) {
    buffer += (char)payload[i];
  }

  if (buffer.length() > 0) {
    if (buffer == "OFF")
      digital_outputs.set(CH00, LOW);
    else if (buffer == "ON")
      digital_outputs.set(CH00, HIGH);
  }
}

EthernetClient ethClient;
PubSubClient client(server, 1883, callback, ethClient);

void setup() {
  Ethernet.begin(mac, ip);
  digital_outputs.setLatch();

  if (client.connect("arduinoClient")) {
    client.publish("test/out", "hello world");
    client.subscribe("test/in");
  }
}

void loop() {
  client.loop();
}
