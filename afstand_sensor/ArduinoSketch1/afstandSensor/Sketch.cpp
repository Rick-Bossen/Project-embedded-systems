/*Begining of Auto generated code by Atmel studio */
#include <Arduino.h>

/*End of auto generated code by Atmel studio */


//Beginning of Auto generated function prototypes by Atmel Studio
double meetAfstand();
bool ongeveerGelijk(double var1, double var2);
//End of Auto generated function prototypes by Atmel Studio

double meet1 = 0.0;
double meet2 = 0.0;

//variabelen voor de functie meetAfstand()
double distanceCm = 0.0;
unsigned long durationMicroSec = 0;

// pinnen declareren
int ledPinGroen = 3;
int ledPinGeel = 4;
int ledPinRood = 5;
int echoPin = 12;
int triggerPin = 13;


void setup() {
  pinMode(ledPinGroen, OUTPUT);
  pinMode(ledPinGeel, OUTPUT);
  pinMode(ledPinRood, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(triggerPin, OUTPUT);
 
  Serial.begin(9600);
}

void loop() {
  meet1 = meetAfstand();
  delay(2000);
  meet2 = meetAfstand();
  Serial.print(meet1);
  Serial.print("  ");
  Serial.println(meet2); 
  // er is geen foute waarde gevonden
  if(meet1 != -1 && meet2 != -1){
  //het luik beweegt
  if(!ongeveerGelijk(meet1,meet2)){
    if(meet1<meet2){
      //het luik gaat omhoog
      digitalWrite(ledPinGroen,HIGH);
      digitalWrite(ledPinGeel,HIGH);
      digitalWrite(ledPinRood,LOW);
      }
    else if(meet1<meet2){
      //het luik gaat omlaag
      digitalWrite(ledPinGroen,LOW);
      digitalWrite(ledPinGeel,HIGH);
      digitalWrite(ledPinRood,HIGH);
      }
  }
  // het luik beweegt niet
  else{
    if(meet1<30){
      //het luik is omlaag
      digitalWrite(ledPinGroen,LOW);
      digitalWrite(ledPinGeel,LOW);
      digitalWrite(ledPinRood,HIGH);
      }
     else if(meet1>120){
      //het luik is omhoog
      digitalWrite(ledPinGroen,HIGH);
      digitalWrite(ledPinGeel,LOW);
      digitalWrite(ledPinRood,LOW);
    }
   }

 }
 delay(500);
}
//functie om de afstand sensor te besturen, de waarde uit te lezen, en de afstant te berekenen
double meetAfstand(){
    // Om zeker te zijn dat triggerPin LOW is.
    digitalWrite(triggerPin, LOW);
    delayMicroseconds(2);
    // Hou de trigger 10 microseconden in, dit is het signaal om de sensor te laaten meten.
    digitalWrite(triggerPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(triggerPin, LOW);
    // lezen van de tijd en het berekenen van de aftand
    durationMicroSec = pulseIn(echoPin, HIGH);
    distanceCm = durationMicroSec / 2.0 * 0.0343;
    if (distanceCm == 0 || distanceCm > 400) {
        return(-1.0) ;
    } 
    else {
        return(distanceCm);
    }
}
//functie om te controleren of de waarden dicht bij elkaar liggen
bool ongeveerGelijk(double var1,double var2){
  if(var1-2<var2&&var1+2>var2){
    return(true);
  }
  else{
    return(false);
  }
}
