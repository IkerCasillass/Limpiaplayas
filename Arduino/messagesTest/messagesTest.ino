//Arduino pseudo control by commands Limpiaplayas TMR 2023

//global variables for communication
String msg; 
String nom = "Arduino";

void setup()
{
  //serial begin
  Serial.begin(9600);  
}

void loop()
{
  
  readSerialPort();
  msg.replace("\n", "");

  if (msg == "D") {
    sendDebbugData("Right");
    
  }else if(msg == "I"){
    sendDebbugData("Left");
     
  }
  else if(msg == "C"){
    sendDebbugData("blob centered");
    
  }
  else if (msg == "B"){
    sendDebbugData("looking");
    
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

void sendDebbugData(String cmd) {
  //write data
  Serial.print(nom);
  Serial.print(" doing: ");
  Serial.print(cmd);
}
