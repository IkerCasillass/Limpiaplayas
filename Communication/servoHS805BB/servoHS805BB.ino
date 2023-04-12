#include <Servo.h>
Servo myservo;   
String msg; 
String nom = "Arduino";

void setup() {
  Serial.begin(9600);
  myservo.attach(9);
  myservo.write(0); 
}

void loop() {

  readSerialPort();

    if (msg == "giro") {
      sendData();
      myservo.write(90); 
    }
    else if(msg == "avanza"){
      sendData();
      myservo.write(0); 
    }
    delay(500);
 

}

void readSerialPort() {
  msg = "";
  if (Serial.available()) {
    delay(10);
    while (Serial.available() > 0) {
      msg += (char)Serial.read();
    }
    Serial.flush();
  }
}

void sendData() {
  //write data
  Serial.print(nom);
  Serial.print(" Angle set to: ");
  Serial.print(msg);
}