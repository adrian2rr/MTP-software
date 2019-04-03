/*
 * constants.h
 *
 *  Created on: March 19, 2018
 *      Author: Adrian Rodriguez
 */

#ifndef CONSTANTS_H_
#define CONSTANTS_H_

//#define PAYLOAD_LENGTH 32

#define IRQ_ON    0x00
#define IRQ_OFF   0x01
#define CRC_1B    0x00
#define CRC_2B    0x01
#define PRX       0X01
#define PTX       0x00
#define SET       0X01
#define NO_SET    0X00

typedef struct DEVICE_CONFIG {
    char irq_rx;        //[IRQ_ON,IRQ_OFF]
    char irq_tx;        //[IRQ_ON,IRQ_OFF]
    char irq_max;       //[IRQ_ON,IRQ_OFF]
    char crc;           //[NO_SET,SET]
    char crc_coding;    //[CRC_1B,CRC_2B]
    char power;         //[NO_SET,SET]
    char mode;          //[PTX,PRX]
} DEVICE_CONFIG;


#define PWR_18    0x00
#define PWR_12    0X01
#define PWR_6     0x02
#define PWR_0     0x03
#define RATE_250  0X00
#define RATE_1    0X01
#define RATE_2    0X02

typedef struct RF_CONFIG {
    char channel;       //[0x00 - 0x7F]
    char con_carrier;   //[NO_SET,SET]
    char output_power;  //[PWR_18,PWR_12,PWR_6,PWR_0]
    char rate;          //[RATE_250,RATE_1,RATE_2]
    char pll;			//[NO_SET,SET]
} RF_CONFIG;


#define IRQ_SET   0x01
#define IRQ_CLEAR 0X00

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

#define ADDRESS_3B  0X01
#define ADDRESS_4B  0x02
#define ADDRESS_5B  0x03

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

// Commands constants
#define REGISTER_CONFIG_R     0x00
#define REGISTER_CONFIG_W     0x20

#define REGISTER_AUTO_ACK_R   0X01
#define REGISTER_AUTO_ACK_W   0X21

#define REGISTER_PIPE_ST_R    0X02
#define REGISTER_PIPE_ST_W    0x22

#define REGISTER_ADDR_WITD_R  0x03
#define REGISTER_ADDR_WITD_W  0x23

#define REGISTER_CHANNEL_R    0x05
#define REGISTER_CHANNEL_W    0x25

#define REGISTER_RF_R         0x06
#define REGISTER_RF_W         0x26

#define REGISTER_STATUS_R     0x07
#define REGISTER_STATUS_W     0x27

#define REGISTER_PWD_DET      0x09

#define REGISTER_RX_ADD_R     0x0A
#define REGISTER_RX_ADD_W     0x2A

#define REGISTER_TX_ADD_R     0x10
#define REGISTER_TX_ADD_W     0x30

#define REGISTER_RX_0_P_R	    0x11
#define REGISTER_RX_0_P_W     0x31

#define REGISTER_FIFO_R       0x17

#define REGISTER_FEATURE_R    0x1D
#define REGISTER_FEATURE_W    0x3D

#define PAYLOAD_R             0x61
#define PAYLOAD_W             0xA0
#define PAYLOAD_W_NA		      0xB0

#define FLUSH_RX              0xE2
#define FLUSH_TX              0xE1

#define READ_STATUS           0xFF

#define PADDING               0x00

#endif /* CONSTANTS_H_ */

