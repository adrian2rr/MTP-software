/*
 * commands.h
 *
 *  Created on: March 20, 2018
 *      Author: Adrian Rodriguez
 */

#ifndef COMMANDS_H_
#define COMMANDS_H_

extern DEVICE_CONFIG read_config(STATUS *status, int device);

extern STATUS write_config(DEVICE_CONFIG config, int device);

extern RF_CONFIG read_rfconfig(STATUS *status, int device);

extern STATUS write_channel(char channel, int device);

extern STATUS write_rfconfig(RF_CONFIG config, int device);

extern STATUS read_status(int device);

extern char read_powerdetector(STATUS *status, int device);

extern FIFO_STATUS read_fifostatus(STATUS *status, int device);

extern STATUS flushrx(int device);

extern STATUS flushtx(int device);

extern STATUS read_payload(char *rx, int len, int device);

extern STATUS write_payload(char *data, int len, int device);

extern AUTO_ACK read_auto_ack(STATUS *status, int device);

extern STATUS write_auto_ack(AUTO_ACK status, int device);

extern PIPES read_pipes_status(STATUS *status, int device);

extern STATUS write_pipes_status(PIPES status, int device);

extern char read_address_width(STATUS *status, int device);

extern STATUS write_address_width(char width, int device);

extern STATUS read_rx_address(char pipe, char *addr, int device);

extern STATUS write_rx_address(char pipe, char *addr, int device);

extern STATUS read_tx_address(char *addr, int device);

extern STATUS write_tx_address(char *addr, int device);

extern FEATURE read_feature(STATUS *status, int device);

extern STATUS write_features(FEATURE status, int device);

extern STATUS write_bytes_pipe(char pipe, char bytes, int device);

extern void write_status(STATUS status, int device);


#endif /* COMMANDS_H_ */
