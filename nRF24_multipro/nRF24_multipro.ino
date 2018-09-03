/*
 Forked from perrytsao's Cheerson CX-10 project for JJRC H8 Mini/H8 3D 
 as well as Syma X20.
 This sketch is to interact with a Python script running on a Linux 
 machine to control the drone.
 *  
 * 
 * Mayank Joneja 3 Sep 2018
 * botmayank on github.com
 * 
 ******************************************************************************
 This is a fork of the Multi-Protocol nRF24L01 Tx project
 from goebish on RCgroups / github
 This version accepts serial port strings and converts
 them to ppm commands which are then transmitted via
 the nRF24L01. 

 The purpose of this code is to enable control over the Cheerson CX-10 
 drone via code running on a PC.  In my case, I am developing Python code to
 fly the drone. 
 
 This code can be easily adapted to the other mini-drones 
 that the Multi-protocol board supports. 

 The format for the serial command is:
 ch1value,ch2value,ch3value,...
 e.g.:  1500,1800,1200,1100, ...

 Up to 12 channel commands can be submitted. The channel order is defined
 by chan_order. The serial port here is running at 115200bps. 

 Python code in serial_test.py was written to generate the serial strings.  

 Hardware used:
 This code was tested on the Arduino Uno and nRF24L01 module. 
 Wiring diagrams and more info on this project at www.makehardware.com/pc-mini-drone-controller.html
 
 I believe this code will remain compatible with goebish's 
 nRF24L01 Multi-Protocol board.  A way to 
 connect to the serial port will be needed (such as the FTDI). 
 
 Perry Tsao 29 Feb 2016
 perrytsao on github.com
 *********************************************************************************

 
 ##########################################
 #####   MultiProtocol nRF24L01 Tx   ######
 ##########################################
 #        by goebish on rcgroups          #
 #                                        #
 #   Parts of this project are derived    #
 #     from existing work, thanks to:     #
 #                                        #
 #   - PhracturedBlue for DeviationTX     #
 #   - victzh for XN297 emulation layer   #
 #   - Hasi for Arduino PPM decoder       #
 #   - hexfet, midelic, closedsink ...    #
 ##########################################


 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License.
 If not, see <http://www.gnu.org/licenses/>.
 */

#include <util/atomic.h>
#include <EEPROM.h>
#include "iface_nrf24l01.h"
#include <string.h>

// ############ Wiring ################
#define PPM_pin   2  // PPM in
//SPI Comm.pins with nRF24L01
#define MOSI_pin  3  // MOSI - D3
#define SCK_pin   4  // SCK  - D4
#define CE_pin    5  // CE   - D5
#define MISO_pin  A0 // MISO - A0
#define CS_pin    A1 // CS   - A1

#define ledPin    13 // LED  - D13

enum {
  SYMA,
  JJRC_H8,
  JJRC_H8_3D  
};

// SPI outputs
#define MOSI_on PORTD |= _BV(3)  // PD3
#define MOSI_off PORTD &= ~_BV(3)// PD3
#define SCK_on PORTD |= _BV(4)   // PD4
#define SCK_off PORTD &= ~_BV(4) // PD4
#define CE_on PORTD |= _BV(5)    // PD5
#define CE_off PORTD &= ~_BV(5)  // PD5
#define CS_on PORTC |= _BV(1)    // PC1
#define CS_off PORTC &= ~_BV(1)  // PC1
// SPI input
#define  MISO_on (PINC & _BV(0)) // PC0

#define RF_POWER TX_POWER_80mW 

// PPM stream settings
#define CHANNELS 12 // number of channels in ppm stream, 12 ideally
enum chan_order{
    THROTTLE,
    AILERON,
    ELEVATOR,
    RUDDER,
    AUX1,  // (CH5)  led light, or 3 pos. rate on CX-10, H7, or inverted flight on H101
    AUX2,  // (CH6)  flip control
    AUX3,  // (CH7)  still camera (snapshot)
    AUX4,  // (CH8)  video camera
    AUX5,  // (CH9)  headless
    AUX6,  // (CH10) calibrate Y (V2x2), pitch trim (H7), RTH (Bayang, H20), 360deg flip mode (H8-3D, H22)
    AUX7,  // (CH11) calibrate X (V2x2), roll trim (H7)
    AUX8,  // (CH12) Reset / Rebind
};

