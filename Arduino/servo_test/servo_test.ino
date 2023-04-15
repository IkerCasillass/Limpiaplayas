#include <Servo.h>
Servo myservo;   
String msg; 
String nom = "Arduino";

void setup() {
  myservo.attach(9);
  myservo.write(90); 
  delay(1000);
}

void loop() {

  myservo.write(90); 
  delay(1000);
  myservo.write(180); 
  delay(2000);
  

}

void calibration(){
  for (int i = 0; i<180; i++){
    myservo.write(i); 
    delay(20);
  }
  delay(1000);
  for (int i = 180; i>0; i--){
    myservo.write(i); 
    delay(20);
  }
  delay(1000);
}
