// Esta es la librería para utilizar las funciones de red del ESP8266
#include <ESP8266WiFi.h> 
#include <PubSubClient.h>
#include <SimpleDHT.h>

int pinDHT22 = 5;
SimpleDHT22 dht22(pinDHT22);

const char* ssid = "RedWifi";
const char* password = "PassWifi";
const char* mqtt_server = "IpServer";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
 
void setup() {
  pinMode(pinDHT22, INPUT);     // Initialize the pinDHT22 pin as an output
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  Serial.begin(9600);
}

void loop() {
 
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  HumTemp();

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
    if (client.connect("ESP8266Client-1")) {
      Serial.println("conectado");
      // Once connected, publish an announcement...
      client.publish("casa/temperatura", "Enviando el primer mensaje");
      // ... and resubscribe
      client.subscribe("casa/temperatura");
    } else {
      Serial.print("fallo, rc=");
      Serial.print(client.state());
      Serial.println(" intentando en 5 segundos");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
 
void HumTemp() {
  
  float temperature = 0;
  float humidity = 0;
  
  int err = SimpleDHTErrSuccess;
  if ((err = dht22.read2(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Lectura del DHT22 fallida, error="); Serial.println(err);delay(2000);
    return;
  }
  
  Serial.print((float)temperature); Serial.print(" *C, ");
  Serial.print((float)humidity); Serial.println(" RH%");

  long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    snprintf (msg, 75, "Hum %0.2lf Temp %0.2lf", humidity, temperature);
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish("casa/temperatura", msg);

    delay(1500);
  }

  delay(1500);
}
