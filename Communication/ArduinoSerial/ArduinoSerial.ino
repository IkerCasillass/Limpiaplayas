String nom = "Arduino";
String msg;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  readSerialPort();
  msg.replace("\n", "");

  if (msg == "data") {
    sendData();
  }else if(msg=="led0"){
    digitalWrite(LED_BUILTIN,LOW);
    Serial.print(" Arduino set led to LOW");
  }else if(msg=="led1"){
    digitalWrite(LED_BUILTIN,HIGH);
    Serial.print(" Arduino set led to HIGH");
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
  //write data ledState x sensor1 x sensor2
  Serial.print(digitalRead(LED_BUILTIN));
}