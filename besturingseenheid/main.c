#include <avr/io.h>

#include "main.h"
#include "uart.h"
#include "sunblind.h"
#include "scheduler.h"

// TODO remove later TEMPORARY VALUES
char current_unit = MANUAL;

uint8_t current_temperature = 19;
uint8_t current_light = 40;

// Random values don't copy in later code
uint8_t light_open;
uint8_t light_close;
uint8_t temperature_open;
uint8_t temperature_close;

void randomize_temp_values(){
	current_unit = rand() % 2;
	current_temperature = rand() % 30;
	current_light = rand() % 200;

	// Random values don't copy in later code
	light_open = rand() % 30;
	light_close = rand() % 10;
	temperature_open = rand() % 15;
	temperature_close = rand() % 30;
}

// END TEMPORARY CODE
void route_instruction(){
	if(has_input()){
		uint8_t input = receive();
		uint8_t code = input >> 4;
		
		if(code == SET_UNIT){
			uint8_t unit = input & 0x07;
			//set_unit(input)
		}else if(code == ROLL){
			uint8_t direction = input & 0x01;
			roll(direction);
		}else if (code == SET_UNIT_RANGE){
			uint8_t unit = input & 0x07;
			uint8_t minimum = receive();
			uint8_t maximum = receive();
			//set_unit_range(unit, minimum, maximum)
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
	// TODO remove randomize
	randomize_temp_values();
	
	// Status: Opened, Closed, Expanding, Collapsing (2 bits min.)
	transmit((STATE_INFO << 4)|current_status);
	// Current distance (7 bits min.)
	transmit(current_distance);
	
	// Current Unit: Manual, Light of Temperature (3 bits min.)
	transmit((UNIT_INFO << 4)|current_unit);
	
	// TODO add if statement depending on the unit existing
	
	// Temperature info:
	transmit_unit_values(TEMPERATURE, temperature_open, temperature_close, current_temperature);
	
	// Light info:
	transmit_unit_values(LIGHT, light_open, light_close, current_light);

	transmit('\r');
	transmit('\n');
}

void init(){
	// UART
	uart_init();
	
	DDRB = 0xFF; // Set port B to output
	DDRC = 0x00 | ULTRASONIC_TRIGGER; // Set ultrasonic trigger to output
	current_status = CLOSED;
	
	// Scheduler
	SCH_Init_T1();
	SCH_Add_Task(route_instruction, 0, 5); // Check every 50ms for input
	SCH_Add_Task(transmit_status, 0, 6000); // Send status every 60s
	SCH_Add_Task(check_sunblind_position, 0, 50); // Checking state every 500ms
	SCH_Start();
}

int main(void)
{
	// TODO remove later
	srand(time());
	
   init();
   while(1) {
	   SCH_Dispatch_Tasks();
   }
   
   return 0;
}