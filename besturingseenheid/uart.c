#include <avr/sfr_defs.h>
#include <avr/io.h>
#include "uart.h"

void uart_init(){
	// Baud rate
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	// Disable U2X Mode
	UCSR0A = 0;
	// Enable receiver and transmitter
	UCSR0B = _BV(TXEN0) | _BV(RXEN0);
	// Set frame format asynchronous, 8 data bit, 1 stop bit
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
}

void transmit(uint8_t data)
{
	loop_until_bit_is_set(UCSR0A, UDRE0);
	UDR0 = data;
}

char has_input(){
	return UCSR0A & _BV(RXC0);
}

uint8_t receive()
{
	loop_until_bit_is_set(UCSR0A, RXC0);
	return UDR0;
}
