//Motor 1
int PWM1 = 7;
int RPWM1 = 22;
int LPWM1 = 24;

void setup()
{
  //Motor1
  pinMode(PWM1, OUTPUT);
  pinMode(RPWM1, OUTPUT);
  pinMode(LPWM1, OUTPUT);
  
  Serial.begin(9600);  
  motor_stop();
}

void loop()
{
  int i;
  for(i = 0; i <= 255; i= i+10)
  { //clockwise rotation
    analogWrite(PWM1,i);
    digitalWrite(LPWM1,LOW);
    digitalWrite(RPWM1,HIGH);
    Serial.print("PWM: ");
    Serial.println(i);
    delay(500);
  }
  delay(500);
  for(i = 0; i <= 255; i= i+10)
  { //counter clockwise rotation
    analogWrite(PWM1,i);
    digitalWrite(RPWM1,LOW);
    digitalWrite(LPWM1,HIGH);
    delay(500);
  }
  delay(500);
}


void motor_ccw()
{
  analogWrite(PWM1,100);
  digitalWrite(RPWM1,LOW);
  digitalWrite(LPWM1,HIGH);
}

void motor_cw()
{
  analogWrite(PWM1,100);
  digitalWrite(RPWM1,HIGH);
  digitalWrite(LPWM1,LOW);
}

void motor_stop()
{
  digitalWrite(RPWM1,LOW);
  digitalWrite(LPWM1,LOW);
  analogWrite(PWM1,0);
}
