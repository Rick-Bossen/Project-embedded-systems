#include "main.h"

#ifndef TEMP_H
#define TEMP_H

char current_unit = MANUAL;

uint8_t current_temperature = 19;
uint8_t current_light = 40;

// Random values don't copy in later code
uint8_t light_open = 20;
uint8_t light_close = 10;
uint8_t temperature_open = 16;
uint8_t temperature_close = 20;

#endif