#ifndef gpReminders_h
#define gpReminders_h

#include "Arduino.h"
#include "gpHelpers.cpp"
#include "gpRemindersStructs.cpp"
#include "gpDebugger.cpp" /* Contains simple command to print to console to debug easily*/

class gpReminders
{
public:
  String getReminderToShow(gpRemindersStructs::Reminder reminders[], gpRemindersStructs::Tijd currentTime)
  {
    gpDebugger::serialPrintln("== getReminderToShow");
    gpDebugger::serialPrint("= Current time (h): ");
    gpDebugger::serialPrintln(currentTime.uur);
    gpDebugger::serialPrint("= Current time (m): ");
    gpDebugger::serialPrintln(currentTime.minuut);

    gpDebugger::serialPrintln("Will iterate through every reminder, to check if there is one to show at current time!");
    for (int i = 0; i < 32; i++)
    {
      gpRemindersStructs::Reminder reminder = reminders[i];
      if (reminder.tijd.uur == currentTime.uur && reminder.tijd.minuut == currentTime.minuut)
      {
        gpDebugger::serialPrint("= Reminder no.");
        gpDebugger::serialPrintln(i);
        gpDebugger::serialPrintln("This reminder needs to be executed now!");
        gpDebugger::serialPrintln(reminder.tijd.uur);
        gpDebugger::serialPrint(currentTime.uur);
        return reminder.content;
      }
    }
    return ""; //there is no reminder to execute right now!
  }
  void extractReminders(String input_data, gpRemindersStructs::Reminder reminders[], int *last_reminder)
  {
    int data_reminderCount = GpHelpers.splitString(input_data, '`', 0).toInt();
    *last_reminder = data_reminderCount;
    String data_reminderData = GpHelpers.splitString(input_data, '`', 1);

    gpDebugger::serialPrintln("Reminders size: ");
    gpDebugger::serialPrint(data_reminderCount);

    gpDebugger::serialPrintln("Reminders content: ");
    gpDebugger::serialPrint(data_reminderData);

    for (int i = 0; i < data_reminderCount; i++)
    {
      String reminderStr = GpHelpers.splitString(data_reminderData, '|', i);

      String reminder_content = GpHelpers.splitString(reminderStr, '~', 0);
      String reminder_time = GpHelpers.splitString(reminderStr, '~', 1);

      int reminder_time_h = GpHelpers.splitString(reminder_time, ':', 0).toInt();
      int reminder_time_m = GpHelpers.splitString(reminder_time, ':', 1).toInt();

      gpRemindersStructs::Tijd struct_reminder_tijd{reminder_time_h, reminder_time_m};
      gpRemindersStructs::Reminder struct_reminder{reminder_content, struct_reminder_tijd};

      reminders[i] = struct_reminder;
    }
  }

private:
  gpHelpers GpHelpers;
  
};

#endif
