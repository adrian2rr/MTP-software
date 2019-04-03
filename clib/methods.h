/*
 * methods.h
 *
 *  Created on: March 25, 2018
 *      Author: Adrian Rodriguez
 */

#ifndef METHODS_H_
#define METHODS_H_

extern TRANSCIEVER system_init(int device, int mode);

extern void rx_mode(TRANSCIEVER *transciever);

extern void wait_single_message(TRANSCIEVER *transciever, char *rx);

extern void print_batch(char *rx, int len);

extern void send_single_message(TRANSCIEVER *transciever, char *tx);

extern void print_all(TRANSCIEVER *transciever);

#endif /* METHODS_H_ */
