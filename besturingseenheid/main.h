#include <avr/io.h>

#ifndef MAIN_H
#define MAIN_H

// instructions
#define SET_UNIT 1
#define ROLL 2
#define SET_UNIT_RANGE 3

// units
#define MANUAL 0
#define LIGHT 1
#define TEMPERATURE 2

// direction
#define CLOSED 0
#define OPENED 1
#define EXPANDING 2
#define COLLAPSING 3

// Responses
#define STATE_INFO 1
#define UNIT_INFO 2
#define UNIT_VALUE_INFO 3

uint8_t current_unit;
char current_status;

uint8_t current_distance;
uint8_t current_temperature;
uint8_t current_light;

uint8_t light_open;
uint8_t light_close;
uint8_t temperature_open;
uint8_t temperature_close;

#endif