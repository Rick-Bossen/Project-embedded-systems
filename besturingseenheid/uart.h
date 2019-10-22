#ifndef UART_H
#define UART_H

// 19.2k baudrate
#define UBBRVAL 51

void uart_init();
void transmit(uint8_t);
char has_input();
uint8_t receive();

#endif