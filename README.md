# nrf24_multipro_h8_pc
nRF24L01 multi-protocol RC transmitter project being used for JJRC/Eachine H8 mini to control over Serial. This project aims to develop a USB dongle to control the H8 directly from the PC using the nRF24L01+ module and later expand to control and/or charge multiple quadcopters with this custom hardware based on the Arduino Leonardo (Atmega32u4).

The main Arduino code is in the nRF24_multipro folder with the main sketch being nRF24_multipro.ino. The script to control the quad over serial is serial_test.py while the board files for the Quadstick are in the hardware_design folder.

This project is based on the work of perrystao:
https://github.com/perrytsao/nrf24_cx10_pc

which in turn is based upon the awesome nrf24_multipro project by goebish:
https://github.com/goebish/nrf24_multipro
