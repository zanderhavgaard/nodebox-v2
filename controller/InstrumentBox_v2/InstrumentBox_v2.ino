// revised and simplified Nodebox v1 / v2 controller
// @Author: Zander Havgaard >> pezh@itu.dk

String controller_num = "02";

boolean debug = false;

int buttonPin = 2;
int buttonState = 1;
int analogValue = 0;
int analog_pin = 5;
String charArray[] = {"A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k"};
int save_pin = 3;
int play_pin = 4;
int save_pin_state = 0;
int play_pin_state = 0;
boolean play_save_bool = false;
String char_to_send = "";

void setup() {
Serial.begin(9600); // Initiate serial
delay(500);
pinMode(analog_pin, INPUT);
pinMode(buttonPin, INPUT);
pinMode(save_pin, INPUT);
pinMode(play_pin, INPUT);
}

void loop() {
  play_pin_state = LOW;
  save_pin_state = LOW;
  play_pin_state = digitalRead(play_pin);
  save_pin_state = digitalRead(save_pin);

  /*if (save_pin_state == HIGH){ 
    play_save_bool = true;
    if (debug){Serial.println("true");}
  }
  else {
    play_save_bool = false;
    if (debug){Serial.println("false");}
  }*/
  
  if (play_pin_state == HIGH){ //&& save_pin_state == LOW){
    play_save_bool = false;
    if (debug){Serial.println("false");}
  }
  else if (save_pin_state == HIGH){ //&& save_pin_state == HIGH){
    play_save_bool = true;
    if (debug){Serial.println("true");}
  }

  char_to_send = "";
    
  buttonState = digitalRead(buttonPin); // Reads the input from the button
  analogValue = analogRead(5); // Reads the input from the softpot
  int y = map(analogValue, 0, 1023, 0, 35); // maps the output of from the softpot, to something corresponding to our charArray[]
  char_to_send = charArray[y];

  if (buttonState == HIGH){
    if (!play_save_bool){
      Serial.println("$" + controller_num + "|p#" + char_to_send +"^"); 
      delay(250);
    }
    else if (play_save_bool){
      Serial.println("$" + controller_num + "|s#" + char_to_send + "^"); 
      delay(250);
    }    
  }
  delay(100);
}

