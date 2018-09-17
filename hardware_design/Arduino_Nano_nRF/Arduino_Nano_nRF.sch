EESchema Schematic File Version 4
LIBS:Arduino_Nano_nRF-cache
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date "jeu. 02 avril 2015"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Label 2350 2800 0    60   ~ 0
1(Tx)
Text Label 2350 2900 0    60   ~ 0
0(Rx)
Text Label 2350 3000 0    60   ~ 0
Reset
Text Label 2350 3200 0    60   ~ 0
2
Text Label 2350 3300 0    60   ~ 0
3(**)
Text Label 2350 3400 0    60   ~ 0
4
Text Label 2350 3500 0    60   ~ 0
5(**)
Text Label 2350 3600 0    60   ~ 0
6(**)
Text Label 2350 3700 0    60   ~ 0
7
Text Label 2350 3800 0    60   ~ 0
8
Text Label 2350 3900 0    60   ~ 0
9(**)
Text Label 2350 4000 0    60   ~ 0
10(**/SS)
Text Label 2350 4100 0    60   ~ 0
11(**/MOSI)
Text Label 2350 4200 0    60   ~ 0
12(MISO)
Text Label 4200 4200 0    60   ~ 0
13(SCK)
Text Label 4200 3900 0    60   ~ 0
A0
Text Label 4200 3800 0    60   ~ 0
A1
Text Label 4200 3700 0    60   ~ 0
A2
Text Label 4200 3600 0    60   ~ 0
A3
Text Label 4200 3500 0    60   ~ 0
A4
Text Label 4200 3400 0    60   ~ 0
A5
Text Label 4200 3300 0    60   ~ 0
A6
Text Label 4200 3200 0    60   ~ 0
A7
Text Label 4200 4000 0    60   ~ 0
AREF
Text Label 4200 3000 0    60   ~ 0
Reset
Text Notes 4450 2700 0    60   ~ 0
Holes
Text Notes 2150 2300 0    60   ~ 0
Shield for Arduino Nano
Text Label 3900 2650 1    60   ~ 0
Vin
Wire Notes Line
	2125 2350 3325 2350
Wire Notes Line
	3325 2350 3325 2175
$Comp
L Connector_Generic:Conn_01x01 P3
U 1 1 56D73ADD
P 4450 2350
F 0 "P3" V 4550 2350 50  0000 C CNN
F 1 "CONN_01X01" V 4550 2350 50  0001 C CNN
F 2 "Socket_Arduino_Nano:1pin_Nano" H 4450 2350 50  0001 C CNN
F 3 "" H 4450 2350 50  0000 C CNN
	1    4450 2350
	0    -1   -1   0   
$EndComp
NoConn ~ 4450 2550
$Comp
L Connector_Generic:Conn_01x01 P4
U 1 1 56D73D86
P 4550 2350
F 0 "P4" V 4650 2350 50  0000 C CNN
F 1 "CONN_01X01" V 4650 2350 50  0001 C CNN
F 2 "Socket_Arduino_Nano:1pin_Nano" H 4550 2350 50  0001 C CNN
F 3 "" H 4550 2350 50  0000 C CNN
	1    4550 2350
	0    -1   -1   0   
$EndComp
$Comp
L Connector_Generic:Conn_01x01 P5
U 1 1 56D73DAE
P 4650 2350
F 0 "P5" V 4750 2350 50  0000 C CNN
F 1 "CONN_01X01" V 4750 2350 50  0001 C CNN
F 2 "Socket_Arduino_Nano:1pin_Nano" H 4650 2350 50  0001 C CNN
F 3 "" H 4650 2350 50  0000 C CNN
	1    4650 2350
	0    -1   -1   0   
$EndComp
$Comp
L Connector_Generic:Conn_01x01 P6
U 1 1 56D73DD9
P 4750 2350
F 0 "P6" V 4850 2350 50  0000 C CNN
F 1 "CONN_01X01" V 4850 2350 50  0001 C CNN
F 2 "Socket_Arduino_Nano:1pin_Nano" H 4750 2350 50  0001 C CNN
F 3 "" H 4750 2350 50  0000 C CNN
	1    4750 2350
	0    -1   -1   0   
$EndComp
NoConn ~ 4550 2550
NoConn ~ 4650 2550
NoConn ~ 4750 2550
$Comp
L Connector_Generic:Conn_01x15 P1
U 1 1 56D73FAC
P 3200 3500
F 0 "P1" H 3200 4300 50  0000 C CNN
F 1 "Digital" V 3300 3500 50  0000 C CNN
F 2 "Socket_Arduino_Nano:Socket_Strip_Arduino_1x15" H 3200 3500 50  0001 C CNN
F 3 "" H 3200 3500 50  0000 C CNN
	1    3200 3500
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x15 P2
U 1 1 56D740C7
P 3600 3500
F 0 "P2" H 3600 4300 50  0000 C CNN
F 1 "Analog" V 3700 3500 50  0000 C CNN
F 2 "Socket_Arduino_Nano:Socket_Strip_Arduino_1x15" H 3600 3500 50  0001 C CNN
F 3 "" H 3600 3500 50  0000 C CNN
	1    3600 3500
	-1   0    0    -1  
$EndComp
$Comp
L power:GND #PWR01
U 1 1 56D7422C
P 2900 4300
F 0 "#PWR01" H 2900 4050 50  0001 C CNN
F 1 "GND" H 2900 4150 50  0000 C CNN
F 2 "" H 2900 4300 50  0000 C CNN
F 3 "" H 2900 4300 50  0000 C CNN
	1    2900 4300
	1    0    0    -1  
$EndComp
Wire Wire Line
	3000 3100 2900 3100
Wire Wire Line
	2900 3100 2900 4300
Wire Wire Line
	3000 2800 2350 2800
