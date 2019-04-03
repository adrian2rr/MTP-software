/*
 * commands.c
 *
 *  Created on: March 19, 2018
 *      Author: Adrian Rodriguez
 *
 *  Functions to send commands to the rf module.
 *
 */

/*********************** Variables and imports *************************/

#include "constants.h"
#include "spi_connector.h"
#include "utils.h"

/***********************************************************************/

/***************************** Functions *******************************/

DEVICE_CONFIG read_config(STATUS *status, int device) {
/*
  ***********************************************************************
  *                                                                     *
  * DEVICE_CONFIG read_config(STATUS *status, int device):              *
  *   Read device configuration                                         *
  *                                                                     *
  *   Parameters:                                                       *
  *     - STATUS *status: pointer to a status object where the          *
  *         received status will be saved.                              *
  *     - int device: device to send command                            *
  *                                                                     *
  *   Return:                                                           *
  *     - DEVICE_CONFIG: configuration received from the module.        *
  *                                                                     *
  ***********************************************************************
*/

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command to send
  tx[0] = REGISTER_CONFIG_R;
  tx[1] = PADDING;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Get status object
  *status = extract_status(rx[0]);

  // Return Config object
  return exctract_config(rx[1]);
}


STATUS write_config(DEVICE_CONFIG config, int device) {
/*
  ***********************************************************************
  *                                                                     *
  * STATUS write_config(DEVICE_CONFIG *config, int device):             *
  *   Write device configuration                                        *
  *                                                                     *
  *   Parameters:                                                       *
  *     - DEVICE_CONFIG config: config object to write in the module.   *
  *     - int device: device to send command                            *
  *                                                                     *
  *   Return:                                                           *
  *     - STATUS: Status object received from the module.               *
  *                                                                     *
  ***********************************************************************
*/

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_CONFIG_W;
  tx[1] = parse_config(config);

  // SPI operation
  spi_data(tx, rx, len, device);

  // Return status received
  return extract_status(rx[0]);
}


RF_CONFIG read_rfconfig(STATUS *status, int device) {
/*
  ***********************************************************************
  *                                                                     *
  * RF_CONFIG read_rfconfig(STATUS *status, int device):                *
  *   Read RF device configuration                                      *
  *                                                                     *
  *   Parameters:                                                       *
  *     - STATUS *status: pointer to a status object where the          *
  *         received status will be saved.                              *
  *     - int device: device to send command                            *
  *                                                                     *
  *   Return:                                                           *
  *     - RF_CONFIG: RF Configuration object received.                  *
  *                                                                     *
  ***********************************************************************
*/

  int len = 2;
  char tx[len];
  char rx[len];
  RF_CONFIG output;

  // Set command and data to send
  tx[0] = REGISTER_CHANNEL_R;
  tx[1] = PADDING;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Set channel and set next command
  output.channel = rx[1];
  tx[0] = REGISTER_RF_R;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Extract status Received
  *status = extract_status(rx[0]);

  // Extract rf information
  extract_rf(rx[1], &output);

  return output;
}


STATUS write_channel(char channel, int device) {
/*
  ***********************************************************************
  *                                                                     *
  * STATUS write_channel(char channel, int device):                     *
  *   Write RF channel into the device.                                 *
  *                                                                     *
  *   Parameters:                                                       *
  *     - char channel: channel to set in the transciever.              *
  *     - int device: device to send command                            *
  *                                                                     *
  *   Return:                                                           *
  *     - STATUS: status received from the module.                      *
  *                                                                     *
  ***********************************************************************
*/

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_CHANNEL_W;
  tx[1] = channel;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Return status received
  return extract_status(rx[0]);
}


STATUS write_rfconfig(RF_CONFIG config, int device) {
/*
  ***********************************************************************
  *                                                                     *
  * STATUS write_rfconfig(RF_CONFIG config, int device):                *
  *   Write RF config into the device.                                  *
  *                                                                     *
  *   Parameters:                                                       *
  *     - RF_CONFIG config: rf config object to set in the transciever. *
  *     - int device: device to send command                            *
  *                                                                     *
  *   Return:                                                           *
  *     - STATUS: status received from the module.                      *
  *                                                                     *
  ***********************************************************************
*/

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_RF_W;
  tx[1] = parse_rfconfig(config);

  // SPI operation
  spi_data(tx, rx, len, device);

  // Return status received
  return extract_status(rx[0]);
}


STATUS read_status(int device) {
/*
  ***********************************************************************
  *                                                                     *
  * STATUS read_status(int device):                                     *
  *   Read status register.                                             *
  *                                                                     *
  *   Parameters:                                                       *
  *     - int device: device to send command                            *
  *                                                                     *
  *   Return:                                                           *
  *     - STATUS: status received from the module.                      *
  *                                                                     *
  ***********************************************************************
*/

  int len = 1;
  char tx[len];
  char rx[len];

  // Set command to Send
  tx[0] = READ_STATUS;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Return status Received
  return extract_status(rx[0]);
}


