double distanceCm = 0;
unsigned long durationMicroSec = 0;
int triggerPin = 13;
int echoPin = 12;
void setup() {
  // put your setup code here, to run once:
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  
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
        Serial.println(-1.0) ;
    } 
    else {
        Serial.println(distanceCm);
    }
    delay(500);
}
