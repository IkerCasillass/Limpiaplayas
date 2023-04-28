String nom = "Arduino";
String msg;

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  readSerialPort();
  msg.replace("\n", "");

  if (msg == "data") {
    sendData();
  }else if(msg=="led0"){
    digitalWrite(LED_BUILTIN,LOW);
    Serial1.print(" Arduino set led to LOW");
    //Serial.print(" Arduino set led to LOW");
  }else if(msg=="led1"){
    digitalWrite(LED_BUILTIN,HIGH);
    Serial1.print(" Arduino set led to HIGH");
    //Serial.print(" Arduino set led to HIGH");
  }
}

void readSerialPort() {
  msg = "";
  if (Serial1.available()) {
    delay(10);
    while (Serial1.available() > 0) {
      msg += (char)Serial1.read();
    }
    Serial1.flush();
  }
}

void sendData() {
  //write data ledState x sensor1 x sensor2
  Serial1.print(digitalRead(LED_BUILTIN));
}
