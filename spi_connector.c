/*
 * spi_connector.c
 *
 *  Created on: March 19, 2018
 *      Author: Adrian Rodriguez
 *
 *  Funcionality to interconnect the rest of the software with
 *  external SPI libraries.
 *
 */

/*********************** Variables and imports *************************/

// External libraries
#include "xgpio.h"
#include "xparameters.h"

// Global parameters to be used by external libraries
#define GPIO_DEVICE_DATA XPAR_AXI_GPIO_0_DEVICE_ID
#define GPIO_DEVICE_CONTROL XPAR_AXI_GPIO_1_DEVICE_ID
#define RECIVER_CHANNEL 1
#define SENDER_CHANNEL 2
#define END_CHANNEL 1
#define START_CHANNEL 2

XGpio Gpio_data, Gpio_control;

/***********************************************************************/

/***************************** Functions *******************************/

void spi_init() {
/*
  ***********************************************************************
  *                                                                     *
  * void spi_init():                                                    *
  *   initialization of the spi interface and selection of its          *
  *   configuration.                                                    *
  *                                                                     *
  *   Parameters:                                                       *
  *     -                                                               *
  *                                                                     *
  *   Return:                                                           *
  *     -                                                               *
  *                                                                     *
  *   Note: This is an example, replaced with SPI code for rapsberry    *
  *                                                                     *
  ***********************************************************************
*/

	int Status;

	Status = XGpio_Initialize(&Gpio_data, GPIO_DEVICE_DATA);

	if (Status != XST_SUCCESS){
		return XST_FAILURE;
	}

	Status = XGpio_Initialize(&Gpio_control, GPIO_DEVICE_CONTROL);

	if (Status != XST_SUCCESS){
			return XST_FAILURE;
	}

	XGpio_SelfTest(&Gpio_data);
	XGpio_SelfTest(&Gpio_control);

	XGpio_SetDataDirection(&Gpio_data, RECIVER_CHANNEL, 1);
	XGpio_SetDataDirection(&Gpio_data, SENDER_CHANNEL, 0);

	XGpio_SetDataDirection(&Gpio_control, END_CHANNEL, 1);
	XGpio_SetDataDirection(&Gpio_control, START_CHANNEL, 0);

  return;
}



void spi_data(char *tx_data, char *rx_data, int len) {
/*
  ***********************************************************************
  *                                                                     *
  * void spi_data(char *tx_data, char *rx_data, int len):               *
  *   Perform a SPI operation                                           *
  *                                                                     *
  *   Parameters:                                                       *
  *     - char *tx_data: Pointer to an array of char to send to the     *
  *         module.                                                     *
  *     - char *rx_data: Pointer to an array of char where the data     *
  *         received will be written.                                   *
  *     - int len: Number of bytes in the arrays                        *
  *                                                                     *
  *   Return:                                                           *
  *     -                                                               *
  *                                                                     *
  *   Note: This is an example, replaced with SPI code for rapsberry    *
  *                                                                     *
  ***********************************************************************
*/

  int ready = 0;

  XGpio_DiscreteWrite(&Gpio_data, SENDER_CHANNEL, *tx_data);
  XGpio_DiscreteWrite(&Gpio_control, START_CHANNEL, 1);

  while (!ready) {
    end = XGpio_DiscreteRead(&Gpio_control, END_CHANNEL);

    if(end){
      ready = 1;
      *rx_data = XGpio_DiscreteRead(&Gpio_data, RECIVER_CHANNEL);
    }

  }

  XGpio_DiscreteWrite(&Gpio_control, START_CHANNEL, 0);

  return;
}
