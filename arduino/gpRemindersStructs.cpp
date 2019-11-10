#ifndef gpRemindersStructs_h
#define gpRemindersStructs_h

#include "Arduino.h"

class gpRemindersStructs
{
public:
  struct Tijd
  {
    int uur;
    int minuut;
    int seconde;
  };

  struct Reminder
  {
    String content;
    Tijd tijd;
  };
};

#endif
