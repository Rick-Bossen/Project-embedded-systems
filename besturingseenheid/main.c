#include <avr/io.h>
#include "uart.h"
#include "scheduler.h"

// @TODO All routing can be moved to a different file later depending on the rest of the code

// instructions
#define SET_UNIT 1
#define ROLL 2
#define SET_UNIT_RANGE 3

// units
#define MANUAL 0
#define LIGHT 1
#define TEMPERATURE 1

// direction
#define OUT 0
#define IN 1

void route_instruction(){
	if(has_input()){
		uint8_t input = receive();
		uint8_t code = input >> 4;
		if(code == SET_UNIT){
			uint8_t unit = input & 0x07;
			//set_unit(input)
		}else if(code == ROLL){
			uint8_t direction = input & 0x01;
			//roll(direction)
		}else if (code == SET_UNIT_RANGE){
			uint8_t unit = input & 0x07;
			uint8_t minimum = receive();
			uint8_t maximum = receive();
			//set_unit_range(unit, minimum, maximum)
		}
	}
}

void transmit_status(){
	// @TODO Bijvullen wanneer er meer werkelijke gegevens bekend zijn.
}

void init(){
	// UART
	uart_init();
	
	// Scheduler
	SCH_Init_T1();
	SCH_Add_Task(route_instruction, 0, 5); // Check every 50ms for input
	SCH_Add_Task(transmit_status, 0, 6000); // Send status every 60s
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