Wire Wire Line
	2350 2900 3000 2900
Wire Wire Line
	3000 3000 2350 3000
Wire Wire Line
	2350 3200 3000 3200
Wire Wire Line
	3000 3300 2350 3300
Wire Wire Line
	2350 3400 3000 3400
Wire Wire Line
	3000 3500 2350 3500
Wire Wire Line
	2350 3600 3000 3600
Wire Wire Line
	3000 3700 2350 3700
Wire Wire Line
	2350 3800 3000 3800
Wire Wire Line
	3000 3900 2350 3900
Wire Wire Line
	2350 4000 3000 4000
Wire Wire Line
	3000 4100 2350 4100
Wire Wire Line
	2350 4200 3000 4200
$Comp
L power:GND #PWR02
U 1 1 56D746ED
P 3900 4300
F 0 "#PWR02" H 3900 4050 50  0001 C CNN
F 1 "GND" H 3900 4150 50  0000 C CNN
F 2 "" H 3900 4300 50  0000 C CNN
F 3 "" H 3900 4300 50  0000 C CNN
	1    3900 4300
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 4300 3900 2900
Wire Wire Line
	3900 2900 3800 2900
Wire Wire Line
	3800 2800 3900 2800
Wire Wire Line
	3900 2800 3900 2650
$Comp
L power:+5V #PWR03
U 1 1 56D747E8
P 4000 2650
F 0 "#PWR03" H 4000 2500 50  0001 C CNN
F 1 "+5V" V 4000 2850 28  0000 C CNN
F 2 "" H 4000 2650 50  0000 C CNN
F 3 "" H 4000 2650 50  0000 C CNN
	1    4000 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4000 2650 4000 3100
Wire Wire Line
	4000 3100 3800 3100
$Comp
L power:+3V3 #PWR04
U 1 1 56D74854
P 4100 2650
F 0 "#PWR04" H 4100 2500 50  0001 C CNN
F 1 "+3.3V" V 4100 2850 28  0000 C CNN
F 2 "" H 4100 2650 50  0000 C CNN
F 3 "" H 4100 2650 50  0000 C CNN
	1    4100 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 2650 4100 4100
Wire Wire Line
	4100 4100 3800 4100
Wire Wire Line
	4200 3000 3800 3000
Wire Wire Line
	3800 3200 4200 3200
Wire Wire Line
	4200 3300 3800 3300
Wire Wire Line
	4200 3400 3800 3400
Wire Wire Line
	3800 3500 4200 3500
Wire Wire Line
	4200 3600 3800 3600
Wire Wire Line
	4200 3700 3800 3700
Wire Wire Line
	3800 3800 4200 3800
Wire Wire Line
	4200 3900 3800 3900
Wire Wire Line
	4200 4000 3800 4000
Wire Wire Line
	3800 4200 4200 4200
Wire Notes Line
	4850 2750 4300 2750
Wire Notes Line
	4300 2750 4300 2200
Wire Notes Line
	4850 4550 2100 4550
Wire Notes Line
	2100 4550 2100 2200
Text Notes 3300 2800 0    60   ~ 0
1
Text Notes 7100 6950 0    100  ~ 0
Arduino Nano nRF24L01+ shield\n(c) botmayank 2018
Wire Notes Line
	2100 2200 4850 2200
Wire Notes Line
	4850 2200 4850 4550
$Comp
L nano_nrf:Conn_02x04_Odd_Even J1
U 1 1 5BA0BFE8
P 6500 3050
F 0 "J1" H 6550 3367 50  0000 C CNN
F 1 "Conn_02x04_Odd_Even" H 6550 3276 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x04_P2.54mm_Vertical" H 6500 3050 50  0001 C CNN
F 3 "~" H 6500 3050 50  0001 C CNN
	1    6500 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	6300 3050 5850 3050
Wire Wire Line
	6300 3150 5850 3150
Wire Wire Line
	6300 3250 5850 3250
Wire Wire Line
	6800 2950 7200 2950
Text Notes 6200 3450 0    50   ~ 0
nRF24L01+ Header\n
$Comp
L power:GND #PWR0101
U 1 1 5BA0D080
P 6100 3300
F 0 "#PWR0101" H 6100 3050 50  0001 C CNN
F 1 "GND" H 6100 3150 50  0000 C CNN
F 2 "" H 6100 3300 50  0000 C CNN
F 3 "" H 6100 3300 50  0000 C CNN
	1    6100 3300
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0102
U 1 1 5BA0D0AE
P 7200 2950
F 0 "#PWR0102" H 7200 2800 50  0001 C CNN
F 1 "+5V" H 7200 3150 50  0000 C CNN
F 2 "" H 7200 2950 50  0000 C CNN
F 3 "" H 7200 2950 50  0000 C CNN
	1    7200 2950
	1    0    0    -1  
$EndComp
NoConn ~ 6800 3250
Text Label 5850 3050 0    60   ~ 0
5(**)
Text Label 5850 3150 0    60   ~ 0
4
Text Label 5850 3250 0    60   ~ 0
A0
Text Label 7300 3050 2    60   ~ 0
A1
Text Label 7350 3150 2    60   ~ 0
3(**)
Text Notes 6150 3050 0    50   ~ 0
CE
Text Notes 6850 3050 0    50   ~ 0
CSN
Text Notes 6150 3150 0    50   ~ 0
SCK\n
Text Notes 6800 3150 0    50   ~ 0
MOSI
Wire Wire Line
	6800 3150 7350 3150
Wire Wire Line
	6800 3050 7300 3050
Text Notes 6150 3250 0    50   ~ 0
MISO
Wire Wire Line
	6300 2950 6100 2950
Wire Wire Line
	6100 2950 6100 3300
$EndSCHEMATC