char read_powerdetector(STATUS *status, int device) {
/*
  ***********************************************************************
  *                                                                     *
  * char read_powerdetector(STATUS *status, int device):                *
  *   Read power detection register.                                    *
  *                                                                     *
  *   Parameters:                                                       *
  *     - STATUS *status: pointer to a status object where the          *
  *         received status will be saved.                              *
  *     - int device: device to send command                            *
  *                                                                     *
  *   Return:                                                           *
  *     - char: power detection register received.                      *
  *                                                                     *
  ***********************************************************************
*/

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command to send
  tx[0] = REGISTER_PWD_DET;
  tx[1] = PADDING;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Get status object
  *status = extract_status(rx[0]);

  // Return power detection
  return rx[1];
}


FIFO_STATUS read_fifostatus(STATUS *status, int device) {
/*
  ***********************************************************************
  *                                                                     *
  * FIFO_STATUS read_fifostatus(STATUS *status, int device):            *
  *   Read device fifo status.                                          *
  *                                                                     *
  *   Parameters:                                                       *
  *     - STATUS *status: pointer to a status object where the          *
  *         received status will be saved.                              *
  *     - int device: device to send command                            *
  *                                                                     *
  *   Return:                                                           *
  *     - FIFO_STATUS: fifo status received from the module.            *
  *                                                                     *
  ***********************************************************************
*/

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command to send
  tx[0] = REGISTER_FIFO_R;
  tx[1] = PADDING;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Get status object
  *status = extract_status(rx[0]);

  // Return Config object
  return exctract_fifo(rx[1]);
}


STATUS flushrx(int device) {
/*
  ***********************************************************************
  *                                                                     *
  * STATUS flushrx(int device):                                         *
  *   Flush rx fifo buffer.                                             *
  *                                                                     *
  *   Parameters:                                                       *
  *     - int device: device to send command                            *
  *                                                                     *
  *   Return:                                                           *
  *     - STATUS: status received from the module.                      *
  *                                                                     *
  ***********************************************************************
*/

  int len = 1;
  char tx[len];
  char rx[len];

  // Set command to Send
  tx[0] = FLUSH_RX;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Return status Received
  return extract_status(rx[0]);
}


STATUS flushtx(int device) {
/*
  ***********************************************************************
  *                                                                     *
  * STATUS flushtx(int device):                                         *
  *   Flush tx fifo buffer.                                             *
  *                                                                     *
  *   Parameters:                                                       *
  *     - int device: device to send command                            *
  *                                                                     *
  *   Return:                                                           *
  *     - STATUS: status received from the module.                      *
  *                                                                     *
  ***********************************************************************
*/

  int len = 1;
  char tx[len];
  char rx[len];

  // Set command to Send
  tx[0] = FLUSH_TX;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Return status Received
  return extract_status(rx[0]);
}


STATUS read_payload(char *rx, int len, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * STATUS read_payload(char *rx, int len, int device):                 *
    *   Read first packet in rx fifo.                                     *
    *                                                                     *
    *   Parameters:                                                       *
    *     - char *rx: pointer to char array where the data will be saved. *
    *     - int len: number of bytes to be read.                          *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - STATUS: status received from the module.                      *
    *                                                                     *
    ***********************************************************************
  */

  len += 1;
  char tx[len];
  char rx_aux[len];

  // Set command to send and padding
  tx[0] = PAYLOAD_R;
  for (int i = 1; i < len; i++) {
    tx[i] = PADDING;
  }

  // SPI operation
  spi_data(tx, rx_aux, len, device);

  // copy rx
  for(int i = 1; i < len; i++) {
    *(rx + i - 1) = *(rx_aux + i);
  }

  // Return status Received
  return extract_status(rx_aux[0]);
}


STATUS write_payload(char *data, int len, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * STATUS write_payload(char *data, int len, int device):              *
    *   Write packet into tx fifo buffer.                                 *
    *                                                                     *
    *   Parameters:                                                       *
    *     - char *data: pointer to char array of the data to send.        *
    *     - int len: number of bytes to be sent.                          *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - STATUS: status received from the module.                      *
    *                                                                     *
    ***********************************************************************
  */

  len += 1;
  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = PAYLOAD_W_NA;
  for (int i = 1; i < len; i++) {
    tx[i] = *(data + i - 1);
  }

  // SPI operation
  spi_data(tx, rx, len, device);

  // Return status Received
  return extract_status(rx[0]);
}


