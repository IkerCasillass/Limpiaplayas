#include <DHT.h>
#include <DHT_U.h>
// Definimos el pin digital donde se conecta el sensor
#define DHTPIN A0
#define DHTTYPE DHT11
#define pinled 2
DHT dht(DHTPIN, DHTTYPE);
String command;

void setup() {
  // Inicializamos comunicación serie
  Serial.begin(9600);
  // Comenzamos el sensor DHT
  dht.begin();
  pinMode(pinled, OUTPUT);
}
 
void loop() {
  // Esperamos 5 segundos entre medidas
  delay(5000);
  // Leemos la temperatura en grados centígrados (por defecto)
  float t = dht.readTemperature();
  Serial.print(t);
  //digitalWrite(pinled, HIGH);
//  if (t>24) {
//      digitalWrite(pinled, HIGH);
//      Serial.print('on');
//  }
//  else {
//    digitalWrite(pinled, HIGH);
//    Serial.print('off');
//  }
  
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();
      if (command.equals("on")) {
        digitalWrite(pinled, HIGH);
      }
      else if (command.equals("off")) {
      digitalWrite(pinled, LOW);
    }
    else {
      digitalWrite(pinled, LOW);
    }
  }

  delay(1000);
}
