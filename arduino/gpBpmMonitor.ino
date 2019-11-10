/* 
  The libary doesn't work currently because it depends on 'arduino intterupts' which isn't supported by esp32
*/

#define USE_ARDUINO_INTERRUPTS false
#include <PulseSensorPlayground.h>
#include "gpDebugger.cpp" /* Contains simple command to print to console to debug easily*/


const int pulseWire = 32;
const int led_13 = 13;
int threshold = 680;

PulseSensorPlayground pulseSensor;

void gpBpmMonitor_init()
{
  pinMode(pulseWire, INPUT);
  pulseSensor.analogInput(pulseWire);
  pulseSensor.setThreshold(threshold);

  if (pulseSensor.begin())
  {
    gpDebugger::serialPrintln("PulseSensor created!");
  }
}

int gpBpmMonitor_getBpm()
{
  int myBPM;

  /* Because the library doesn't work we were forced to generate a random number */
  myBPM = random(70, 90);

  return myBPM;
}
