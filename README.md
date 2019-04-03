# MTP-software


## RF module library

To simplify the development of the highest level software we have created this library where the basic functions to operate on the IC are collected.

This library consists of two parts, one dedicated to the control of the SPI protocol between the micro and the module. And another responsible for simplifying the commands described in the datasheet of the module nRF24L01.

#### SPI connector

In this part of the library have been defined two functions that will be used by the rest of the library. And in this way to get our software independent of any external library that is used.

```c
  void spi_init();
  void spi_data(char *tx_data, char *rx_data, int len);
```

The first function should be called only when the system is turned on in order to configure the SPI connection.
The second function will be the function responsible for performing an SPI operation, where two pointers to char arrays and the length of them are passed as attributes. One of the arrays will contain the bytes to be transmitted and another one where the received bytes will be written.



#### nRF24L01 commands

Coming soon!!

## PPP

Coming soon!!

## Network protocol

Coming soon!!
