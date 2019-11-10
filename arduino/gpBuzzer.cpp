#ifndef gpBuzzer_h
#define gpBuzzer_h

#include "Arduino.h"
#include "gpDebugger.cpp" /* Contains simple command to print to console to debug easily*/

#define BUZZER_PIN 17

class gpBuzzer
{
public:
  void init()
  {
    pinMode(BUZZER_PIN, OUTPUT);
  }
  void buzzer()
  {
    const int toon = 800;
    const int dur = 1000;
    const int del = 250;

    tone(BUZZER_PIN, toon, dur);
    delay(del);
    tone(BUZZER_PIN, toon, dur);
    delay(del);
  }

private:
  /* ESP32 does not have built-in tone() and noTone() function, so we need to implement it */
  void tone(uint8_t pin, unsigned int freq, unsigned long duration)
  {
    ledcAttachPin(pin, 0);
    ledcWriteTone(0, freq);
    if (duration)
    {
      delay(duration);
      noTone(pin);
    }
  }
  void noTone(uint8_t pin)
  {
    ledcDetachPin(pin);
    ledcWrite(0, 0);
  }
};

#endif
