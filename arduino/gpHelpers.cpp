#ifndef gpHelpers_h
#define gpHelpers_h

#include "Arduino.h"
#include "gpRemindersStructs.cpp"


class gpHelpers
{
  public:
    String getPrintableTime(gpRemindersStructs::Tijd tijd, bool addSeconds)
    {
      String hours = String(tijd.uur);
      if(tijd.uur < 10) hours = "0" + hours;

      String minutes = String(tijd.minuut);
      if(tijd.minuut < 10) minutes = "0" + minutes;

      String seconds = String(tijd.seconde);
      if(tijd.seconde < 10) seconds = "0" + seconds;

      String timeStr = hours + ":" + minutes;
      if(addSeconds) timeStr = timeStr + ":" + seconds;

      return timeStr;
    }
    int getCenterPos(int input)
    {
      int pos = (16 - String(input).length()) / 2;
      return pos;
    }
    int getCenterPos(String input)
    {
      int pos = (16 - input.length()) / 2;
      return pos;
    }
    int getCenterPos(const char *input)
    {
      int pos = (16 - String(input).length()) / 2;
      return pos;
    }
    String splitString(String data, char separator, int index)
    {
      int found = 0;
      int strIndex[] = {0, -1};
      int maxIndex = data.length() - 1;

      for (int i = 0; i <= maxIndex && found <= index; i++)
      {
        if (data.charAt(i) == separator || i == maxIndex)
        {
          found++;
          strIndex[0] = strIndex[1] + 1;
          strIndex[1] = (i == maxIndex) ? i + 1 : i;
        }
      }

      return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
    }
    String ipToStr(IPAddress ip)
    {
      String s = "";
      for (int i = 0; i < 4; i++)
      {
        s += i ? "." + String(ip[i]) : String(ip[i]);
      }
      return s;
    }

};

#endif