#define PPM_MIN 1000
#define PPM_SAFE_THROTTLE 1050 
#define PPM_MID 1500
#define PPM_MAX 2000
#define PPM_MIN_COMMAND 1300
#define PPM_MAX_COMMAND 1700
#define GET_FLAG(ch, mask) (ppm[ch] > PPM_MAX_COMMAND ? mask : 0)

// supported protocols
enum {
    PROTO_V2X2 = 0,     // WLToys V2x2, JXD JD38x, JD39x, JJRC H6C, Yizhan Tarantula X6 ...
    PROTO_CG023,        // EAchine CG023, CG032, 3D X4
    PROTO_CX10_BLUE,    // Cheerson CX-10 blue board, newer red board, CX-10A, CX-10C, Floureon FX-10, CX-Stars (todo: add DM007 variant)
    PROTO_CX10_GREEN,   // Cheerson CX-10 green board
    PROTO_H7,           // EAchine H7, MoonTop M99xx
    PROTO_BAYANG,       // EAchine H8(C) mini, H10, BayangToys X6, X7, X9, JJRC JJ850, Floureon H101
    PROTO_SYMAX5C1,     // Syma X5C-1 (not older X5C), X11, X11C, X12
    PROTO_YD829,        // YD-829, YD-829C, YD-822 ...
    PROTO_H8_3D,        // EAchine H8 mini 3D, JJRC H20, H22
    PROTO_END
};

// EEPROM locations
enum{
    ee_PROTOCOL_ID = 0,
    ee_TXID0,
    ee_TXID1,
    ee_TXID2,
    ee_TXID3
};

uint16_t overrun_cnt=0;
uint8_t transmitterID[4];
uint8_t current_protocol;
static volatile bool ppm_ok = false;
uint8_t packet[32];
static bool reset=true;
volatile uint16_t Servo_data[12];
static uint16_t ppm[12] = {PPM_MIN,PPM_MID,PPM_MID,PPM_MID,PPM_MID,PPM_MID,
                           PPM_MID,PPM_MID,PPM_MID,PPM_MID,PPM_MID,PPM_MID,};

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
char *p, *i;
char* c = new char[200 + 1]; // match 200 characters reserved for inputString later
char* errpt;
uint8_t ppm_cnt;

uint8_t drone = SYMA;

void setup()
{
    
    randomSeed((analogRead(A4) & 0x1F) | (analogRead(A5) << 5));
    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, LOW); //start LED off
    pinMode(PPM_pin, INPUT);
    pinMode(MOSI_pin, OUTPUT);
    pinMode(SCK_pin, OUTPUT);
    pinMode(CS_pin, OUTPUT);
    pinMode(CE_pin, OUTPUT);
    pinMode(MISO_pin, INPUT);

    // PPM ISR setup
    //attachInterrupt(PPM_pin - 2, ISR_ppm, CHANGE);
    TCCR1A = 0;  //reset timer1
    TCCR1B = 0;
    TCCR1B |= (1 << CS11);  //set timer1 to increment every 1 us @ 8MHz, 0.5 us @16MHz

    set_txid(false);

    // Serial port input/output setup
    Serial.begin(115200);
    // reserve 200 bytes for the inputString:
    inputString.reserve(200);
}

