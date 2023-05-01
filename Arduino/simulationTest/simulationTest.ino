//Arduino simulation Limpiaplayas TMR 2023

//global variables for communication
String msg; 
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
  //IDDLE
  //Serial.println(msg.lenght());  
   
  //sea avoid
  if (msg == "S") {
    seaAvoid();
  }
  else if(msg == "CD"){//can Detect
    canDetect();  
  }
  else if(msg == "C"){//can Collect
    canCollect();
  }
  else if (msg == "T"){//deposit can -> Throw
    deposit();
  }
  else if (msg == "I"){//looking -> Iddle
    looking();
  }
  
  delay(50);
  
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
