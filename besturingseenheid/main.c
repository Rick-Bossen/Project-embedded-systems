#include <avr/io.h>

#include "main.h"
#include "uart.h"
#include "sunblind.h"
#include "sensors.h"
#include "scheduler.h"

void set_unit(uint8_t unit){
	current_unit = unit;
}

void set_unit_range(uint8_t unit, uint8_t open, uint8_t close){
	if(unit == TEMPERATURE){
		temperature_open = open;
		temperature_close = close;
	}else if(unit == LIGHT){
		light_open = open;
		light_close = close;
	}
}

void route_instruction(){
	if(has_input()){
		uint8_t input = receive();
		uint8_t code = input >> 4;
		
		if(code == SET_UNIT){
			uint8_t unit = input & 0x07;
			set_unit(unit);
		}else if(code == ROLL){
			set_unit(MANUAL); // If manual roll in or out, don't overwrite it again with temperature until changed manually.
			uint8_t direction = input & 0x01;
			roll(direction);
		}else if (code == SET_UNIT_RANGE){
			uint8_t unit = input & 0x07;
			uint8_t minimum = receive();
			uint8_t maximum = receive();
			set_unit_range(unit, minimum, maximum);
		}
	}
}

void transmit_unit_values(char unit, uint8_t open_at, uint8_t close_at, uint8_t current_value){
	transmit((UNIT_VALUE_INFO << 4)|unit);
	transmit(open_at);
	transmit(close_at);
	transmit(current_value);
}

void transmit_status(){	
	// Status: Opened, Closed, Expanding, Collapsing (2 bits min.)
	transmit((STATE_INFO << 4)|current_status);
	// Current distance (7 bits min.)
	transmit(current_distance);
	
	// Current Unit: Manual, Light of Temperature (3 bits min.)
	transmit((UNIT_INFO << 4)|current_unit);
	
	// Temperature info:
	if(current_unit == TEMPERATURE){
		transmit_unit_values(TEMPERATURE, temperature_open, temperature_close, current_temperature);
	}
	// Light info:
	else if(current_unit == LIGHT){
		transmit_unit_values(LIGHT, light_open, light_close, current_light);
	}
	

	transmit('\r');
	transmit('\n');
}

void init(){
	// UART
	uart_init();
	
	DDRB = 0xFF;
	DDRD = 0x00 | ULTRASONIC_TRIGGER;
	
	current_status = CLOSED;
	current_unit = 0xff;
	
	light_open = 50;
	light_close = 100;
	temperature_open = 15;
	temperature_close = 25;
	
	// ADC init
	ADCSRA |= (1<<ADPS2);
	ADMUX |= (1<<REFS0);
	ADCSRA |= (1<<ADEN);
	ADCSRA |= (1<<ADSC);
	
	// Scheduler
	SCH_Init_T1();
	SCH_Add_Task(route_instruction, 0, 5); // Check every 50ms for input
	SCH_Add_Task(transmit_status, 0, 600); // Send status every 60s
	SCH_Add_Task(check_sunblind_position, 0, 50); // Checking state every 500ms
	SCH_Add_Task(check_temperature, 0, 400); // Checking state every 40s
	SCH_Add_Task(check_light, 0, 300); // Checking state every 30s
	SCH_Start();
}

int main(void)
{	
   init();
   while(1) {
	   SCH_Dispatch_Tasks();
   }
   
   return 0;
}