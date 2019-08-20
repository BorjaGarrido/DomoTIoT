#include <ESP8266WiFi.h> 
#include <PubSubClient.h>

const char* ssid = "MIWIFI_2G_g7GD";
const char* password = "Afpaa3bF";
const char* mqtt_server = "192.168.1.143";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup() {
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  Serial.begin(9600);
}
void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  nivelLuz();
}

void setup_wifi()
{
 Serial.begin(9600);
 // We start by connecting to a WiFi network

 Serial.println();
 Serial.println();
 Serial.print("Conectando a ");
 Serial.println(ssid);

 WiFi.begin(ssid, password);

 while (WiFi.status() != WL_CONNECTED) {
   delay(500);
   Serial.print(".");
 }

 Serial.println("");
 Serial.println("WiFi conectado");
 Serial.println("Direccion IP: ");
 Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Esperando conexion MQTT...");
    // Attempt to connect
    if (client.connect("ESP8266Client-4")) {
      Serial.println("conectado");
      // Once connected, publish an announcement...
      client.publish("casa/luz", "Enviando el primer mensaje");
      // ... and resubscribe
      client.subscribe("casa/luz");
    } else {
      Serial.print("fallo, rc=");
      Serial.print(client.state());
      Serial.println(" intentando en 5 segundos");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void nivelLuz(){

  int sensorValue = analogRead(A0);   // read the input on analog pin 0

  float voltage = sensorValue * (5.0 / 1023.0);   // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V)

  Serial.println(sensorValue);

  Serial.println(voltage);   // print out the value you read 

  long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    snprintf (msg, 75, "Vol %0.2f", voltage);
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish("casa/luz", msg);

    delay(1000);
  }

  delay(1000);
  
}
