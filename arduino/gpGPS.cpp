#ifndef gpGPS_h
#define gpGPS_h

#include "Arduino.h"
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include "gpRemindersStructs.cpp" /* Reminder structs, Reminder and Tijd */
#include "gpDebugger.cpp" /* Contains simple command to print to console to debug easily*/

#define RX_PIN 23
#define TX_PIN 18
#define BD_RATE 9600

class gpGPS
{
  public:
    void init()
    {
      ss.begin(BD_RATE, RX_PIN, TX_PIN); /* check if this is good */
    }
    void updateData()
    {
      
      currentTime_h = gps.time.hour() + 1; // hacky, but it works
      currentTime_m = gps.time.minute();
      currentTime_s = gps.time.second();
      currentLocation_lat = gps.location.lat();
      currentLocation_lat_str = String(gps.location.lat(),6);
      currentLocation_lng = gps.location.lng();
      currentLocation_lng_str = String(gps.location.lng(),6);
      
    }
    void feedGps()
    {
      while (ss.available() > 0)
      {
        char c = ss.read();
        gps.encode(c);
      }
    }
    

    int currentTime_h;
    int currentTime_m;
    int currentTime_s;
    float currentLocation_lat;
    float currentLocation_lng;
    String currentLocation_lat_str;
    String currentLocation_lng_str;
  private:
    SoftwareSerial ss;
    TinyGPSPlus gps;


};

#endif
