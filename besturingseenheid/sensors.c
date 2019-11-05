#include "main.h"
#include "sunblind.h"
#include "sensors.h"

uint16_t read_adc(uint8_t channel)
{
	ADMUX &= 0xF0;                 
	ADMUX |= channel;
	ADCSRA |= (1<<ADSC);
	loop_until_bit_is_set(ADCSRA, ADSC);
	return ADCW;
}

void check_temperature(){
	float voltage = read_adc(TEMPERATURE) * 5.0 / 1024.0;
	uint8_t temperature = (uint8_t)(voltage - 0.5) * 100;

	if(temperature > 0){
		current_temperature = temperature;
		if(current_unit == 0xff){
			current_unit = TEMPERATURE;
		}
		
		if(current_unit == TEMPERATURE){
			if((current_status == CLOSED) & (current_temperature >= temperature_open)){
				roll(OPENED);
			}else if((current_status == OPENED) & (current_temperature <= temperature_close)){
				roll(CLOSED);
			}
		}
	}
}

void check_light(){
	uint8_t light = (uint8_t)read_adc(LIGHT_PIN) * 100;
	
	if(light > 0){
		current_light = light;
		if(current_unit == 0xff){
			current_unit = LIGHT;
		}
		
		if(current_unit == LIGHT){
			if((current_status == CLOSED) & (current_light >= light_open)){
				roll(OPENED);
			}else if((current_status == OPENED) & (current_light <= light_close)){
				roll(CLOSED);
			}
		}
		
	}
}