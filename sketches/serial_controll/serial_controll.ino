int in1=9;
int in2=8;
int in3=7;
int in4=6;
/*define channel enable output pins*/
int ENA=10;
int ENB=5;

void _mForward(int l_speed, int r_speed)
{
  analogWrite(ENA,l_speed);
  analogWrite(ENB,r_speed);
  digitalWrite(in1,LOW);//digital output
  digitalWrite(in2,HIGH);
  digitalWrite(in3,LOW);
  digitalWrite(in4,HIGH);
 Serial.println("move!");
}

void _mStop()
{
  digitalWrite(ENA,LOW);
  digitalWrite(ENB,LOW);
  Serial.println("Stop!");
} 

void setup() {
  Serial.begin(9600);
  pinMode(in1,OUTPUT);
  pinMode(in2,OUTPUT);
  pinMode(in3,OUTPUT);
  pinMode(in4,OUTPUT);
  pinMode(ENA,OUTPUT);
  pinMode(ENB,OUTPUT);
  _mForward(100, 100);
  delay(1000);
   _mStop();

}

void loop(){
  //Check if there is any data available to read
  if(Serial.available() >= 3){
    //read only one byte at a time
      uint8_t c = Serial.read();
      uint8_t l = Serial.read();
      uint8_t r = Serial.read();

      _mForward(l, r);
      Serial.print(l);
      Serial.print("|");
      Serial.print(r);
      Serial.print("\n");
      delay(30);
  }
}
