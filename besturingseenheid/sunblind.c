#include <avr/io.h>
#define F_CPU 16e6
#include <util/delay.h>
#include "main.h"
#include "sunblind.h"
#include "uart.h"

uint8_t measure_distance(){
	uint8_t distance_cm = 0;
	PINC = 0x00;
	
	PORTC &= ~ULTRASONIC_TRIGGER;
	_delay_ms(2);
	PORTC |= ULTRASONIC_TRIGGER;
	_delay_us(10);
	PORTC &= ~ULTRASONIC_TRIGGER;
	loop_until_bit_is_set(PINC, PORTC1);
	TCNT1 = 0;
	loop_until_bit_is_clear(PINC, PORTC1);
	uint16_t time = TCNT1;
	distance_cm = time / 4;
	
	return distance_cm;
}

void check_sunblind_position(){
	uint8_t distance = measure_distance();
	uint8_t control_distance = measure_distance();
	
	uint8_t difference = distance - control_distance;
	if(difference > -2 && difference < 2){
		current_distance = distance;
		
		if(current_status == EXPANDING && distance > 30){
			current_status = OPENED;
		}else if(current_status == COLLAPSING && distance < 10){
			current_status = CLOSED;
		}
	}
	set_leds();
}

void roll(char direction){
	if(direction == CLOSED && current_status == OPENED){
		current_status = COLLAPSING;
	}else if(direction == OPENED && current_status == CLOSED){
		current_status = EXPANDING;
	}
}


void set_leds(){
	if(current_status == OPENED || current_status == EXPANDING){
		PORTB |= LED_GREEN;
		PORTB &= ~LED_RED;
	}else if (current_status == CLOSED || current_status == COLLAPSING){
		PORTB |= LED_RED;
		PORTB &= ~LED_GREEN;
	}
	
	if (current_status == EXPANDING || current_status == COLLAPSING){
		PORTB ^= LED_YELLOW;
	}else{
		PORTB &= ~LED_YELLOW;
	}
}