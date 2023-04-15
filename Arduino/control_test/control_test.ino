//Arduino pseudo control by comands Limpiaplayas TMR 2023

#include <Servo.h>
Servo FR; //front right servo
Servo FL; //front left servo
Servo BR; //back right servo
Servo BL; //back left servo
Servo door; //door servo

//global variables for communication
String msg; 
String nom = "Arduino";

//Motor 1 front left
int FLM = 7;
int RPWM1 = 22;
int LPWM1 = 24;

//Motor 2 front right
int FRM = 8;
int RPWM2 = 26;
int LPWM2 = 28;

//Motor 3 back left
int BLM = 9;
int RPWM3 = 30;
int LPWM3 = 32;

//Motor 4 back right
int BRM = 10;
int RPWM4 = 34;
int LPWM4 = 36;

//Motor 5 blades
int BM = 11;
int RPWM5 = 38;
int LPWM5 = 40;

void setup()
{
  //Motor1 front left
  pinMode(FLM, OUTPUT);
  pinMode(RPWM1, OUTPUT);
  pinMode(LPWM1, OUTPUT);
  //Motor2 front right
  pinMode(FRM, OUTPUT);
  pinMode(RPWM2, OUTPUT);
  pinMode(LPWM2, OUTPUT);
  //Motor3 back left
  pinMode(BLM, OUTPUT);
  pinMode(RPWM3, OUTPUT);
  pinMode(LPWM3, OUTPUT);
  //Motor4 back right
  pinMode(BRM, OUTPUT);
  pinMode(RPWM4, OUTPUT);
  pinMode(LPWM4, OUTPUT);
  //Motor5 blades
  pinMode(BM, OUTPUT);
  pinMode(RPWM5, OUTPUT);
  pinMode(LPWM5, OUTPUT);

  //Servos all set to standby position calibrate range
  //front right
  FR.attach(2);
  FR.write(90); 
  //front left
  FL.attach(3);
  FL.write(0);
  //back right
  BR.attach(4);
  BR.write(90);
  //back left
  BL.attach(5);
  BL.write(90);
  //door servo
  door.attach(6);
  door.write(0);

  //serial begin
  Serial.begin(9600);  
  robot_stop();
}

void loop()
{
  readSerialPort();

  if (msg == "stop") {
    robot_stop();
  }
  else if(msg == "forward"){
    forward();
  }
  else if(msg == "backward"){
    backward();
  }
  else if(msg == "turnR"){
    turnRight();  
  }
  else if(msg == "turnL"){
    turnLeft();
  }
  
  delay(500);
  
}

//COMMUNICATION
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

//BASIC MOVEMENT
void backward()
{
  //Motor1 front left
  analogWrite(FLM, 100);
  digitalWrite(RPWM1, LOW);
  digitalWrite(LPWM1, HIGH);
  //Motor2 front right
  analogWrite(FRM, 100);
  digitalWrite(RPWM2, LOW);
  digitalWrite(LPWM2, HIGH);
  //Motor3 back left
  analogWrite(BLM, 100);
  digitalWrite(RPWM3, LOW);
  digitalWrite(LPWM3, HIGH);
  //Motor4 back right
  analogWrite(BRM, 100);
  digitalWrite(RPWM4, LOW);
  digitalWrite(LPWM4, HIGH);
}

void forward()
{
  //Motor1 front left
  analogWrite(FLM, 100);
  digitalWrite(RPWM1, HIGH);
  digitalWrite(LPWM1, LOW);
  //Motor2 front right
  analogWrite(FRM, 100);
  digitalWrite(RPWM2, HIGH);
  digitalWrite(LPWM2, LOW);
  //Motor3 back left
  analogWrite(BLM, 100);
  digitalWrite(RPWM3, HIGH);
  digitalWrite(LPWM3, LOW);
  //Motor4 back right
  analogWrite(BRM, 100);
  digitalWrite(RPWM4, HIGH);
  digitalWrite(LPWM4, LOW);
}

void turnRight(){

  //front right
  FR.write(180); 
  //front left
  FL.write(90);
  //back right
  BR.write(90);
  //back left
  BL.write(90);
  
  //Motor1 front left
  analogWrite(FLM, 50);
  digitalWrite(RPWM1, HIGH);
  digitalWrite(LPWM1, LOW);
  //Motor2 front right
  analogWrite(FRM, 50);
  digitalWrite(RPWM2, LOW);
  digitalWrite(LPWM2, HIGH);
  //Motor3 back left
  analogWrite(BLM, 100);
  digitalWrite(RPWM3, LOW);
  digitalWrite(LPWM3, LOW);
  //Motor4 back right
  analogWrite(BRM, 100);
  digitalWrite(RPWM4, LOW);
  digitalWrite(LPWM4, LOW);
}

void turnLeft(){
  
  //front right
  FR.write(180); 
  //front left
  FL.write(90);
  //back right
  BR.write(90);
  //back left
  BL.write(90);

   //Motor1 front left
  analogWrite(FLM, 50);
  digitalWrite(RPWM1, LOW);
  digitalWrite(LPWM1, HIGH);
  //Motor2 front right
  analogWrite(FRM, 50);
  digitalWrite(RPWM2, HIGH);
  digitalWrite(LPWM2, LOW);
  //Motor3 back left
  analogWrite(BLM, 100);
  digitalWrite(RPWM3, LOW);
  digitalWrite(LPWM3, LOW);
  //Motor4 back right
  analogWrite(BRM, 100);
  digitalWrite(RPWM4, LOW);
  digitalWrite(LPWM4, LOW);
}

void robot_stop()
{
  //Motor1 front left
  analogWrite(FLM, 100);
  digitalWrite(RPWM1, LOW);
  digitalWrite(LPWM1, LOW);
  //Motor2 front right
  analogWrite(FRM, 100);
  digitalWrite(RPWM2, LOW);
  digitalWrite(LPWM2, LOW);
  //Motor3 back left
  analogWrite(BLM, 100);
  digitalWrite(RPWM3, LOW);
  digitalWrite(LPWM3, LOW);
  //Motor4 back right
  analogWrite(BRM, 100);
  digitalWrite(RPWM4, LOW);
  digitalWrite(LPWM4, LOW);
}
