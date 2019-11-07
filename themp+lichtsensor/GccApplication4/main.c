/*
 * GccApplication4.c
 *
 * Created: 2-11-2019 12:54:49
 * Author : shand
 */

#include <avr/io.h>
#include "PORTPIN.h"
int light_vaule;
int themp_vaule;





int main(void)
{
	DDRC = 0b00000000;


    while (1)
    {
		light_vaule = LIGHT_PIN;
		themp_vaule = THEMP_PIN;
		// berekening voor thempratuur in graden Celsius
		float voltage = themp_vaule * 5.0;
		voltage /= 1024.0;
		float themprature = (voltage - 0.5)*100;
		if (themprature>20)
		{
			PORTB = LED_THEMP;
		}
		else if (light_vaule > 25)
		{
			PORTB = LED_LIGHT;
		}
    }
}

