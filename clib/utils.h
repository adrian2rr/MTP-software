/*
 * utils.h
 *
 *  Created on: March 19, 2018
 *      Author: Adrian Rodriguez
 */

 #ifndef UTILS_H_
 #define UTILS_H_

extern STATUS extract_status(char status);

extern char parse_status(STATUS config);

extern DEVICE_CONFIG exctract_config(char config);

extern char parse_config(DEVICE_CONFIG config);

extern void extract_rf(char rf, RF_CONFIG *output);

extern char parse_rfconfig(RF_CONFIG config);

extern FIFO_STATUS exctract_fifo(char status);

extern AUTO_ACK exctract_auto_ack(char status);

extern char parse_auto_ack(AUTO_ACK status);

extern PIPES extract_pipes_status(char status);

extern char parse_pipes_status(PIPES status);

extern FEATURE extract_feature(char status);

extern char parse_feature(FEATURE status);

 #endif /* UTILS_H_ */
