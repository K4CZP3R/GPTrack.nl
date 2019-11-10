#ifndef gpLCD_h
#define gpLCD_h

#include "Arduino.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "gpDebugger.cpp" /* Contains simple command to print to console to debug easily*/
#include "gpHelpers.cpp"

#define I2C_ADDR 0x27
#define XCHARS 16
#define XLINES 2

#define CLEAR_ON_PRINT true

class gpLCD
{
  public:
    gpLCD()
    {
      this->lcd = new LiquidCrystal_I2C(I2C_ADDR, XCHARS, XLINES);
    }
    void init()
    {
      lcd->begin(15, 13);
      lcd->backlight();
      lcd->print("Creating chars");
      lcd->createChar(0, char_clock);
      lcd->createChar(1, char_reminders);
      lcd->createChar(2, char_hr);
      delay(500);
      lcd->clear();
    }
    void dashboard_show(int n_reminders, int hr, String time_str) {
      /* reminders aantal: R4 */
      lcd->setCursor(1, 0);
      lcd->print(n_reminders);

      /* tijd */
      lcd->setCursor(11, 0);
      lcd->print(time_str);

      /* HR */
      lcd->setCursor(4, 0);
      lcd->print(hr);

    }
    void dashboard_show_message(String message)
    {
      clear(1);
      lcd->setCursor(0, 1);
      lcd->print(message);
    }
    void dashboard_show_template()
    {
      /* reminder icon */
      lcd->clear();
      lcd->setCursor(0, 0);
      lcd->write(1);

      /* hr icon */
      lcd->setCursor(3, 0);
      lcd->write(2);

      /* time icon */
      lcd->setCursor(10, 0);
      lcd->write(0);
    }


    void log_print(String content) {
      print(content, 0, get_log_pos());
    }
    void log_print(const char *content) {
      print(content, 0, get_log_pos());
    }
    void log_print(int content) {
      print(content, 0, get_log_pos());
    }

    void c_print(String content, int y)
    {
      int start_pos = GpHelpers.getCenterPos(content);
      print(content, start_pos, y);
    }
    void c_print( int content, int y)
    {
      int start_pos = GpHelpers.getCenterPos(content);
      print(content, start_pos, y);
    }
    void c_print(const char *content, int y)
    {
      int start_pos = GpHelpers.getCenterPos(content);
      print(content, start_pos, y);
    }

    void print(String content, int x, int y)
    {
      if (CLEAR_ON_PRINT) clear(y);

      lcd->setCursor(x, y);
      lcd->print(content);
    }
    void print( int content, int x, int y)
    {
      if (CLEAR_ON_PRINT) clear(y);
      lcd->setCursor(x, y);
      lcd->print(content);
    }
    void print( const char *content, int x, int y)
    {
      if (CLEAR_ON_PRINT) clear(y);

      lcd->setCursor(x, y);
      lcd->print(content);
    }
    void clear(int line)
    {
      lcd->setCursor(0, line);
      lcd->print("                "); //don't judge me
    }
    void backlight(bool state) {
      state == true ? lcd->backlight() : lcd->noBacklight();
    }


  private:
    int last_log_pos = 1;
    int get_log_pos() {
      last_log_pos = (last_log_pos == 0 ? 1 : 0);
      return last_log_pos;
    }
    byte char_clock[8] = {
      0x00,
      0x0E,
      0x15,
      0x15,
      0x13,
      0x11,
      0x0E,
      0x00
    };
    byte char_reminders[8] = {
      0x00,
      0x15,
      0x1F,
      0x11,
      0x11,
      0x11,
      0x1F,
      0x00
    };
    byte char_hr[8] = {
      0x00,
      0x0A,
      0x15,
      0x11,
      0x0A,
      0x04,
      0x00,
      0x00
    };
    LiquidCrystal_I2C *lcd;
    gpHelpers GpHelpers;


};

#endif
