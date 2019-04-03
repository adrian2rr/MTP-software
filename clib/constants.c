/*
 * constants.c
 *
 *  Created on: March 19, 2018
 *      Author: Adrian Rodriguez
 */

typedef struct DEVICE_CONFIG {
    char irq_rx;        //[IRQ_ON,IRQ_OFF]
    char irq_tx;        //[IRQ_ON,IRQ_OFF]
    char irq_max;       //[IRQ_ON,IRQ_OFF]
    char crc;           //[NO_SET,SET]
    char crc_coding;    //[CRC_1B,CRC_2B]
    char power;         //[NO_SET,SET]
    char mode;          //[PTX,PRX]
} DEVICE_CONFIG;

typedef struct RF_CONFIG {
    char channel;       //[0x00 - 0x7F]
    char con_carrier;   //[NO_SET,SET]
    char output_power;  //[PWR_18,PWR_12,PWR_6,PWR_0]
    char rate;          //[RATE_250,RATE_1,RATE_2]
    char pll;			//[NO_SET,SET]
} RF_CONFIG;

typedef struct STATUS {
    char rx_data;       //[NO_SET,SET]
    char tx_data;       //[NO_SET,SET]
    char max_retrans;   //[NO_SET,SET]
} STATUS;

typedef struct FIFO_STATUS {
    char tx_full;       //[NO_SET,SET]
    char tx_empty;      //[NO_SET,SET]
    char rx_full;       //[NO_SET,SET]
    char rx_empty;      //[NO_SET,SET]
    char tx_reuse;      //[NO_SET,SET]
} FIFO_STATUS;

typedef struct PIPES {
    char pipe0;         //[NO_SET,SET]
    char pipe1;         //[NO_SET,SET]
    char pipe2;         //[NO_SET,SET]
    char pipe3;         //[NO_SET,SET]
    char pipe4;         //[NO_SET,SET]
    char pipe5;         //[NO_SET,SET]
} PIPES;

typedef struct AUTO_ACK {
    char pipe0;         //[NO_SET,SET]
    char pipe1;         //[NO_SET,SET]
    char pipe2;         //[NO_SET,SET]
    char pipe3;         //[NO_SET,SET]
    char pipe4;         //[NO_SET,SET]
    char pipe5;         //[NO_SET,SET]
} AUTO_ACK;

typedef struct FEATURE {
    char dynamic_pay;   //[NO_SET,SET]
    char payload_ack;   //[NO_SET,SET]
    char no_ack;        //[NO_SET,SET]
} FEATURE;

typedef struct TRANSCIEVER {
    DEVICE_CONFIG device_config;
    RF_CONFIG rf_config;
    STATUS status;
    FIFO_STATUS fifo_status;
    PIPES pipes;
    AUTO_ACK auto_ack;
    FEATURE feature;
    char address_width;
    char mode;
} TRANSCIEVER;
