//Arduino simulation Limpiaplayas TMR 2023

//global variables for communication
String msg, msg1, msg2; 
String nom = "Arduino";

//hoop goal
int red = 8;

//sea detected
int blue = 9;

//can detected
int yellow = 10;

//looking
int green = 11;

void setup()
{
  //Motor1 front left
  pinMode(red, OUTPUT);
  //Motor2 front right
  pinMode(blue, OUTPUT);
  //Motor3 back left
  pinMode(yellow, OUTPUT);
  //Motor4 back right
  pinMode(green, OUTPUT);

  //serial begin
  Serial.begin(9600);  
}

void loop()
{
  
  readSerialPort();
  msg.replace("\n", "");

  //sea avoid
  if (msg1 == "S") {
    seaAvoid();
    //if (msg2 == "R") {
    //}
  }
  // else if(msg1 == "CD"){//can Detect
  //   canDetect();  
  // }
  else if(msg1 == "C"){//can Collect
    canCollect();
    if (msg2 == "R"){
      canCenter1();
    }
    else if (msg2 == "L") {
      canCenter2();
    }
    else if (msg2 == "C"){
          //hoop goal
      digitalWrite(red, HIGH);
      //sea
      digitalWrite(blue, HIGH);
      //can
      digitalWrite(yellow, HIGH);
      //looking
      digitalWrite(green, HIGH);
    }
  }
  // else if (msg1 == "T"){//deposit can -> Throw
  //   deposit();
  // }
  else if (msg1 == "I"){//looking -> Iddle
    looking();
  }
  else if (msg1 == "H"){ // detected hoop
    hoopDetect();
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

    if (msg.length() > 1){
      msg1 = msg.substring(0, 1);
      msg2 = msg.substring(1);
    }
    else {
      msg1 = msg;
      Serial.print("Unico mensaje " + msg1);
    }
      
    Serial.flush();
  }
}

void sendData(String cmd) {
  //write data
  Serial.print(nom);
  Serial.print(" doing: ");
  Serial.print(cmd);
}

void canDetect()
{
  
  //hoop goal
  digitalWrite(red, LOW);
  //sea
  digitalWrite(blue, LOW);
  //can
  digitalWrite(yellow, HIGH);
  //looking
  digitalWrite(green, LOW);
}

void canCollect()
{
  bool state = HIGH;
  for (int i = 0; i < 3; i++){
    //can
    digitalWrite(yellow, state);
    state = !state;
    delay(200);
  }
}

void canCenter1() {
  digitalWrite(green, HIGH);
}

void canCenter2() {
  digitalWrite(green, HIGH);
  digitalWrite(red, HIGH);
}
void seaDetect(){
  //hoop goal
  digitalWrite(red, LOW);
  //sea
  digitalWrite(blue, HIGH);
  //can
  digitalWrite(yellow, LOW);
  //looking
  digitalWrite(green, LOW);
}

void seaAvoid()
{
  
  bool state = HIGH;
  for (int i = 0; i < 3; i++){
    //can
    digitalWrite(blue, state);
    state = !state;
    delay(200);
  }
}

void looking(){

  //hoop goal
  digitalWrite(red, HIGH);
  //sea
  digitalWrite(blue, HIGH);
  //can
  digitalWrite(yellow, HIGH);
  //looking
  digitalWrite(green, HIGH);
  
}

void robot_stop()
{
  
  //hoop goal
  digitalWrite(red, LOW);
  //sea
  digitalWrite(blue, LOW);
  //can
  digitalWrite(yellow, LOW);
  //looking
  digitalWrite(green, LOW);
}

void hoopDetect(){
  //hoop goal
  digitalWrite(red, HIGH);
  //sea
  digitalWrite(blue, LOW);
  //can
  digitalWrite(yellow, LOW);
  //looking
  digitalWrite(green, LOW);
}

void deposit() { // open gate
  bool state = HIGH;
  for (int i = 0; i < 3; i++){
    //can
    digitalWrite(red, state);
    state = !state;
    delay(200);
  }
}





//BASIC MOVEMENT
// void backward(){

  
//   //Motor1 front left
//   analogWrite(FLM, 100);
//   digitalWrite(RPWM1, LOW);
//   digitalWrite(LPWM1, HIGH);
//   //Motor2 front right
//   analogWrite(FRM, 100);
//   digitalWrite(RPWM2, LOW);
//   digitalWrite(LPWM2, HIGH);
//   //Motor3 back left
//   analogWrite(BLM, 100);
//   digitalWrite(RPWM3, LOW);
//   digitalWrite(LPWM3, HIGH);
//   //Motor4 back right
//   analogWrite(BRM, 100);
//   digitalWrite(RPWM4, LOW);
//   digitalWrite(LPWM4, HIGH);
// }

// void forward(){


//   //Motor1 front left
//   analogWrite(FLM, 100);
//   digitalWrite(RPWM1, HIGH);
//   digitalWrite(LPWM1, LOW);
//   //Motor2 front right
//   analogWrite(FRM, 100);
//   digitalWrite(RPWM2, HIGH);
//   digitalWrite(LPWM2, LOW);
//   //Motor3 back left
//   analogWrite(BLM, 100);
//   digitalWrite(RPWM3, HIGH);
//   digitalWrite(LPWM3, LOW);
//   //Motor4 back right
//   analogWrite(BRM, 100);
//   digitalWrite(RPWM4, HIGH);
//   digitalWrite(LPWM4, LOW);
// }

