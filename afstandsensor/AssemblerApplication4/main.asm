;
; AssemblerApplication4.asm
;
; Created: 16-10-2019 12:10:17
; Author : shand
;
#include <avr/io.h>

int main(void)
{
	DDRD = 0b11111111;
	DDRB = 0b00000000;
	while(1){
		int temp = PINB & 0b00000011;
		if(temp != 0b00000000){
			turnOnLed(temp);
		}
	}
	return 0;
}

void turnOnLed(temp){
	PORTD = temp;
}
