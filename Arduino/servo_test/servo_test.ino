#include <Servo.h>
Servo myservo;   
String msg; 
String nom = "Arduino";

void setup() {
  myservo.attach(2);
  myservo.write(0); 
  delay(1000);
}

void loop() {

  calibration();
  

}

void calibration(){
  for (int i = 0; i<90; i++){
    myservo.write(i); 
    delay(20);
  }
  delay(1000);
  for (int i = 90; i>0; i--){
    myservo.write(i); 
    delay(20);
  }
  delay(1000);
}
