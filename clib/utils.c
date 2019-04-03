/*
 * utils.c
 *
 *  Created on: March 19, 2018
 *      Author: Adrian Rodriguez
 *
 *  Auxiliary functions.
 *
 */

/*********************** Variables and imports *************************/

 #include "constants.h"

 /***********************************************************************/

 /***************************** Functions *******************************/

STATUS extract_status(char status) {
/*
  ***********************************************************************
  *                                                                     *
  * STATUS extract_status(char status):                                 *
  *   Transform a status char into object.                              *
  *                                                                     *
  *   Parameters:                                                       *
  *     - char status: status byte                                      *
  *                                                                     *
  *   Return:                                                           *
  *     - STATUS object.                                                *
  *                                                                     *
  ***********************************************************************
*/

  STATUS output;

  if (status & (1<<6)) {
    output.rx_data = IRQ_SET;
  } else {
    output.rx_data = IRQ_CLEAR;
  }

  if (status & (1<<5)) {
    output.tx_data = IRQ_SET;
  } else {
    output.tx_data = IRQ_CLEAR;
  }

  if (status & (1<<4)) {
    output.max_retrans = IRQ_SET;
  } else {
    output.max_retrans = IRQ_CLEAR;
  }

  return output;
}


char parse_status(STATUS config){

	char output;

	output = 0x00;

	if (config.max_retrans){
		output += 0x10;
	}

	if (config.rx_data){
		output += 0x40;
	}

	if (config.tx_data){
		output += 0x20;
	}

	return output;
}


DEVICE_CONFIG exctract_config(char config){
/*
  ***********************************************************************
  *                                                                     *
  * DEVICE_CONFIG exctract_config(char config):                         *
  *   Transform a config char into object.                              *
  *                                                                     *
  *   Parameters:                                                       *
  *     -	char config: config byte.                                     *
  *                                                                     *
  *   Return:                                                           *
  *     -	DEVICE_CONFIG object.                                         *
  *                                                                     *
  ***********************************************************************
*/

  DEVICE_CONFIG output;

  if (config & (1<<6)) {
    output.irq_rx = IRQ_OFF;
  } else {
    output.irq_rx = IRQ_ON;
  }

  if (config & (1<<5)) {
    output.irq_tx = IRQ_OFF;
  } else {
    output.irq_tx = IRQ_ON;
  }

  if (config & (1<<4)) {
    output.irq_max = IRQ_OFF;
  } else {
    output.irq_max = IRQ_ON;
  }

  if (config & (1<<3)) {
    output.crc = SET;
  } else {
    output.crc = NO_SET;
  }

  if (config & (1<<2)) {
    output.crc_coding = CRC_2B;
  } else {
    output.crc_coding = CRC_1B;
  }

  if (config & (1<<1)) {
    output.power = SET;
  } else {
    output.power = NO_SET;
  }

  if (config & (1<<0)) {
    output.mode = PRX;
  } else {
    output.mode = PTX;
  }

  return output;
}


char parse_config(DEVICE_CONFIG config){
/*
  ***********************************************************************
  *                                                                     *
  * char parse_config(DEVICE_CONFIG config):                            *
  *   Transform a config object into char.                              *
  *                                                                     *
  *   Parameters:                                                       *
  *     -	DEVICE_CONFIG config: config object.                        *
  *                                                                     *
  *   Return:                                                           *
  *     -	char with configuration.                                    *
  *                                                                     *
  ***********************************************************************
*/

  char output;

  output = 0x00;

  if (config.irq_rx) {
    output += 0x40;
  }

  if (config.irq_tx) {
    output += 0x20;
  }

  if (config.irq_max) {
    output += 0x10;
  }

  if (config.crc) {
    output += 0x08;
  }

  if (config.crc_coding) {
    output += 0x04;
  }

  if (config.power) {
    output += 0x02;
  }

  if (config.mode) {
    output += 0x01;
  }

  return output;
}


