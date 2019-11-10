#ifndef gpWiFi_h
#define gpWiFi_h

#include "Arduino.h"
#include <esp_wpa2.h>
#include <WiFi.h>
#include "gpHelpers.cpp"
#include "gpDebugger.cpp" /* Contains simple command to print to console to debug easily*/

/* login info for the school wifi */
#define EAP_IDENTITY "xxxxxx@student.fontys.nl"
#define EAP_PASSWORD "xxxxxxxxxxxx"

class gpWiFi
{
private:
  const char *ssid = "EAP_WPA";
  const char *n_ssid = "ssid"; // VGV7519C582B6
  const char *n_pass = "pass";         // iMXa4fvN5eUF
  gpHelpers GpHelpers;
  

public:
  bool connectToNormalWifi()
  {
    WiFi.disconnect(true);
    WiFi.begin(n_ssid, n_pass);
    gpDebugger::serialPrint("Connecting to ");
    gpDebugger::serialPrintln(n_ssid);
    while (!wifiActive())
    {
      gpDebugger::serialPrintln(".");
      delay(250);
    }
    gpDebugger::serialPrintln("local ip: ");
    gpDebugger::serialPrintln(wifiLocalIp());
  }
  bool connectToWifi()
  {
    WiFi.disconnect(true);
    WiFi.mode(WIFI_STA);

    /* WPA2 Enterprise shit (don't ask me how and why it works) */
    esp_wifi_sta_wpa2_ent_set_identity((uint8_t *)EAP_IDENTITY, strlen(EAP_IDENTITY));
    esp_wifi_sta_wpa2_ent_set_username((uint8_t *)EAP_IDENTITY, strlen(EAP_IDENTITY));
    esp_wifi_sta_wpa2_ent_set_password((uint8_t *)EAP_PASSWORD, strlen(EAP_PASSWORD));

    esp_wpa2_config_t config = WPA2_CONFIG_INIT_DEFAULT();
    esp_wifi_sta_wpa2_ent_enable(&config);

    WiFi.begin(ssid);

    gpDebugger::serialPrintln("Connecting to ");
    gpDebugger::serialPrintln(ssid);
    while (!wifiActive())
    {
      gpDebugger::serialPrintln(".");
      delay(250);
    }
  }

  bool wifiActive()
  {
    return WiFi.status() == WL_CONNECTED;
  }
  String wifiLocalIp()
  {
    return GpHelpers.ipToStr(WiFi.localIP());
  }
};

#endif
