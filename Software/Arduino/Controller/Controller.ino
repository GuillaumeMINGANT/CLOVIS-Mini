
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
boolean buffer_is_full = false;

unsigned int id_len = 0;
unsigned int pos_len = 0;
unsigned char * id;  
unsigned int * pos;
unsigned char * data;

void clear_buffer()
{
  top_buffer = 0;         
}

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
    for(int i = 1; i < (top_buffer / 3) - 1; i++){
      id[i - 1] = buffer[i * 3];
      int new_pos = buffer[i * 3 + 1] * 256 + buffer[i * 3 + 2];
      if(new_pos < 0){
        pos[i - 1] = 0;
      }
      else if(new_pos > 1023){
        pos[i - 1] = 1023;
      }
      else{
        pos[i - 1] = new_pos;
      }
    }
    id_len = (top_buffer / 3) - 1;

    pos_len = id_len;
    clear_buffer();     
    buffer_is_full = false;
    return true;
  }

  if(top_buffer == 7){  // Send motor's data
    data[0] = (char)255; 
    data[1] = (char)255;
    data[2] = (char)255; 
    for(char i=0; i<buffer[3]; i++)
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

    for (int i = 0; i < (NB_MOTORS * 7) + 6; i++){
      Serial.write(data[i]);
    }  
  }
  clear_buffer();         
  buffer_is_full = false;
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

    if(!buffer_is_full){
      buffer[top_buffer] = Serial.read();
      top_buffer += 1;


      if(top_buffer == 3){
        if(buffer[0] != 255 || buffer[1] != 255 || buffer[2] != 255){         
          buffer[0] = buffer[1];
          buffer[1] = buffer[2];
          top_buffer -= 1;          
        }
      }
      if(top_buffer > 6){
        if(buffer[top_buffer - 3] == 254 && buffer[top_buffer - 2] == 254 && buffer[top_buffer - 1] == 254){
          buffer_is_full = true;           
        }
      }


    }
    else{     
      if(read_message()){
        move_motors();      
      }
    }


  }
}