void extract_rf(char rf, RF_CONFIG *output) {
/*
  ***********************************************************************
  *                                                                     *
  * void extract_rf(char rf, RF_CONFIG *output):                        *
  *   Transform a rf config char into a rf config object.               *
  *                                                                     *
  *   Parameters:                                                       *
  *     -	char rf: byte with the data to transform.                     *
  *     - RF_CONFIG *output: pointer to an RF_CONFIG object where       *
  *         the data will be saved.                                     *
  *                                                                     *
  *   Return:                                                           *
  *     -                                                               *
  *                                                                     *
  ***********************************************************************
*/

  if (rf & (1<<7)) {
    output->con_carrier = SET;
  } else {
    output->con_carrier = NO_SET;
  }

  if (rf & (1<<4)) {
    output->pll = SET;
  } else {
	  output->pll = NO_SET;
  }

  output->output_power = 0x00;

  if (rf & (1<<2)) {
    output->output_power += 0x02;
  }

  if (rf & (1<<1)) {
    output->output_power += 0x01;
  }

  if (rf & (1<<5)) {
    output->rate = RATE_250;
  } else {
    if (rf & (1<<3)) {
      output->rate = RATE_1;
    } else {
      output->rate = RATE_2;
    }
  }

  return;
}


char parse_rfconfig(RF_CONFIG config) {
/*
  ***********************************************************************
  *                                                                     *
  * char parse_rfconfig(RF_CONFIG config):                              *
  *   Transform a rf config object into a char.                         *
  *                                                                     *
  *   Parameters:                                                       *
  *     - RF_CONFIG config: RF_CONFIG object to parse into char.        *
  *                                                                     *
  *   Return:                                                           *
  *     - char: byte with the rf configuration.                         *
  *                                                                     *
  ***********************************************************************
*/

  char output;

  output = 0x00;

  if (config.con_carrier) {
    output += 0x80;
  }

  if (config.pll) {
    output += 0x10;
  }

  switch (config.rate) {
    case RATE_250:
      output += 0x20;
      break;
    case RATE_2:
      output += 0x08;
      break;
    default:
      output += 0x00;
  }

  switch (config.output_power) {
    case PWR_0:
      output += 0x06;
      break;
    case PWR_6:
      output += 0x04;
      break;
    case PWR_12:
      output += 0x02;
      break;
    default:
      output += 0x00;
  }

  return output;
}


FIFO_STATUS exctract_fifo(char status){
/*
  ***********************************************************************
  *                                                                     *
  * FIFO_STATUS exctract_fifo(char status):                             *
  *   Transform a fifo register char into object.                       *
  *                                                                     *
  *   Parameters:                                                       *
  *     -	char status: fifo status byte.                                *
  *                                                                     *
  *   Return:                                                           *
  *     -	FIFO_STATUS object.                                           *
  *                                                                     *
  ***********************************************************************
*/

  FIFO_STATUS output;

  if (status & (1<<6)) {
    output.tx_reuse = SET;
  } else {
    output.tx_reuse = NO_SET;
  }

  if (status & (1<<5)) {
    output.tx_full = SET;
  } else {
    output.tx_full = NO_SET;
  }

  if (status & (1<<4)) {
    output.tx_empty = SET;
  } else {
    output.tx_empty = NO_SET;
  }

  if (status & (1<<1)) {
    output.rx_full = SET;
  } else {
    output.rx_full = NO_SET;
  }

  if (status & (1<<0)) {
    output.rx_empty = SET;
  } else {
    output.rx_empty = NO_SET;
  }

  return output;
}


AUTO_ACK exctract_auto_ack(char status){
/*
  ***********************************************************************
  *                                                                     *
  * AUTO_ACK exctract_auto_ack(char status):                            *
  *   Transform a auto_ack register char into object.                   *
  *                                                                     *
  *   Parameters:                                                       *
  *     -	char status: auto_ack status byte.                            *
  *                                                                     *
  *   Return:                                                           *
  *     -	AUTO_ACK object.                                              *
  *                                                                     *
  ***********************************************************************
*/

  AUTO_ACK output;

  if (status & (1<<5)) {
    output.pipe5 = SET;
  } else {
    output.pipe5 = NO_SET;
  }

  if (status & (1<<4)) {
    output.pipe4 = SET;
  } else {
    output.pipe4 = NO_SET;
  }

  if (status & (1<<3)) {
    output.pipe3 = SET;
  } else {
    output.pipe3 = NO_SET;
  }

  if (status & (1<<2)) {
    output.pipe2 = SET;
  } else {
    output.pipe2 = NO_SET;
  }

  if (status & (1<<1)) {
    output.pipe1 = SET;
  } else {
    output.pipe1 = NO_SET;
  }

  if (status & (1<<0)) {
    output.pipe0 = SET;
  } else {
    output.pipe0 = NO_SET;
  }

  return output;
}