// void turnRight(){

//   // turn engine
//    //Motor1 front left
//   analogWrite(FLM, 50);
//   digitalWrite(RPWM1, HIGH);
//   digitalWrite(LPWM1, LOW);
//   //Motor2 front right
//   analogWrite(FRM, 50);
//   digitalWrite(RPWM2, HIGH);
//   digitalWrite(LPWM2, LOW);
//   //Motor3 back left
//   analogWrite(BLM, 50);
//   digitalWrite(RPWM3, LOW);
//   digitalWrite(LPWM3, HIGH);
//   //Motor4 back right
//   analogWrite(BRM, 50);
//   digitalWrite(RPWM4, LOW);
//   digitalWrite(LPWM4, HIGH);

  
//   //smooth axis wheel
//   //index for decrement
//   int j = 90;
//   for(int i=90; i<180; i+=5){
//     //front right
//     FR.write(i); 
//     //front left
//     FL.write(j);
//     //back right
//     BR.write(j);
//     //back left
//     BL.write(i);
//     j-=5;
//     delay(100);
//   }
//   delay(100);  
//   // Iniciar giro
//   //Motor1 front left
//   analogWrite(FLM, 50);
//   digitalWrite(RPWM1, HIGH);
//   digitalWrite(LPWM1, LOW);
//   //Motor2 front right
//   analogWrite(FRM, 50);
//   digitalWrite(RPWM2, LOW);
//   digitalWrite(LPWM2, HIGH);
//   //Motor3 back left
//   analogWrite(BLM, 50);
//   digitalWrite(RPWM3, LOW);
//   digitalWrite(LPWM3, HIGH);
//   //Motor4 back right
//   analogWrite(BRM, 50);
//   digitalWrite(RPWM4, HIGH);
//   digitalWrite(LPWM4, LOW);
 
// }

// void turnLeft(){

//   // turn engine
//     //Motor1 front left
//   analogWrite(FLM, 50);
//   digitalWrite(RPWM1, HIGH);
//   digitalWrite(LPWM1, LOW);
//   //Motor2 front right
//   analogWrite(FRM, 50);
//   digitalWrite(RPWM2, HIGH);
//   digitalWrite(LPWM2, LOW);
//   //Motor3 back left
//   analogWrite(BLM, 50);
//   digitalWrite(RPWM3, LOW);
//   digitalWrite(LPWM3, HIGH);
//   //Motor4 back right
//   analogWrite(BRM, 50);
//   digitalWrite(RPWM4, LOW);
//   digitalWrite(LPWM4, HIGH);

   

//   //smooth axis wheel
//   //index for decrement
//   int j = 90;
//   for(int i=90; i<180; i+=5){
//     //front right
//     FR.write(i); 
//     //front left
//     FL.write(j);
//     //back right
//     BR.write(j);
//     //back left
//     BL.write(i);
//     j-=5;
//     delay(100);
//     }
//   delay(100);
//   // Inica giro izquierda
//   //Motor1 front left
//   analogWrite(FLM, 50);
//   digitalWrite(RPWM1, LOW);
//   digitalWrite(LPWM1, HIGH);
//   //Motor2 front right
//   analogWrite(FRM, 50);
//   digitalWrite(RPWM2, HIGH);
//   digitalWrite(LPWM2, LOW);
//   //Motor3 back left
//   analogWrite(BLM, 50);
//   digitalWrite(RPWM3, HIGH);
//   digitalWrite(LPWM3, LOW);
//   //Motor4 back right
//   analogWrite(BRM,50);
//   digitalWrite(RPWM4, LOW);
//   digitalWrite(LPWM4, HIGH);
// }


// void align(){
//   Serial.print("Align");

//   //Motor1 front left
//   analogWrite(FLM, 50);
//   digitalWrite(RPWM1, LOW);
//   digitalWrite(LPWM1, HIGH);
//   //Motor2 front right
//   analogWrite(FRM, 50);
//   digitalWrite(RPWM2, LOW);
//   digitalWrite(LPWM2, HIGH);
//   //Motor3 back left
//   analogWrite(BLM, 50);
//   digitalWrite(RPWM3, HIGH);
//   digitalWrite(LPWM3, LOW);
//   //Motor4 back right
//   analogWrite(BRM, 50);
//   digitalWrite(RPWM4, HIGH);
//   digitalWrite(LPWM4, LOW);

//  //smooth axis wheel
//   //index for decrement
//   int j = 0;
//   for(int i=180; i>=90; i-=5){
//     //front right
//     FR.write(i); 
//     //front left
//     FL.write(j);
//     //back right
//     BR.write(j);
//     //back left
//     BL.write(i);
//     j+=5;
//     delay(100);
//   }
//   robot_stop();
// }


// void deposit() { // open gate
//   for (int i = 0; i<90; i++){
//     door.write(i); 
//     delay(20);
//   }

//   delay(5000);

//   for (int i = 90; i>0; i--){
//     door.write(i); 
//     delay(20);
//   }
// }

