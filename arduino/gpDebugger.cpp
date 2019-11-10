#ifndef gpDebugger_h
#define gpDebugger_h

#include "Arduino.h"

class gpDebugger
{
  private:
    static const bool debugMode = false;

  public:
    static void serialPrint(String arg)
    {
      if (debugMode == true)
      {
        Serial.print(arg);
      }
    };

    static void serialPrint(int arg)
    {
      if (debugMode == true)
      {
        Serial.print(arg);
      }
    };

    static void serialPrintln(String arg)
    {
      if (debugMode == true)
      {
        Serial.println(arg);
      }
    };

    static void serialPrintln(int arg)
    {
      if (debugMode == true)
      {
        Serial.println(arg);
      }
    };

    static void serialPrintln()
    {
      Serial.println();
    }
};

#endif