/* -------------------------------------------------------------------
  Commands

  Register:
    - Read:       000X XXXX [1 to 5 LSBF]   =>  2 to 6 bytes
    - Write:      001X XXXX [1 to 5 LSBF]   =>  2 to 6 bytes

  Payload:
    - Read:       0110 0001 [1 to 32 LSBF]  =>  2 to 33 bytes
    - Write:      1010 0000 [1 to 32 LSBF]  =>  2 to 33 bytes

  Flush FIFO:
    - RX:         1110 0010                 =>  1 bytes
    - TX:         1110 0001                 =>  1 bytes
    - Reuse TX:   1110 0011                 =>  1 bytes

  Reuse TX Payload:
    - Activate    1110 0011                 =>  1 bytes

  ACK:
    - Payload     1010 1PPP [1 to 32 LSBF]  =>  2 to 33 bytes
    - TX no ACK   1011 0000 [1 to 32 LSBF]  =>  2 to 33 bytes

  NOP:
    - Read STATUS 1111 1111                 =>  1 bytes
------------------------------------------------------------------- */
/* -------------------------------------------------------------------
  Register

  Config: Read [0x00] - Write [0x20]
    Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    RV  | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
    ---------
      - 7:  [RW]  only '0'
      - 6:  [RW]  IRQ by RX_DR  (Received message)            [1 disabled - 0 active  ]
      - 5:  [RW]  IRQ by TX_DS  (message TX or ACK received)  [1 disabled - 0 active  ]
      - 4:  [RW]  IRQ by MAX_RT (Max Retramissions)           [1 disabled - 0 active  ]
      - 3:  [RW]  Enable CRC                                  [1 enabled  - 0 disabled]
      - 2:  [RW]  CRC encodign scheme                         [1 2 bytes  - 0 1 bytes ]
      - 1:  [RW]  Power up                                    [1 Power up - 0 Power Down]
      - 0:  [RW]  RX/TX controlled (PRIM_RX)                  [1 PRX      - 0 PTX     ]

  --------------------------

  Enhanced ShockBurst: Read [0x01] - Write [0x21]
    Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    RV  | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 |
    ---------
      - 7:  [RW]  only '0'
      - 6:  [RW]  only '0'
      - 5:  [RW]  Enable auto acknowledgement data pipe 5     [1 active - 0 disabled  ]
      - 4:  [RW]  Enable auto acknowledgement data pipe 4     [1 active - 0 disabled  ]
      - 3:  [RW]  Enable auto acknowledgement data pipe 3     [1 active - 0 disabled  ]
      - 2:  [RW]  Enable auto acknowledgement data pipe 2     [1 active - 0 disabled  ]
      - 1:  [RW]  Enable auto acknowledgement data pipe 1     [1 active - 0 disabled  ]
      - 0:  [RW]  Enable auto acknowledgement data pipe 0     [1 active - 0 disabled  ]

  --------------------------

  Enabled RX Addresses: Read [0x02] - Write [0x22]
    Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    RV  | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
    ---------
      - 7:  [RW]  only '0'
      - 6:  [RW]  only '0'
      - 5:  [RW]  Enable data pipe 5     [1 active - 0 disabled  ]
      - 4:  [RW]  Enable data pipe 4     [1 active - 0 disabled  ]
      - 3:  [RW]  Enable data pipe 3     [1 active - 0 disabled  ]
      - 2:  [RW]  Enable data pipe 2     [1 active - 0 disabled  ]
      - 1:  [RW]  Enable data pipe 1     [1 active - 0 disabled  ]
      - 0:  [RW]  Enable data pipe 0     [1 active - 0 disabled  ]

  --------------------------

  Address Widths: Read [0x03] - Write [0x23]
    Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    RV  | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
    ---------
      - 7:  [RW]  only '0'
      - 6:  [RW]  only '0'
      - 5:  [RW]  only '0'
      - 4:  [RW]  only '0'
      - 3:  [RW]  only '0'
      - 2:  [RW]  only '0'
      - 1-0:  [RW]  RX/TX Address field width [3 bytes, 4 bytes, 5 bytes]

  --------------------------

  Retransmission: Read [0x04] - Write [0x24]
    Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    RV  | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
    ---------
      - 7-4:  [RW]  Retransmission delay 250us + [7:4] * 250us
      - 3-0:  [RW]  Retransmission count [0 disabled - 1:15 Retransmissions]

  --------------------------

  RF Channel: Read [0x05] - Write [0x25]
    Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    RV  | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
    ---------
      - 7:  [RW]  only '0'
      - 6-0:[RW]  Frequency channel (2400 MHz + [6:0] MHz)

      Note: 2Mbps bandwith can overlap

  --------------------------

  RF Setup:   Read [0x06] - Write [0x26]
    Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    RV  | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 |
    ---------
      - 7:  [RW]  Continuous carrier
      - 6:  [RW]  only '0'
      - 5:  [RW]  RF Data Rate to 250 kbps          [1 enable - 0 disabled]
      - 4:  [RW]  Force PLL lock signal (only test) [1 enable - 0 disabled]
      - 3:  [RW]  Select Data rate           [0: 1Mbps, 1: 2Mbps]  Note: only when bit 5 (250 kbps) disabled
      - 2-1:[RW]  RF output power     (-18 dBm + [2:1] * 6 dB)
      - 0:        Don't care

  --------------------------

  Status:     Read [0x07] - Write [0x27]
    Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    RV  | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 |
    ---------
      - 7:  [RW]  only '0'
      - 6:  [RW]  Data Ready RX (write 1 to clear)  [1 data ready   - 0 not]
      - 5:  [RW]  Data sent or ACK (1 to clear)     [1 data sent    - 0 not]
      - 4:  [RW]  Max retramissions (1 to clear)    [1 max reached  - 0 not]
      - 3-1: [R]  Data pipe number for Payload [000:101 Pipe#, 110 Not used, 111 FIFO empty]
      - 0:   [R]  TX FIFO full                      [1 full         - 0 not]

  --------------------------

  TX observe: Read [0x08]
    Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    RV  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
    ---------
      - 7-4:  [R] Count Lost Packets - Note: Overflow protected, to reset write to RF_CH
      - 3-0:  [R] Count Retramissions - Note: Counter reset with new packet transmission

  --------------------------

  Power Detector: Read [0x09]
    Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    RV  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
    ---------
      - 7-1:  [R] Reserved
      - 0:    [R] Received Power Detector (-64 dBm threshold)

  --------------------------

  FIFO Status: Read [0x17]
    Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    RV  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
    ---------
      - 7:  [R] only '0'
      - 6:  [R] TX Payload Reuse  (reset flushing tx)
      - 5:  [R] TX FIFO full                            [1 full   - 0 not]
      - 4:  [R] TX FIFO empty                           [1 empty  - 0 not]
      - 3-2:[R] only '00'
      - 1:  [R] RX FIFO full                            [1 full   - 0 not]
      - 0:  [R] RX FIFO empty                           [1 empty  - 0 not]

  --------------------------

  FEATURE: Read [0x1D] - Write [0x3D]
    Bit | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    RV  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
    ---------
      - 7-3: [R] only '0'
      - 2:  [RW] Dynamic payload length
      - 1:  [RW] Payload with ACK
      - 0:  [RW] No ACK

------------------------------------------------------------------- */