void loop()
{
    uint32_t timeout;
    // reset / rebind
    if(reset || ppm[AUX8] > PPM_MAX_COMMAND) {
        reset = false;
        Serial.println("Selecting protocol");
        selectProtocol();        
        NRF24L01_Reset();
        Serial.println("nrf24l01 reset.");
        NRF24L01_Initialize();
        Serial.println("nrf24l01 init.");
        init_protocol();
    }
    // process protocol
    switch(current_protocol) {
        case PROTO_CG023: 
        case PROTO_YD829:
            timeout = process_CG023();
            break;
        case PROTO_V2X2: 
            timeout = process_V2x2();
            break;
        case PROTO_CX10_GREEN:
        case PROTO_CX10_BLUE:
            timeout = process_CX10(); // returns micros()+6000 for time to next packet. 
            break;
        case PROTO_H7:
            timeout = process_H7();
            break;
        case PROTO_BAYANG:
            timeout = process_Bayang();
            break;
        case PROTO_SYMAX5C1:
            timeout = process_SymaX(); 
            break;
        case PROTO_H8_3D:
            timeout = process_H8_3D();
            break;
    }
    // updates ppm values out of ISR
    //update_ppm();
    overrun_cnt=0;

    // Process string into tokens and assign values to ppm
    // The Arduino will also echo the command values that it assigned
    // to ppm
    if (stringComplete) {
        // process string        
        strcpy(c, inputString.c_str());
        p = strtok_r(c,",",&i); // returns substring up to first "," delimiter
        ppm_cnt=0;
        while (p !=0){
          //Serial.print(p);
          int val=strtol(p, &errpt, 10);
          if (!*errpt) {
            Serial.print(val);
            ppm[ppm_cnt]=val;
          }
          else
            Serial.print("x"); // prints "x" if it could not decipher the command. Other values in string may still be assigned.
          Serial.print(";"); // a separator between ppm values
          p = strtok_r(NULL,",",&i);
          ppm_cnt+=1;
        }
        Serial.println("."); // prints "." at end of command
        //ppm[0]=       
        
        // clear the string:
        inputString = "";
        stringComplete = false;
    }
    
    // Read the string from the serial buffer
    while (Serial.available()) {
      // get the new byte:
      char inChar = (char)Serial.read();
      // if the incoming character is a newline, set a flag
      // so the main loop can do something about it:
      if (inChar == '\n') {
        stringComplete = true;
      }
      else {      
        // add it to the inputString:
        inputString += inChar;
      }
      
    }
    // wait before sending next packet
    while(micros() < timeout) // timeout for CX-10 blue = 6000microseconds. 
    {
      //overrun_cnt+=1;
    };
    /* // Compare counter to debug for overruns
    if ((overrun_cnt<1000)||(stringComplete)) {
      Serial.println(overrun_cnt);
    }
    */
}

void set_txid(bool renew)
{
    uint8_t i;
    for(i=0; i<4; i++)
        transmitterID[i] = EEPROM.read(ee_TXID0+i);
    if(renew || (transmitterID[0]==0xFF && transmitterID[1]==0x0FF)) {
        for(i=0; i<4; i++) {
            transmitterID[i] = random() & 0xFF;
            EEPROM.update(ee_TXID0+i, transmitterID[i]); 
        }            
    }
}

void selectProtocol()
{
    // wait for multiple complete ppm frames
    ppm_ok = false;
    /*
    uint8_t count = 10;
    while(count) {
        while(!ppm_ok) {} // wait
        update_ppm();
        if(ppm[AUX8] < PPM_MAX_COMMAND) // reset chan released
            count--;
        ppm_ok = false;
    }
    */
    // startup stick commands
    
    //if(ppm[RUDDER] < PPM_MIN_COMMAND)        // Rudder left
    set_txid(true);                      // Renew Transmitter ID
    
    // protocol selection
    Serial.println("Current protocol:");
    switch(drone){
      case SYMA:
        Serial.println("SYMA");
        current_protocol = PROTO_SYMAX5C1; // Syma X5C-1, X11, X11C, X12
        break;
      case JJRC_H8:
        Serial.println("BAYANG");
        current_protocol = PROTO_BAYANG;    // EAchine H8(C) mini, BayangToys X6/X7/X9, JJRC JJ850 ...
        break;
      case JJRC_H8_3D:
        Serial.println("JJRC_H8_3D");
        current_protocol = PROTO_H8_3D; // H8 mini 3D, H20 ...
        break;      
      default:
        Serial.println("None!");
    }    
    // wait for safe throttle
    /*while(ppm[THROTTLE] > PPM_SAFE_THROTTLE) {
        delay(100);
        update_ppm();
    }
    */
}

void init_protocol()
{
    switch(current_protocol) {
        case PROTO_CG023:
        case PROTO_YD829:
            CG023_init();
            CG023_bind();
            break;
        case PROTO_V2X2:
            V2x2_init();
            V2x2_bind();
            break;
        case PROTO_CX10_GREEN:
        case PROTO_CX10_BLUE:
            CX10_init();
            CX10_bind();            
            break;
        case PROTO_H7:
            H7_init();
            H7_bind();
            break;
        case PROTO_BAYANG:
            Bayang_init();
            Bayang_bind();
            Serial.println("Bayang initialized and bound");
            break;
        case PROTO_SYMAX5C1:
            Symax_init();
            SymaX_bind();
            Serial.println("Syma initialized and bound");
            break;
        case PROTO_H8_3D:
            H8_3D_init();
            H8_3D_bind();
            Serial.println("H8 3D initialized and bound");
            break;
    }
}
