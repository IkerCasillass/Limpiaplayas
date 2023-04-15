//Motor 1
int PWM1 = 7;
int RPWM1 = 22;
int LPWM1 = 24;

//Motor 2
int PWM2 = 8;
int RPWM2 = 26;
int LPWM2 = 28;

//Motor 3
int PWM3 = 9;
int RPWM3 = 30;
int LPWM3 = 32;

//Motor 4
int PWM4 = 10;
int RPWM4 = 34;
int LPWM4 = 36;

//Motor 5
int PWM5 = 11;
int RPWM5 = 38;
int LPWM5 = 40;

//Servo1
int PWMS1 = 2;

//Servo2
int PWMS2 = 3;

//Servo3
int PWMS3 = 4;

//Servo4
int PWMS4 = 5;

//Servo5
int PWMS5 = 6;

void setup()
{
  //Motor1
  pinMode(PWM1, OUTPUT);
  pinMode(RPWM1, OUTPUT);
  pinMode(LPWM1, OUTPUT);
  //Motor2
  pinMode(PWM1, OUTPUT);
  pinMode(RPWM1, OUTPUT);
  pinMode(LPWM1, OUTPUT);
  //Motor3
  pinMode(PWM1, OUTPUT);
  pinMode(RPWM1, OUTPUT);
  pinMode(LPWM1, OUTPUT);
  //Motor4
  pinMode(PWM1, OUTPUT);
  pinMode(RPWM1, OUTPUT);
  pinMode(LPWM1, OUTPUT);
  //Motor5
  pinMode(PWM1, OUTPUT);
  pinMode(RPWM1, OUTPUT);
  pinMode(LPWM1, OUTPUT);

  //Servos 
  pinMode(PWMS1, OUTPUT);
  pinMode(PWMS2, OUTPUT);
  pinMode(PWMS3, OUTPUT);
  pinMode(PWMS4, OUTPUT);
  pinMode(PWMS5, OUTPUT);
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
