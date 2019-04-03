/*
 * methods.c
 *
 *  Created on: March 25, 2018
 *      Author: Adrian Rodriguez
 *
 *  Functions to execute workflows using the commands.
 *
 */

 /*********************** Variables and imports *************************/

#include "constants.h"
#include "commands.h"
#include "spi_connector.h"
#include <time.h>

#define TX_CHANNEL 0x70
#define RX_CHANNEL 0x60
#define TX_POWER PWR_0
#define RX_POWER PWR_0

 /***********************************************************************/

 /***************************** Functions *******************************/

TRANSCIEVER system_init(int device, int mode) {
 /*
   ***********************************************************************
   *                                                                     *
   * TRANSCIEVER system_init(int device, int mode):                      *
   *   Initial configuration of the transciever.                         *
   *                                                                     *
   *   Parameters:                                                       *
   *     - int device: device to send command (1 PTX - 2 PRX)            *
   *     - int mode: transciever mode (1 DATA_TX - 2 DATA_RX)            *
   *                                                                     *
   *   Return:                                                           *
   *     - TRANSCIEVER: configuration and status of the transciever.     *
   *                                                                     *
   ***********************************************************************
 */

  TRANSCIEVER transciever;

  change_cs(0, device);

  STATUS status;
  FIFO_STATUS fifo_status;

  DEVICE_CONFIG device_config;
  device_config.irq_rx = IRQ_OFF;
  device_config.irq_tx = IRQ_OFF;
  device_config.irq_max = IRQ_OFF;
  device_config.crc = SET;
  //device_config.crc = NO_SET;
  device_config.crc_coding = CRC_2B;
  device_config.power = SET;
  device_config.mode = device == 1 ? PTX : PRX;

  RF_CONFIG rf_config;
  if (mode == 1){
    rf_config.channel = device == 1 ? TX_CHANNEL : RX_CHANNEL;
  } else {
    rf_config.channel = device == 1 ? RX_CHANNEL : TX_CHANNEL;
  }
  rf_config.con_carrier = NO_SET;
  rf_config.output_power = device == 1 ? TX_POWER : RX_POWER;
  rf_config.rate = RATE_250;
  rf_config.pll = NO_SET;

  PIPES pipes;
  pipes.pipe0 = SET;
  pipes.pipe1 = NO_SET;
  pipes.pipe2 = NO_SET;
  pipes.pipe3 = NO_SET;
  pipes.pipe4 = NO_SET;
  pipes.pipe5 = NO_SET;

  AUTO_ACK auto_ack;
  //auto_ack.pipe0 = SET;
  auto_ack.pipe0 = NO_SET;
  auto_ack.pipe1 = NO_SET;
  auto_ack.pipe2 = NO_SET;
  auto_ack.pipe3 = NO_SET;
  auto_ack.pipe4 = NO_SET;
  auto_ack.pipe5 = NO_SET;

  FEATURE feature;
  feature.dynamic_pay = NO_SET;
  feature.payload_ack = NO_SET;
  feature.no_ack = SET;
  //feature.no_ack = NO_SET;

  char address_width = ADDRESS_5B;

  write_bytes_pipe(0, 0x20, 1);

  write_features(feature, 1);
  write_address_width(address_width, 1);
  write_pipes_status(pipes, 1);
  write_auto_ack(auto_ack, 1);
  write_rfconfig(rf_config, 1);
  write_channel(rf_config.channel, 1);
  write_config(device_config, 1);
  fifo_status = read_fifostatus(&status, 1);

  transciever.device_config = device_config;
  transciever.rf_config = rf_config;
  transciever.status = status;
  transciever.fifo_status = fifo_status;
  transciever.pipes = pipes;
  transciever.auto_ack = auto_ack;
  transciever.feature = feature;
  transciever.address_width = address_width;
  transciever.mode = device == 1 ? 0x00 : 0x01;

  return transciever;
}


void rx_mode(TRANSCIEVER *transciever) {
/*
  ***********************************************************************
  *                                                                     *
  * void rx_mode(TRANSCIEVER *transciever):                             *
  *   Set transciever to rx mode.                                       *
  *                                                                     *
  *   Parameters:                                                       *
  *     - TRANSCIEVER *transciever: transciever object.                 *
  *                                                                     *
  *   Return:                                                           *
  *     -                                                               *
  *                                                                     *
  ***********************************************************************
*/
  int device;

  if (transciever->mode)
    device = 2;
  else
    device = 1;

  if (transciever->device_config.mode == PRX && transciever->device_config.power) {
    change_cs(1, device);
  } else if (transciever->device_config.mode == PRX) {
    transciever->device_config.power = SET;

    write_config(transciever->device_config, device);
    change_cs(1, device);
  } else {
    //TODO
    ;
  }

  return;
}