AUTO_ACK read_auto_ack(STATUS *status, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * AUTO_ACK read_auto_ack(STATUS *status, int device):                 *
    *   Read status of auto ack pipes.                                    *
    *                                                                     *
    *   Parameters:                                                       *
    *     - STATUS *status: pointer to a status object where the          *
    *         received status will be saved.                              *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - AUTO_ACK: auto ack pipes status.                              *
    *                                                                     *
    ***********************************************************************
  */

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_AUTO_ACK_R;
  tx[1] = PADDING;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Get status object
  *status = extract_status(rx[0]);

  // Return status Received
  return exctract_auto_ack(rx[1]);
}


STATUS write_auto_ack(AUTO_ACK status, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * STATUS write_auto_ack(AUTO_ACK status, int device):                 *
    *   Read status of auto ack pipes.                                    *
    *                                                                     *
    *   Parameters:                                                       *
    *     - AUTO_ACK status: object with the configuration that will      *
    *         be write in the module.                                     *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - STATUS: status received from the module.                      *
    *                                                                     *
    ***********************************************************************
  */

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_AUTO_ACK_W;
  tx[1] = parse_auto_ack(status);

  // SPI operation
  spi_data(tx, rx, len, device);

  // Return status Received
  return extract_status(rx[0]);
}


PIPES read_pipes_status(STATUS *status, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * PIPES read_pipes_status(STATUS *status, int device):                *
    *   Read status of pipes.                                             *
    *                                                                     *
    *   Parameters:                                                       *
    *     - STATUS *status: pointer to a status object where the          *
    *         received status will be saved.                              *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - PIPES: pipes status.                                          *
    *                                                                     *
    ***********************************************************************
  */

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_PIPE_ST_R;
  tx[1] = PADDING;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Get status object
  *status = extract_status(rx[0]);

  // Return status Received
  return extract_pipes_status(rx[1]);
}


STATUS write_pipes_status(PIPES status, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * STATUS write_pipes_status(PIPES status, int device):                *
    *   Write status of pipes.                                            *
    *                                                                     *
    *   Parameters:                                                       *
    *     - PIPES status: object with the configuration that will         *
    *         be write in the module.                                     *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - status received from the module.                              *
    *                                                                     *
    ***********************************************************************
  */

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_PIPE_ST_W;
  tx[1] = parse_pipes_status(status);

  // SPI operation
  spi_data(tx, rx, len, device);

  // Return status Received
  return extract_status(rx[0]);
}


char read_address_width(STATUS *status, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * char read_address_width(STATUS *status, int device):                *
    *   Read the address width of the pipes.                              *
    *                                                                     *
    *   Parameters:                                                       *
    *     - STATUS *status: pointer to a status object where the          *
    *         received status will be saved.                              *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - char: address width.                                          *
    *                                                                     *
    ***********************************************************************
  */

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_ADDR_WITD_R;
  tx[1] = PADDING;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Get status object
  *status = extract_status(rx[0]);

  // Return status Received
  return rx[1];
}


STATUS write_address_width(char width, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * STATUS write_address_width(char width, int device):                 *
    *   Write address width of pipes.                                     *
    *                                                                     *
    *   Parameters:                                                       *
    *     - char width: address width that will be writen in the moduele. *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - status received from the module.                              *
    *                                                                     *
    ***********************************************************************
  */

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_ADDR_WITD_W;
  tx[1] = width;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Return status Received
  return extract_status(rx[0]);
}


STATUS read_rx_address(char pipe, char *addr, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * STATUS read_rx_address(char pipe, char *addr, int device):          *
    *   read address of a pipe.                                           *
    *                                                                     *
    *   Parameters:                                                       *
    *     - char pipe: number of the pipe to read.                        *
    *     - char *addr: pointer to the array char where the address       *
    *         will be saved.                                              *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - status received from the module.                              *
    *                                                                     *
    ***********************************************************************
  */

  int len = 6;
  if (pipe > 0x01){
    len = 2;
  }

  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_RX_ADD_R + pipe;
  for (int i = 1; i < len; i++) {
    tx[i] = PADDING;
  }

  // SPI operation
  spi_data(tx, rx, len, device);

  // copy rx
  for(int i = 1; i < len; i++) {
    *(addr + i - 1) = *(rx + i);
  }

  // Return status Received
  return extract_status(rx[0]);
}


STATUS write_rx_address(char pipe, char *addr, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * STATUS write_rx_address(char pipe, char *addr, int device):         *
    *   write address of a pipe.                                          *
    *                                                                     *
    *   Parameters:                                                       *
    *     - char pipe: number of the pipe to read.                        *
    *     - char *addr: pointer to the array char where the address       *
    *         will be get.                                                *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - status received from the module.                              *
    *                                                                     *
    ***********************************************************************
  */

  int len = 6;
  if (pipe > 0x01){
    len = 2;
  }

  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_RX_ADD_W + pipe;
  for (int i = 1; i < len; i++) {
    tx[i] = *(addr + i - 1);
  }

  // SPI operation
  spi_data(tx, rx, len, device);

  // Return status Received
  return extract_status(rx[0]);
}


