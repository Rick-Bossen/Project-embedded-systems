#ifndef SUNBLIND_H
#define SUNBLIND_H

#define LED_RED _BV(PORTB0)
#define LED_YELLOW _BV(PORTB1)
#define LED_GREEN _BV(PORTB2)

#define ULTRASONIC_TRIGGER _BV(PORTD4)
#define ULTRASONIC_ECHO _BV(PORTD5)

void check_sunblind_position();
void set_leds();
void roll(char direction);

#endif