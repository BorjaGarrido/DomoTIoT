// Esta es la librería para utilizar las funciones de red del ESP8266
#include <ESP8266WiFi.h> 
#include <PubSubClient.h>
#include <Servo.h>

#define pinServo 2

const char* ssid = "RedWifi";
const char* password = "PassWifi";
const char* mqtt_server = "IpServer";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

Servo myservo;  // crea el objeto servo
 
int pos = 0;    // posicion del servo
 
void setup() {
   myservo.attach(pinServo);  // vincula el servo al pin digital 9
  Serial.begin(9600);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}
 
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
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
    if (client.connect("ESP8266Client-6")) {
      Serial.println("conectado");
      // Once connected, publish an announcement...
      client.publish("casa/puerta", "Enviando el primer mensaje");
      // ... and resubscribe
      client.subscribe("casa/puerta");
    } else {
      Serial.print("fallo, rc=");
      Serial.print(client.state());
      Serial.println(" intentando en 5 segundos");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
 
  // Switch on the motor if an 0 was received as first character
  if ((char)payload[0] == '0') {
    for (pos = 0; pos <= 90; pos += 1){
      myservo.write(pos);             
      delay(15);                       
    }
  } if((char)payload[0] == '1') {
    for (pos = 90; pos >= 0; pos -= 1){
      myservo.write(pos);             
      delay(15);                       
   }
  }
}
