#include <ax12.h>
#include <BioloidController.h>

#define GetTorque(id) (ax12GetRegister(id, AX_PRESENT_LOAD_L, 2))
#define GetSpeed(id) (ax12GetRegister(id, AX_PRESENT_SPEED_L, 2))

const unsigned int NB_MOTORS =  22;
const unsigned int BUFFER_SIZE = 256;
const unsigned char END_TRANSMIT = ';';
const unsigned char FIRST_ID = 2;

unsigned int top_buffer = 0;
unsigned char * buffer;

unsigned int id_len = 0;
unsigned int pos_len = 0;
unsigned char * id;  
unsigned int * pos;
unsigned char * data;

char find_lsb(int value){
  return (char)(value % 256);
}

char find_msb(int value){
  value = value - (value % 256);
  return (char)(value / 256);
}

boolean read_message(){
  /*
   *  Read the message if possible and write the required values in id and pos.
   */
  if(top_buffer % 3 == 0 && top_buffer != 0){
    for(int i = 0; i < top_buffer / 3; i++){
      id[i] = buffer[i * 3];
      pos[i] = buffer[i * 3 + 1] * 256 + buffer[i * 3 + 2];
    }
    id_len = top_buffer / 3;
    pos_len = id_len;
    return true;
  }
  
  if(top_buffer == 1){  // Send motor's data
    data[0] = (char)255; 
    data[1] = (char)255;
    data[2] = (char)255; 
    for(char i=0; i<buffer[0]; i++)
    {
      data[(i * 7) + 3] = (int)(i + FIRST_ID);
      
      int temp = (int)GetPosition(i + FIRST_ID);
      data[(i * 7) + 4] = find_msb(temp);
      data[(i * 7) + 5] = find_lsb(temp);
      
      temp = (int)GetSpeed(i + FIRST_ID);
      data[(i * 7) + 6] = find_msb(temp);
      data[(i * 7) + 7] = find_lsb(temp);
      
      temp = (int)GetTorque(i + FIRST_ID);
      data[(i * 7) + 8] = find_msb(temp);
      data[(i * 7) + 9] = find_lsb(temp);
      } 
      
    data[(NB_MOTORS * 7) + 3] = 254; 
    data[(NB_MOTORS * 7) + 4] = 254;
    data[(NB_MOTORS * 7) + 5] = 254;
    //DEBUG
      
    for (int i = 0; i < (NB_MOTORS * 7) + 6; i++){
      Serial.write(data[i]);
    }
    //Serial.print('\n');


    //fin DEBUG      
    }
      
      
    
  return false;
}


void move_motors(){
  /*
     *  Send the positions stores in pos to the motor wich id stores in id.
   */
  int temp;
  int length = 4 + (id_len * 3);   // 3 = id + pos(2byte)
  int checksum = 254 + length + AX_SYNC_WRITE + 2 + AX_GOAL_POSITION_L;
  setTXall();
  ax12write(0xFF);
  ax12write(0xFF);
  ax12write(0xFE);
  ax12write(length);
  ax12write(AX_SYNC_WRITE);
  ax12write(AX_GOAL_POSITION_L);
  ax12write(2);
  for(int i=0; i<id_len; i++)
  {
    temp = pos[i];
    checksum += (temp&0xff) + (temp>>8) + id[i]; 
    ax12write(id[i]);
    ax12write(temp&0xff);
    ax12write(temp>>8);

  } 
  ax12write(0xff - (checksum % 256));
  setRX(0);

  delay(10);
}


void setup(){
  Serial.begin(115200);
  buffer = (unsigned char *) malloc(BUFFER_SIZE * sizeof(unsigned char));
  id = (unsigned char *) malloc(NB_MOTORS * sizeof(unsigned char));
  pos = (unsigned int *) malloc(NB_MOTORS * sizeof(unsigned int));
  data = (unsigned char *) malloc(((NB_MOTORS * 7) + 6) * sizeof(unsigned char));
}


void loop(){
  if(Serial.available()){

    int temp = Serial.read();
    //Serial.println(temp);
    if(temp != (int)END_TRANSMIT){
      buffer[top_buffer] = temp;
      top_buffer += 1;
    }
    else{     
      if(read_message()){
         move_motors();
       
      }
      top_buffer = 0;
    }


  }
    delay(1);


}

