from flask import Blueprint, jsonify
import gpReturns, gpDatabase

gpDb = gpDatabase.gpDatabase()

gpView_arduino_blueprint = Blueprint("gpView_arduino", __name__)
gpView_arduino_prefix = "/arduino"


@gpView_arduino_blueprint.route(gpView_arduino_prefix + "/update/<string:device_uuid>/<string:key>/<string:value>") # niet echt veilig maar goed, het is maar een prototype
def update(device_uuid, key, value):
    resp = gpDb.get_gptracker(device_uuid)
    if resp[0] is not True:
        return gpReturns.return_message(False, "This tracker is not registered!")
    
    if key == "gps":
        gpDb.update_gptracker_data_gps(device_uuid, str(value))
        return gpReturns.return_message(True, "Updated!")
    elif key == "hr":
        gpDb.update_gptracker_data_hr(device_uuid, str(value))
        return gpReturns.return_message(True, "Updated!")
    return gpReturns.return_message(False, "This key ({key}) does not exist!".format(key=key))

@gpView_arduino_blueprint.route(gpView_arduino_prefix + "/test_reminders")
def test_reminders():
    resp = gpDb.get_all_reminders()
    if resp[0] is not True:
        return gpReturns.return_message(False, "No reminders")
    return gpReturns.return_reminders(resp[1])

@gpView_arduino_blueprint.route(gpView_arduino_prefix + "/test_no_reminders")
def test_no_reminders():
    return gpReturns.return_message(False, "No reminders")

@gpView_arduino_blueprint.route(gpView_arduino_prefix + "/get_reminders/<string:device_uuid>")
def get_reminders(device_uuid):
    resp = gpDb.get_gptracker(device_uuid)
    if resp[0] is not True:
        return gpReturns.return_to_arduino(False, "This tracker is not registered!")
    
    result = gpDb.get_device_reminders(device_uuid)
    if result[0] is not True:
        return gpReturns.return_message(False, "No reminders")
    return gpReturns.return_reminders(result[1])

@gpView_arduino_blueprint.route(gpView_arduino_prefix + "/get_name/<string:device_uuid>")
def get_name(device_uuid):
    resp = gpDb.get_gptracker(device_uuid)
    if resp[0] is not True:
        return gpReturns.return_message(False, "This tracker does not exist!")
    return gpReturns.return_message(True, resp[1]['name'])