void wait_single_message(TRANSCIEVER *transciever, char *rx) {
  /*
    ***********************************************************************
    *                                                                     *
    * void wait_single_message(TRANSCIEVER *transciever, char *rx):       *
    *   Wait until one message is received and return it.                 *
    *                                                                     *
    *   Parameters:                                                       *
    *     - TRANSCIEVER *transciever: transciever object.                 *
    *     - char *rx: pointer to char array where the data will be saved. *
    *                                                                     *
    *   Return:                                                           *
    *     -                                                               *
    *                                                                     *
    ***********************************************************************
  */
  int device;

  if (transciever->mode)
    device = 2;
  else
    device = 1;

  char done = NO_SET;
  int len = 32;

  STATUS aux;

  aux = read_status(device);
  write_status(aux, device);

  while(done == NO_SET) {

    if (transciever->fifo_status.rx_empty == NO_SET) {

      transciever->status = read_payload(rx, len, device);
      done = SET;
      transciever->fifo_status = read_fifostatus(&transciever->status, device);

    } else {
    	transciever->fifo_status = read_fifostatus(&transciever->status, device);
    }

  }

  return;
}


void send_single_message(TRANSCIEVER *transciever, char *tx) {
  /*
    ***********************************************************************
    *                                                                     *
    * void send_single_message(TRANSCIEVER *transciever, char *rx):       *
    *   Send a sigle message (no ack).                                    *
    *                                                                     *
    *   Parameters:                                                       *
    *     - TRANSCIEVER *transciever: transciever object.                 *
    *     - char *rx: pointer to char array where the data will be saved. *
    *                                                                     *
    *   Return:                                                           *
    *     -                                                               *
    *                                                                     *
    ***********************************************************************
  */

  int device;

  if (transciever->mode)
    device = 2;
  else
    device = 1;

  int len = 32;

  flushtx(device);

  transciever->status = write_payload(tx, len, device);

  change_cs(1, device);

  usleep(100);

  change_cs(0, device);

  return;
}


void print_batch(char *rx, int len) {
  /*
    ***********************************************************************
    *                                                                     *
    * void print_batch(char *rx, int len):                                *
    *   Print to the console an array of char.                            *
    *                                                                     *
    *   Parameters:                                                       *
    *     - char *rx: pointer to char array with the data to print.       *
    *     - int len: length of the array.                                 *
    *                                                                     *
    *   Return:                                                           *
    *     -                                                               *
    *                                                                     *
    ***********************************************************************
  */

  //xil_printf(" Printing message: \r\n");
	//xil_printf("\r");

  for (int i = 0; i < len; i++) {
    printf("[%d] - %X |", i, *(rx + i));
  }

  //xil_printf("\r\n\r\n------------------\r\n");

  return;
}


void print_all(TRANSCIEVER *transciever) {

  int device;

  if (transciever->mode)
    device = 2;
  else
    device = 1;

	STATUS status;
	DEVICE_CONFIG config;
	RF_CONFIG rfconfig;
	FIFO_STATUS fifo;
	AUTO_ACK autoa;
	PIPES pipes;
	FEATURE feature;

	config = read_config(&status, device);

	printf("\r\n\r\n Device: %X", device);

	printf("\r\n Device: %X - %X - %X - %X - %X - %X - %X", config.crc, config.crc_coding, config.irq_max, config.irq_rx, config.irq_tx, config.mode, config.power);

	rfconfig = read_rfconfig(&status, device);

	printf("\r\n RF: %X - %X - %X - %X - %X", rfconfig.channel, rfconfig.con_carrier, rfconfig.output_power, rfconfig.pll, rfconfig.rate);

	fifo = read_fifostatus(&status, device);

	printf("\r\n fifo: %X - %X - %X - %X - %X", fifo.rx_empty, fifo.rx_full, fifo.tx_empty, fifo.tx_full, fifo.tx_reuse);

	autoa = read_auto_ack(&status, device);

	printf("\r\n auto: %X - %X - %X - %X - %X - %X", autoa.pipe0, autoa.pipe1, autoa.pipe2, autoa.pipe3, autoa.pipe4, autoa.pipe5);

	pipes = read_pipes_status(&status, device);

	printf("\r\n pipes: %X - %X - %X - %X - %X - %X", pipes.pipe0, pipes.pipe1, pipes.pipe2, pipes.pipe3, pipes.pipe4, pipes.pipe5);

	feature = read_feature(&status, device);

	printf("\r\n feature: %X - %X - %X", feature.dynamic_pay, feature.no_ack, feature.payload_ack);

	printf("\r\n status: %X - %X - %X \r\n\n", status.max_retrans, status.rx_data, status.tx_data);

  transciever->device_config = config;
  transciever->rf_config = rfconfig;
  transciever->status = status;
  transciever->fifo_status = fifo;
  transciever->pipes = pipes;
  transciever->auto_ack = autoa;
  transciever->feature = feature;

	return;
}
