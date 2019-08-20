// Esta es la librería para utilizar las funciones de red del ESP8266
#include <ESP8266WiFi.h> 
#include <PubSubClient.h>
#include <MQ2.h>

//change this with the pin that you use
int pin = A0;
float lpg, co, smoke;

MQ2 mq2(pin);

const char* ssid = "MIWIFI_2G_g7GD";
const char* password = "Afpaa3bF";
const char* mqtt_server = "192.168.1.143";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup(){
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  mq2.begin();
  Serial.begin(9600);
}

void loop(){

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  calidadAire();
 
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
    if (client.connect("ESP8266Client-2")) {
      Serial.println("conectado");
      // Once connected, publish an announcement...
      client.publish("casa/aire", "Enviando el primer mensaje");
      // ... and resubscribe
      client.subscribe("casa/aire");
    } else {
      Serial.print("fallo, rc=");
      Serial.print(client.state());
      Serial.println(" intentando en 5 segundos");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void calidadAire(){
 /*read the values from the sensor, it returns
  *an array which contains 3 values.
  * 1 = LPG in ppm
  * 2 = CO in ppm
  * 3 = SMOKE in ppm
  */
  mq2.read(false); //set it false if you don't want to print the values in the Serial

  lpg = mq2.readLPG();

  co = mq2.readCO();

  smoke = mq2.readSmoke();

  Serial.print("LPG: ");
  Serial.print(lpg);
  Serial.println("ppm");
  Serial.print("C0: ");
  Serial.print(co);
  Serial.println("ppm");
  Serial.print("SMOKE: ");
  Serial.print(smoke);
  Serial.println("ppm");

  long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    snprintf (msg, 75, "LPG %0.2lf% \t C0 %0.2lf \t SMOKE %0.2lf", lpg, co, smoke);
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish("casa/aire", msg);
    delay(100);
  }

  delay(100);
}