char parse_auto_ack(AUTO_ACK status){
/*
  ***********************************************************************
  *                                                                     *
  * char parse_auto_ack(AUTO_ACK status):                               *
  *   Transform a auto_ack object into char.                            *
  *                                                                     *
  *   Parameters:                                                       *
  *     -	AUTO_ACK status: auto_ack status object.                      *
  *                                                                     *
  *   Return:                                                           *
  *     -	char object.                                                  *
  *                                                                     *
  ***********************************************************************
*/

  char output;

  output = 0x00;

  if (status.pipe0) {
    output += 0x01;
  }

  if (status.pipe1) {
    output += 0x02;
  }

  if (status.pipe2) {
    output += 0x04;
  }

  if (status.pipe3) {
    output += 0x08;
  }

  if (status.pipe4) {
    output += 0x10;
  }

  if (status.pipe5) {
    output += 0x20;
  }

  return output;
}


PIPES extract_pipes_status(char status) {
  /*
    ***********************************************************************
    *                                                                     *
    * PIPES extract_pipes_status(char status):                            *
    *   Transform a pipes status char into object.                        *
    *                                                                     *
    *   Parameters:                                                       *
    *     -	char status: pipes status char.                               *
    *                                                                     *
    *   Return:                                                           *
    *     -	PIPES object.                                                 *
    *                                                                     *
    ***********************************************************************
  */

  PIPES output;

  if (status & (1<<5)) {
    output.pipe5 = SET;
  } else {
    output.pipe5 = NO_SET;
  }

  if (status & (1<<4)) {
    output.pipe4 = SET;
  } else {
    output.pipe4 = NO_SET;
  }

  if (status & (1<<3)) {
    output.pipe3 = SET;
  } else {
    output.pipe3 = NO_SET;
  }

  if (status & (1<<2)) {
    output.pipe2 = SET;
  } else {
    output.pipe2 = NO_SET;
  }

  if (status & (1<<1)) {
    output.pipe1 = SET;
  } else {
    output.pipe1 = NO_SET;
  }

  if (status & (1<<0)) {
    output.pipe0 = SET;
  } else {
    output.pipe0 = NO_SET;
  }

  return output;
}


char parse_pipes_status(PIPES status) {
  /*
    ***********************************************************************
    *                                                                     *
    * char parse_pipes_status(PIPES status):                              *
    *   Transform a pipes status object into char.                        *
    *                                                                     *
    *   Parameters:                                                       *
    *     -	PIPES status: pipes status object.                            *
    *                                                                     *
    *   Return:                                                           *
    *     -	char object.                                                  *
    *                                                                     *
    ***********************************************************************
  */

    char output;

    output = 0x00;

    if (status.pipe0) {
      output += 0x01;
    }

    if (status.pipe1) {
      output += 0x02;
    }

    if (status.pipe2) {
      output += 0x04;
    }

    if (status.pipe3) {
      output += 0x08;
    }

    if (status.pipe4) {
      output += 0x10;
    }

    if (status.pipe5) {
      output += 0x20;
    }

    return output;
}


FEATURE extract_feature(char status) {
  /*
    ***********************************************************************
    *                                                                     *
    * FEATURE extract_feature(char status):                               *
    *   Transform a feature status char into object.                      *
    *                                                                     *
    *   Parameters:                                                       *
    *     -	char status: feature status char.                             *
    *                                                                     *
    *   Return:                                                           *
    *     -	FEATURE object.                                               *
    *                                                                     *
    ***********************************************************************
  */

  FEATURE output;

  if (status & (1<<2)) {
    output.dynamic_pay = SET;
  } else {
    output.dynamic_pay = NO_SET;
  }

  if (status & (1<<1)) {
    output.payload_ack = SET;
  } else {
    output.payload_ack = NO_SET;
  }

  if (status & (1<<0)) {
    output.no_ack = SET;
  } else {
    output.no_ack = NO_SET;
  }

  return output;
}


char parse_feature(FEATURE status) {
  /*
    ***********************************************************************
    *                                                                     *
    * char parse_feature(FEATURE status):                                 *
    *   Transform a feature object into char.                             *
    *                                                                     *
    *   Parameters:                                                       *
    *     -	FEATURE status: feature object.                               *
    *                                                                     *
    *   Return:                                                           *
    *     -	char object.                                                  *
    *                                                                     *
    ***********************************************************************
  */

    char output;

    output = 0x00;

    if (status.no_ack) {
      output += 0x01;
    }

    if (status.payload_ack) {
      output += 0x02;
    }

    if (status.dynamic_pay) {
      output += 0x04;
    }

    return output;
}
