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
#include "bcm2835.h"

// Global parameters to be used by external libraries
#define CS_0 RPI_GPIO_P1_22
#define CS_1 RPI_V2_GPIO_P1_37


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

	if(!bcm2835_init())
	{
		printf("bcm2835_init() failed\n");
		return;
	}

	bcm2835_gpio_fsel(CS_0, BCM2835_GPIO_FSEL_OUTP);
	bcm2835_gpio_fsel(CS_1, BCM2835_GPIO_FSEL_OUTP);

	if(!bcm2835_spi_begin())
	{
		printf("bcm2835_spi_begin() failed\n");
		return;
	}

	if(!bcm2835_aux_spi_begin())
	{
		printf("bcm2835_aux_spi_begin() failed\n");
		return;
	}

	bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_32);
	bcm2835_aux_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_32);
	bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);
	bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);
	bcm2835_spi_chipSelect(BCM2835_SPI_CS0);

	bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW);

  return;
}


void spi_end() {
/*
  ***********************************************************************
  *                                                                     *
  * void spi_end():                                                     *
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

	bcm2835_spi_end();
	bcm2835_aux_spi_end();

	bcm2835_close();

	return;
}


void spi_data(char *tx_data, char *rx_data, int len, int device) {
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

	if (device == 1) {
		bcm2835_spi_transfernb(tx_data, rx_data, len);
	} else {
		bcm2835_aux_spi_transfernb(tx_data, rx_data, len);
	}

  return;
}



void change_cs(int state, int device) {
/*
  ***********************************************************************
  *                                                                     *
  * void change_cs(int state, int device):                              *
  *   Change the chip select input of the device.                       *
  *                                                                     *
  *   Parameters:                                                       *
  *     - int state: state to set the cs.                               *
  *     - int device: device to change the cs.                          *
  *                                                                     *
  *   Return:                                                           *
  *     -                                                               *
  *                                                                     *
  *   Note: This is an example, replaced with SPI code for rapsberry    *
  *                                                                     *
  ***********************************************************************
*/

	if (device == 1) {
		bcm2835_gpio_write(CS_0, state == 1 ? HIGH : LOW);
	} else {
		bcm2835_gpio_write(CS_1, state == 1 ? HIGH : LOW);
	}

	return;
}



int read_irq(int device) {
/*
  ***********************************************************************
  *                                                                     *
  * int read_irq(int device):                                           *
  *   Read the irq port of the device.                                  *
  *                                                                     *
  *   Parameters:                                                       *
  *     - int device: device to read the irq port.                      *
  *                                                                     *
  *   Return:                                                           *
  *     - int: irq port value.                                          *
  *                                                                     *
  *   Note: This is an example, replaced with SPI code for rapsberry    *
  *                                                                     *
  ***********************************************************************
*/

	/*

	if (device == 1) {
		return XGpio_DiscreteRead(&Gpio_signal_1, IRQ_CHANNEL);
	} else {
		return XGpio_DiscreteRead(&Gpio_signal_2, IRQ_CHANNEL);
	}

	*/

	printf("\r\n Hola desde read_irq");

	return 0;
}
