# gpView_dashboard.py
# Web routes voor alles wat te maken heeft met dashboard
# o.a. reminders
from flask import Blueprint, session, render_template, url_for, redirect, request
from flask_session import Session

import gpReturns, gpDatabase, gpDecorators

gpView_dashboard_blueprint = Blueprint("gpView_dashboard", __name__)
gpView_dashboard_prefix = "/dashboard"

gpDb = gpDatabase.gpDatabase()


@gpView_dashboard_blueprint.route(gpView_dashboard_prefix + "/")
@gpDecorators.needs_to_be_user
@gpDecorators.needs_to_have_registered_gptrack
def main():
    gp_trackers = gpDb.get_gptrackers(session['user']['uuid'])
    if gp_trackers[0] is not True:
        return gpReturns.return_message("Error", "There are no GPTrackers assigned to your account!", 1, "gpView_track.assign_user")
    
    unified = gpDb.make_unified_gptracker_data(gp_trackers[1])
    return render_template("dashboard/dashboard.html", name=session['user']['name'], gp_trackers_unified=unified)


@gpView_dashboard_blueprint.route(gpView_dashboard_prefix + "/reminders/", methods=['GET', 'POST'])
@gpDecorators.needs_to_be_user
@gpDecorators.needs_to_have_registered_gptrack
def reminders():
    if request.method == 'GET':
        reminders = gpDb.get_reminders(uuid=session['user']['uuid'])
        paired_devices = gpDb.get_gptrackers(session['user']['uuid'])
        if paired_devices[0] is not True:
            return gpReturns.return_message("Something went wrong", "Assign GP tracker ofs", 1, url_for("gpView_dashboard.reminders"))
        if reminders[0] is not True:
            print("There are no reminders!")
            reminders[1] = []
            #return gpReturns.return_message("Something went wrong.", "Try again", 1, url_for("gpView_dashboard.reminders"))
        
        return render_template("dashboard/reminders.html", rem=reminders[1], paired_devices=paired_devices[1])
    
    reminder_content = request.form.get("contentInput", None)
    reminder_time = request.form.get("timeInput", None)
    reminder_creator_uuid = session['user']['uuid']
    reminder_device_uuid = request.form.get("deviceRadio", None)

    if reminder_time is None \
        or reminder_content is None \
            or reminder_device_uuid is None:
            return gpReturns.return_message("Error", "Try again.",1, url_for("gpView_dashboard.reminders"))
    
    resp = gpDb.create_reminder(reminder_content,reminder_time, reminder_creator_uuid, reminder_device_uuid)
    if resp[0] is not True:
        return gpReturns.return_message("Error", resp[1], 2, url_for("gpView_dashboard.main"))
    
    return gpReturns.return_message("Reminder added!", "Redirecting to reminders!", 1, url_for("gpView_dashboard.reminders"))


