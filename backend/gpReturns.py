from flask import jsonify


LVL_1_SEPARATOR = "`"
LVL_2_SEPARATOR = "|"
LVL_3_SEPARATOR = "~"
# possible responses to arduino
# Message: m`success|message_content
# Reminders: size ` reminder_content~reminder_time | reminder2_content~reminder2_time

def return_message(success:bool, message:str):
    response_template = f"m{LVL_1_SEPARATOR}{success}{LVL_2_SEPARATOR}{message}"
    return response_template

def return_reminders(reminders_list):
    response_template = f"{len(reminders_list)}{LVL_1_SEPARATOR}"
    for i in range(0, len(reminders_list)):
        reminder_template = f"{reminders_list[i]['content']}{LVL_3_SEPARATOR}{reminders_list[i]['time']}"
        if i != 0 and i != len(reminders_list):
            response_template += LVL_2_SEPARATOR
        response_template += reminder_template
    return response_template