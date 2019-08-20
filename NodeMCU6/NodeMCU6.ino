// Esta es la librería para utilizar las funciones de red del ESP8266
#include <ESP8266WiFi.h> 
#include <PubSubClient.h>

#define led 5

const char* ssid = "MIWIFI_2G_g7GD";
const char* password = "Afpaa3bF";
const char* mqtt_server = "192.168.1.143";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
 
void setup() {
  pinMode(led, OUTPUT);     // Initialize the led pin as an output
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
      client.publish("casa/led", "Enviando el primer mensaje");
      // ... and resubscribe
      client.subscribe("casa/led");
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
  Serial.print("Mensaje recibido [");
  Serial.print(topic);
  Serial.print("] ");
  int pwmVal;
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    payload[length] = '\0'; // Make payload a string by NULL terminating it.
    pwmVal = atoi((char *)payload);
  }
  Serial.println();

  Serial.println(pwmVal);
  
  analogWrite(led,pwmVal);
  
  delay(10);

}
