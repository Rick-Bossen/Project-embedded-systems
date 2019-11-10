#include <avr/io.h>
#define F_CPU 16e6
#include <util/delay.h>
#include "main.h"
#include "sunblind.h"
#include "uart.h"

// Return the distance of the ultrasonic sensor.
uint8_t measure_distance(){
	uint8_t distance_cm = 0;
	PIND = 0x00;
	
	PORTD &= ~ULTRASONIC_TRIGGER;
	_delay_ms(2);
	PORTD |= ULTRASONIC_TRIGGER;
	_delay_us(10);
	PORTD &= ~ULTRASONIC_TRIGGER;
	loop_until_bit_is_set(PIND, PIND5);
	TCNT1 = 0;
	loop_until_bit_is_clear(PIND, PIND5);
	uint16_t time = TCNT1;
	distance_cm = time / 4;
	
	return distance_cm;
}

// Scheduler function: Check the position of the sunblinds
// and store it in the global variables current_distance and current_status
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

// Instruction In: Set the current status based on the direction requested
void roll(char direction){
	if(direction == CLOSED && current_status == OPENED){
		current_status = COLLAPSING;
	}else if(direction == OPENED && current_status == CLOSED){
		current_status = EXPANDING;
	}
}


// Set the LEDs based on the current status
// Closed = Red, Open = Green, Opening = Green and blinking Yellow, Closing = Red and blinking Yellow
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