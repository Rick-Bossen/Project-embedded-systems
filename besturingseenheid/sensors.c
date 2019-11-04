#include "main.h"

#define LIGHT_PIN PINC3
#define TEMPERATURE_PIN PINC4

check_temperature(){
	uint8_t temperature = (uint8_t)((TEMPERATURE_PIN * 5.0 / 1024.0) - 0.5) * 100;

	if(temperature > 0){
		current_temperature = temperature;
		if(current_unit == -1){
			current_unit = TEMPERATURE;
		}
		
		if(current_unit == TEMPERATURE){
			if((current_status == CLOSED) & (current_temperature >= temperature_open)){
				roll(OPENED)
			}else if((current_status == OPENED) & (current_temperature <= temperature_close)){
				roll(CLOSED)
			}
		}
		
	}
}

check_light(){
	uint8_t light = (uint8_t)LIGHT_PIN * 100;
	
	if(light > 0){
		current_light = light;
		if(current_unit == -1){
			current_unit = LIGHT;
		}
		
		if(current_unit == LIGHT){
			if((current_status == CLOSED) & (current_light >= light_open)){
				roll(OPENED)
			}else if((current_status == OPENED) & (current_light <= light_close)){
				roll(CLOSED)
			}
		}
		
	}
}