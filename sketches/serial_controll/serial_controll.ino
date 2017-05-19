const uint8_t header = 0x7E;
const uint8_t bufferSize = 3;

uint8_t buffer[bufferSize];
uint8_t readCounter;
uint8_t isHeader;

//Flag that helps us restart counter when we first find header byte
uint8_t firstTimeHeader; 

int in1 = 9;
int in2 = 8;
int in3 = 7;
int in4 = 6;
int ENA = 11;
int ENB = 5;

String incomingByte = "";

void _mForward(int l_speed, int r_speed)
{
 analogWrite(ENA,l_speed);
 analogWrite(ENB,r_speed);
 digitalWrite(in1,LOW);
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

  readCounter = 0;
  isHeader = 0;
  firstTimeHeader = 0;
  
  _mStop();
}

void loop(){
  //Check if there is any data available to read
  if(Serial.available() > 0){
    //read only one byte at a time
    uint8_t c = Serial.read();
    
    //Check if header is found
    if(c == header){
      //We must consider that we may sometimes receive unformatted data, and
      //given the case we must ignore it and restart our reading code.
      //If it's the first time we find the header, we restart readCounter
      //indicating that data is coming.
      //It's possible the header appears again as a data byte. That's why
      //this conditional is implemented, so that we don't restart readCounter
      //and corrupt the data. 
      if(!firstTimeHeader){
        isHeader = 1;
        readCounter = 0;
        firstTimeHeader = 1;
      }
    }
    
    //store received byte, increase readCounter
    buffer[readCounter] = c;
    readCounter++;
    
    //prior overflow, we have to restart readCounter
    if(readCounter >= bufferSize){
      readCounter = 0;
      
      //if header was found
      if(isHeader){
//        //get checksum value from buffer's last value, according to defined protocol
//        uint8_t checksumValue = buffer[4];
//        
//        //perform checksum validation, it's optional but really suggested
//        if(verifyChecksum(checksumValue)){
//          //We'll employ PWM to control each RGB Component in the Led
//          // TODO CMD
//        }

        Serial.write(buffer[0]);
        Serial.write(buffer[1]);
        Serial.write(buffer[2]);
        
        //restart header flag
        isHeader = 0;
        firstTimeHeader = 0;
      }
    }
  }
}

//This a common checksum validation method
//We perform a sum of all bytes, except the one that corresponds to the original
//checksum value. After summing we need to AND the result to a byte value.
uint8_t verifyChecksum(uint8_t originalResult){
  uint8_t result = 0;
  uint16_t sum = 0;
  
  for(uint8_t i = 0; i < (bufferSize - 1); i++){
    sum += buffer[i];
  }
  result = sum & 0xFF;
  
  if(originalResult == result){
     return 1;
  }else{
     return 0;
  }
}
