#include "gpReminders.cpp"        /* Logic to convert https request to reminder struct */
#include "gpRemindersStructs.cpp" /* Reminder structs, Reminder and Tijd */
#include "gpHttp.cpp"             /* Contains functions to connect to the wifi/ make https requests */
#include "gpWiFi.cpp"             /* Contains functions to make connection with FontysWPA */
#include "gpBuzzer.cpp"           /* Contains function to make a sound */
#include "gpGPS.cpp"              /* Contains functions to get gps location */
#include "gpLCD.cpp"              /* Contains function to print to LCD */
#include "gpDevice.cpp"           /* Contains device UUID */
#include "gpDebugger.cpp"         /* Contains simple command to print to console to debug easily*/
#include "gpHelpers.cpp" /* String helpers */

/* Setting a maximum amount of reminders due to limited memory */
const int maxReminders = 32;
int last_reminder = 0;
gpRemindersStructs::Reminder reminders[maxReminders];

gpHttp GpHttp;
gpReminders GpReminders;
gpBuzzer GpBuzzer;
gpGPS GpGPS;
gpLCD GpLCD;
gpDevice GpDevice;
gpWiFi GpWiFi;
gpHelpers GpHelpers;


TaskHandle_t TaskGPS;


unsigned long mil_server_update = 0;
int server_update_every = 5000;

void setup()
{
  /* Enable/ disable for debug mode*/
  Serial.begin(115200);

  gpDebugger::serialPrintln("Init LCD");
  GpLCD.init();

  GpLCD.c_print("GPTrack.nl", 0);
  GpLCD.c_print("Loading...", 1);

  gpDebugger::serialPrintln("Device init!");
  GpDevice.init();
  GpDevice.activity(true);
  GpLCD.log_print("Device Init!");




  GpLCD.log_print("Connecting to wifi");
  GpDevice.wifi(true);
  /* Used to connect to our school wifi */
  GpWiFi.connectToWifi();
  /* Used to connect to a normal wpa2 network */
  //GpWiFi.connectToNormalWifi();
  GpLCD.log_print("Connected!");

  gpDebugger::serialPrintln("Local ip is: ");
  gpDebugger::serialPrintln(GpWiFi.wifiLocalIp());
  GpLCD.log_print("Local ip is:");
  GpLCD.log_print(GpWiFi.wifiLocalIp());
  GpDevice.wifi(false);

  gpDebugger::serialPrintln("Init buzzer");
  GpLCD.log_print("init buzzer");
  GpBuzzer.init();

  gpDebugger::serialPrintln("Init bpmmonitor");
  GpLCD.log_print("init bpmmon");
  gpBpmMonitor_init();


  GpLCD.log_print("xTaskCreate");
  GpLCD.log_print("TaskGPS on C0");
  xTaskCreatePinnedToCore(
    TaskGPScode,
    "TaskGPS",
    10000,
    NULL,
    0,
    &TaskGPS,
    0);


  GpLCD.dashboard_show_template();
}

void TaskGPScode(void *parameter)
{
  gpDebugger::serialPrintln("Init GPS");
  GpGPS.init();
  for (;;)
  {
    GpGPS.feedGps();
    GpGPS.updateData();
  }
}
bool beep_reminder = false;
void loop()
{
  unsigned long currentMillis = millis();

  gpDebugger::serialPrintln("==== Loop start ====");

  /* Get BPM from sensor */
  int bpm_value = gpBpmMonitor_getBpm();
  gpDebugger::serialPrint("= BPM: ");
  gpDebugger::serialPrintln(bpm_value);

  /* Get Current GPS location */
  gpDebugger::serialPrint("= GPS: ");
  String gps_location = String(GpGPS.currentLocation_lat_str) + "," + String(GpGPS.currentLocation_lng_str);
  gpDebugger::serialPrintln(gps_location);

  gpDebugger::serialPrint("Current seconde:");
  gpDebugger::serialPrintln(GpGPS.currentTime_s);




  /* Update reminders list */
  if (currentMillis - mil_server_update > server_update_every) {
    if (GpWiFi.wifiActive())
    {
      GpDevice.blink_wifi();
      if (bpm_value != -1)
      {
        GpHttp.makeGET(GpDevice.getHRUpdateURL() + String(bpm_value));
      }
      if (gps_location != "")
      {
        GpHttp.makeGET(GpDevice.getGPSUpdateURL() + gps_location);
      }
      String resp = GpHttp.makeGET(GpDevice.getRemindersURL());
      if (resp != "")
      {
        GpReminders.extractReminders(resp, reminders, &last_reminder);
      }
    }
    mil_server_update = currentMillis;
  }

   /*Print all the reminders*/
    gpDebugger::serialPrint("= Reminders: ");
    gpDebugger::serialPrintln(last_reminder);
    for (int i = 0; i < last_reminder; i++)
    {
    gpDebugger::serialPrintln("- reminder no.");
    gpDebugger::serialPrint(i);
    gpRemindersStructs::Reminder currentReminder = reminders[i];
    gpDebugger::serialPrintln(" content: '");
    gpDebugger::serialPrint(currentReminder.content);
    gpDebugger::serialPrint("'");
    gpDebugger::serialPrint(" time h=");
    gpDebugger::serialPrint(currentReminder.tijd.uur);
    gpDebugger::serialPrint(",m=");
    gpDebugger::serialPrint(currentReminder.tijd.minuut);
    gpDebugger::serialPrintln();
    }

  /* Get reminder to show
      There is only one reminder allowed per hour:minute combination
      Run buzzen en print to lcd
  */
  gpDebugger::serialPrintln("= getremindertoshow");

  gpDebugger::serialPrint("Creating current time:");
  gpRemindersStructs::Tijd currentTime = {GpGPS.currentTime_h, GpGPS.currentTime_m, GpGPS.currentTime_s};
  String reminderToExecute = GpReminders.getReminderToShow(reminders, currentTime);
  String timeStr = GpHelpers.getPrintableTime(currentTime, true);
  
  GpLCD.dashboard_show(last_reminder, bpm_value,  timeStr);
  if (!reminderToExecute.equals(""))
  {
    gpDebugger::serialPrintln("REMINDER NEEDS TO BE EXECUTED!");
    gpDebugger::serialPrintln(reminderToExecute);
    GpLCD.dashboard_show_message(String(reminderToExecute));
    if(!beep_reminder){
      GpBuzzer.buzzer();
      beep_reminder = true;
    }
  }
  else {
    beep_reminder = false;
    GpLCD.dashboard_show_message(String("Prototype ESP32"));
  }

  GpDevice.blink_activity();
  delay(1000);
}
