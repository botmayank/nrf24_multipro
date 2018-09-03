# nrf24_multipro_h8_pc
nRF24L01 multi-protocol RC transmitter project being used for JJRC/Eachine H8 mini to control over Serial. This project aims to develop a USB dongle to control the H8 directly from the PC using the nRF24L01+ module and later expand to control and/or charge multiple quadcopters with this custom hardware based on the Arduino Leonardo (Atmega32u4).

The main Arduino code is in the nRF24_multipro folder with the main sketch being nRF24_multipro.ino. The script to control the quad over serial is serial_test.py while the board files for the Quadstick are in the hardware_design folder.

This project is based on the work of perrystao:
https://github.com/perrytsao/nrf24_cx10_pc

which in turn is based upon the awesome nrf24_multipro project by goebish:
https://github.com/goebish/nrf24_multipro

Arduino Nano and nRF24L01+ Module on perfboard to control Syma X20

![Nano+nRF Syma X20](/media/Nano_X20?raw=true)

## Connections

| Arduino Uno/Nano    | NRF24L01+ Module               | nRF Pin No.   |
|---------------------|--------------------------------|---------------|
| GND                 | GND                            | 1             |
| 3.3V                | VCC                            | 2             |
| D5 (Digital 5)      | CE                             | 3             |
| A1 (Analog 1)       | CSN                            | 4             |
| D4 (Digital 4)      | SCK                            | 5             |
| D3 (Digital 3)      | MOSI                           | 6             |
| A0 (Analog 0)       | MISO                           | 7             |
| Not Used            | IRQ                            | 8             |
