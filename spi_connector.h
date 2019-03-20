/*
 * spi_connector.h
 *
 *  Created on: March 19, 2018
 *      Author: Adrian Rodriguez
 */

#ifndef SPI_CONNECTOR_H_
#define SPI_CONNECTOR_H_

extern void spi_init();

extern void spi_data(char *tx_data, char *rx_data, int len);

#endif /* SPI_CONNECTOR_H_ */
