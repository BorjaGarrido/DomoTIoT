#define SS_PIN 4  //D2
#define RST_PIN 5 //D1

// Esta es la librería para utilizar las funciones de red del ESP8266
#include <ESP8266WiFi.h> 
#include <PubSubClient.h>

#include <SPI.h>
#include <MFRC522.h>

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
int statuss = 0;
int out = 0;

const char* ssid = "MIWIFI_2G_g7GD";
const char* password = "Afpaa3bF";
const char* mqtt_server = "192.168.1.143";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;


void setup() 
{
  Serial.begin(9600);   // Initiate a serial communication
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
}
void loop() 
{
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  UsuarioRFID();
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
    if (client.connect("ESP8266Client-3")) {
      Serial.println("conectado");
      // Once connected, publish an announcement...
      client.publish("casa/rfid", "Enviando el primer mensaje");
      // ... and resubscribe
      client.subscribe("casa/rfid");
    } else {
      Serial.print("fallo, rc=");
      Serial.print(client.state());
      Serial.println(" intentando en 5 segundos");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void UsuarioRFID(){
// Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  //Show UID on serial monitor
  Serial.println();
  Serial.print(" UID tag :");
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  Serial.println();
  if (content.substring(1)) //change UID of the card that you want to give access
  {
    Serial.println(" Usuario detectado ");
    Serial.println(" -Bienvenido- ");
    delay(1000);
    statuss = 1;
  }

  char UID[15];
  content.substring(1).toCharArray(UID, 15);

  long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    snprintf (msg, 75, "UID Tag %s", UID);
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish("casa/rfid", msg);
    delay(1000);
  }

}
