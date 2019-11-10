#ifndef gpDevice_h
#define gpDevice_h

#include "Arduino.h"
#include "gpDebugger.cpp" /* Contains simple command to print to console to debug easily*/

class gpDevice
{
public:
  void init()
  {
    pinMode(activity_led, OUTPUT);
    pinMode(wifi_led, OUTPUT);
  }

  void activity(bool state)
  {
    digitalWrite(activity_led, state);
  }
  void wifi(bool state)
  {
    digitalWrite(wifi_led, state);
  }
  void blink_wifi()
  {
    digitalWrite(wifi_led, HIGH);
    delay(100);
    digitalWrite(wifi_led, LOW);
  }
  void blink_activity()
  {
    digitalWrite(activity_led, HIGH);
    delay(100);
    digitalWrite(activity_led, LOW);
  }
  String getDeviceUUID()
  {
    return device_uuid;
  }
  String getDefaultDeviceName()
  {
    return device_name;
  }
  String getRemindersURL()
  {
    return server_url + String("arduino/get_reminders/") + device_uuid;
  }
  String getGPSUpdateURL()
  {
    return server_url + String("arduino/update/") + device_uuid + String("/gps/");
  }
  String getHRUpdateURL()
  {
    return server_url + String("arduino/update/") + device_uuid + String("/hr/");
  }

private:
  int activity_led = 14;
  int wifi_led = 27;
  String device_uuid = "12345";
  String device_name = "ESP32 Prototype";
  String server_url = "https://server.gptrack.nl/";
  String build_date = String(__DATE__) + "." + String(__TIME__);
  
};

#endif
