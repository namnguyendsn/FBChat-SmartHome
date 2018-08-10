/* Copyright 2017 David Conran
*
* An IR LED circuit *MUST* be connected to the ESP8266 on a pin
* as specified by IR_LED below.
*
* TL;DR: The IR LED needs to be driven by a transistor for a good result.
*
* Suggested circuit:
*     https://github.com/markszabo/IRremoteESP8266/wiki#ir-sending
*
* Common mistakes & tips:
*   * Don't just connect the IR LED directly to the pin, it won't
*     have enough current to drive the IR LED effectively.
*   * Make sure you have the IR LED polarity correct.
*     See: https://learn.sparkfun.com/tutorials/polarity/diode-and-led-polarity
*   * Typical digital camera/phones can be used to see if the IR LED is flashed.
*     Replace the IR LED with a normal LED if you don't have a digital camera
*     when debugging.
*   * Avoid using the following pins unless you really know what you are doing:
*     * Pin 0/D3: Can interfere with the boot/program mode & support circuits.
*     * Pin 1/TX/TXD0: Any serial transmissions from the ESP8266 will interfere.
*     * Pin 3/RX/RXD0: Any serial transmissions to the ESP8266 will interfere.
*   * ESP-01 modules are tricky. We suggest you use a module with more GPIOs
*     for your first time. e.g. ESP-12 etc.
*/
#ifndef UNIT_TEST
#include <Arduino.h>
#endif
#include <IRremoteESP8266.h>
#include <IRsend.h>
#include <ir_Mitsubishi.h>

#define STATE_IDLE 0
#define STATE_START 1
#define STATE_DATA 2
#define STATE_END 3

#define IR_LED 4  // ESP8266 GPIO pin to use. (D2).
IRMitsubishiAC mitsubir(IR_LED);  // Set the GPIO used for sending messages.
uint8_t incomingByte;

#define BUFF_SIZE 10
uint8_t g_incomeBuff[BUFF_SIZE];
uint8_t g_incomeCnt;
uint8_t g_val[10] = "         ";
uint8_t g_state;

void printState() {
    Serial.printf("Power: %d,  Mode: %d, Temp: %dC, Fan Speed: %d," \
                    " Vane Mode: %d\n",
                mitsubir.getPower(), mitsubir.getMode(), mitsubir.getTemp(),
                mitsubir.getFan(), mitsubir.getVane());
}

void setup() {
    mitsubir.begin();
    Serial.begin(115200);
    delay(200);

    // Set up what we want to send. See ir_Mitsubishi.cpp for all the options.
    Serial.println("Default state of the remote.");
    printState();
    Serial.println("Setting desired state for A/C.");
    mitsubir.on();
    mitsubir.setFan(1);
    mitsubir.setMode(MITSUBISHI_AC_COOL);
    mitsubir.setTemp(26);
    mitsubir.setVane(MITSUBISHI_AC_VANE_AUTO);
    g_state = STATE_IDLE;
    g_incomeCnt = 0;
}

void loop() {
    uint8_t val;
    // send data only when you receive data:
    if (Serial.available() > 0) {
        // read the incoming byte:
        incomingByte = Serial.read();
        switch(g_state){
            case STATE_IDLE:
                if(incomingByte == 'S'){
                    g_state = STATE_START;
                    Serial.println("STATE_START");
                    g_incomeCnt = 0;
                }
                break;
            case STATE_START:
                if(incomingByte != 'E'){
                    g_incomeBuff[g_incomeCnt] = incomingByte;
                    //Serial.printf("incomingByte: %d\n",incomingByte);
                    g_incomeCnt++;
                }else{
                    g_state = STATE_END;
                }
                break;
            case STATE_END:
                Serial.println("STATE_END");
                switch(g_incomeBuff[2]){
                    case 'N':
                        mitsubir.on();
                        mitsubir.send();
                        Serial.println("Send ON");
                        break;
                    case 'F':
                        mitsubir.off();
                        mitsubir.send();
                        Serial.println("Send OFF");
                        break;
                    case 'T': // check status
                        printState()
                        Serial.println("Check status");
                        break;
                    default:
                        switch(g_incomeBuff[1]){
                            case 'C':
                                Serial.println("Nhiet do");
                                val = atoi((const char*)&g_incomeBuff[2]);
                                Serial.printf("val: %d\n", val, DEC);
                                mitsubir.setTemp(val); // 16 - 31
                                mitsubir.send();
                                break;
                            case 'F':
                                Serial.println("Luong gio");
                                val = atoi((const char*)&g_incomeBuff[2]);
                                Serial.printf("val: %d\n", val, DEC);
                                mitsubir.setFan(val); // 0 - 6
                                mitsubir.send();
                                break;
                            case 'D':
                                Serial.println("Huong gio");
                                val = atoi((const char*)&g_incomeBuff[2]);
                                Serial.printf("val: %d\n", val, DEC);
                                mitsubir.setVane(val); // 0 - 7
                                mitsubir.send();
                                break;
                            default:
                                break;
                        }
                        break;
                }
                g_state = STATE_IDLE;
                memset(g_incomeBuff, 0, BUFF_SIZE);
                g_incomeCnt = 0;
                Serial.println("STATE_IDLE");
                break;
            default:
                break;
        }
    }
}

