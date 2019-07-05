#include <ax12.h>
#include <stdlib.h>
#define GetTorque(id) (ax12GetRegister(id, AX_PRESENT_LOAD_L, 2))


void setup() {
  Serial.begin(115200);
   SetPosition(1,512);
   SetPosition(2,512);
}

void loop()
{

  if (Serial.available())  
  {
    char caract;
    char message[10] = {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '};
    caract = (char)Serial.read();
    
    /*  Load the buffer into message until it find a ';'  */
    int i = 0;
    while(caract != (int)';' && caract != -1)
    {
      delay(1);
      message[i] = caract;

      caract = (char)Serial.read();
      i = i + 1;
    }

    /*  Split the message into 2 parts, the id and the target position  */
    bool flag = false;
    int count = 0;
    char ido[2] = {' ', ' '};
    char pos[10] = {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '};

    for(i=0; i < sizeof(message); i++)
    {
      if (flag ==false && message[i] >= (int)'0' && message[i] <= (int)'9')
      {
        ido[i] = message[i];
        count = count + 1;

      }
      else if(flag == true && message[i] >= (int)'0' && message[i] <= (int)'9')
      {      delay(5);
        pos[count] = message[i];
        count = count + 1;
      }
      else
      {
        flag = true;
      }
    }
    /*  Convert the id and the position in int  */
    int id = atoi(ido);
    int angle = atoi(pos);
    
    /*  If the id is equal to 0 then we send the actual position and torque of the motors from id = 1 to angle  */
    if(id == 0)
    {
      String data = "";
      
      for(i=1; i<=angle; i++)
      {
        data += (String)i;
        data += ":";
        data += (String)(int)(GetPosition(i)/2.84);
        data += ":"; 
        data += (String)(int)(GetTorque(i) * 0.1);
        if(i < angle){
         data += "/"; 
        }       
      }
      Serial.println(data);


    }
    else{
      /*  If id is not 0 it a aplly the position stored in angle to the motor with id equal to id   */
      SetPosition(id, (int)angle*2.84);
    }
    

  }

}
