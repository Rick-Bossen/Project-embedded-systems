/*
 * GccApplication4.c
 *
 * Created: 28-10-2019 20:27:45
 * Author : shand
 */ 

#include <avr/io.h>
#include <util/delay.h>



//Beginning of Auto generated function prototypes by Atmel Studio
double meetAfstand();
int ongeveerGelijk(double var1, double var2);
//End of Auto generated function prototypes by Atmel Studio

double meet1 = 0.0;
double meet2 = 0.0;

//variabelen voor de functie meetAfstand()
double distanceCm = 0.0;
unsigned long durationMicroSec = 0;
int main (void){
// pinnen declareren
DDRD = 0b00111000;
DDRB = 0b00100000;

	meet1 = meetAfstand();
	_delay_ms(2000);
	meet2 = meetAfstand();

	// er is geen foute waarde gevonden
	if(meet1 != -1 && meet2 != -1){
		//het luik beweegt
		if(!ongeveerGelijk(meet1,meet2)){
			if(meet1<meet2){
				//het luik gaat omhoog
				PORTD = 0b00110000;
			}
			else if(meet1<meet2){
				//het luik gaat omlaag
				PORTD = 0b00011000;		
			}
		}
		// het luik beweegt niet
		else{
			if(meet1<30){
				//het luik is omlaag
				PORTD = 0b00100000;
			}
			else if(meet1>120){
				//het luik is omhoog
				PORTD = 0b00001000;
			}
		}

	}
	_delay_ms(500);
}
//functie om de afstand sensor te besturen, de waarde uit te lezen, en de afstant te berekenen
double meetAfstand(){
	// Om zeker te zijn dat triggerPin LOW is.
	PORTB = 0b00000000;
	_delay_ms(2);
	// Hou de trigger 10 microseconden in, dit is het signaal om de sensor te laaten meten.
	PORTB = 0b00010000;
	_delay_ms(10);
	PORTB = 0b00000000;
	// lezen van de tijd en het berekenen van de aftand
	durationMicroSec = pulseIN();
	distanceCm = durationMicroSec / 2.0 * 0.0343;
	if (distanceCm == 0 || distanceCm > 400) {
		return(-1.0) ;
	}
	else {
		return(distanceCm);
	}
}
//functie om te controleren of de waarden dicht bij elkaar liggen
int ongeveerGelijk(double var1,double var2){
	if(var1-2<var2&&var1+2>var2){
		return(1);
	}
	else{
		return(0);
	}
}


 int pulseIN(){
	int tijd = 0;
	while (PINB4 == 1)
	{
		tijd ++;
	}
	return tijd;
}