STATUS read_tx_address(char *addr, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * STATUS read_tx_address(char *addr, int device):                     *
    *   read tx address.                                                  *
    *                                                                     *
    *   Parameters:                                                       *
    *     - char *addr: pointer to the array char where the address       *
    *         will be saved.                                              *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - status received from the module.                              *
    *                                                                     *
    ***********************************************************************
  */

  int len = 6;

  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_TX_ADD_R;
  for (int i = 1; i < len; i++) {
    tx[i] = PADDING;
  }

  // SPI operation
  spi_data(tx, rx, len, device);

  // copy rx
  for(int i = 1; i < len; i++) {
    *(addr + i - 1) = *(rx + i);
  }

  // Return status Received
  return extract_status(rx[0]);
}


STATUS write_tx_address(char *addr, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * STATUS write_tx_address(char *addr, int device):                    *
    *   write tx address.                                                 *
    *                                                                     *
    *   Parameters:                                                       *
    *     - char *addr: pointer to the array char where the address       *
    *         will be get.                                                *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - status received from the module.                              *
    *                                                                     *
    ***********************************************************************
  */

  int len = 6;

  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_TX_ADD_W;
  for (int i = 1; i < len; i++) {
    tx[i] = *(addr + i - 1);
  }

  // SPI operation
  spi_data(tx, rx, len, device);

  // Return status Received
  return extract_status(rx[0]);
}


FEATURE read_feature(STATUS *status, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * FEATURE read_feature(STATUS *status, int device):                   *
    *   Read features.                                                    *
    *                                                                     *
    *   Parameters:                                                       *
    *     - STATUS *status: pointer to a status object where the          *
    *         received status will be saved.                              *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - FEATURE: features status.                                     *
    *                                                                     *
    ***********************************************************************
  */

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_FEATURE_R;
  tx[1] = PADDING;

  // SPI operation
  spi_data(tx, rx, len, device);

  // Get status object
  *status = extract_status(rx[0]);

  // Return status Received
  return extract_feature(rx[1]);
}


STATUS write_features(FEATURE status, int device) {
  /*
    ***********************************************************************
    *                                                                     *
    * STATUS write_features(FEATURE status, int device):                  *
    *   Write status of pipes.                                            *
    *                                                                     *
    *   Parameters:                                                       *
    *     - FEATURE status: object with the features that will            *
    *         be write in the module.                                     *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - status received from the module.                              *
    *                                                                     *
    ***********************************************************************
  */

  int len = 2;
  char tx[len];
  char rx[len];

  // Set command and data to send
  tx[0] = REGISTER_FEATURE_W;
  tx[1] = parse_feature(status);

  // SPI operation
  spi_data(tx, rx, len, device);

  // Return status Received
  return extract_status(rx[0]);
}


STATUS write_bytes_pipe(char pipe, char bytes, int device){
  /*
    ***********************************************************************
    *                                                                     *
    * STATUS write_bytes_pipe(char pipe, char bytes, int device):         *
    *   Write bytes of pipes payload.                                     *
    *                                                                     *
    *   Parameters:                                                       *
    *     - char pipe: Number of the pipe to modify.                      *
    *     - char bytes: Number of bytes of the pipe payload.              *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - status received from the module.                              *
    *                                                                     *
    ***********************************************************************
  */

	int len = 2;
	char tx[len];
	char rx[len];

	// Set command and data to send
	tx[0] = REGISTER_RX_0_P_W + pipe;
	tx[1] = bytes;

	// SPI operation
	spi_data(tx, rx, len, device);

	// Return status Received
	return extract_status(rx[0]);
}


void write_status(STATUS status, int device){
  /*
    ***********************************************************************
    *                                                                     *
    * void write_status(STATUS status, int device):                       *
    *   Write (to clear) Status register.                                 *
    *                                                                     *
    *   Parameters:                                                       *
    *     - STATUS status: Status object with the bits to clear.          *
    *     - int device: device to send command                            *
    *                                                                     *
    *   Return:                                                           *
    *     - status received from the module.                              *
    *                                                                     *
    ***********************************************************************
  */

	int len = 2;
	char tx[len];
	char rx[len];

	// Set command and data to send
	tx[0] = REGISTER_STATUS_W;
	tx[1] = parse_status(status);

	// SPI operation
	spi_data(tx, rx, len, device);

	// Return status Received
	return;
}
