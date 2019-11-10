# gpView_admin.py
# Web routes voor admin panel

from flask import Blueprint, session, render_template, url_for, redirect, request
from flask_session import Session
import gpReturns, gpDatabase, gpDecorators, app_config, gpHelpers, gpSession


gpView_admin_blueprint = Blueprint("gpView_admin", __name__)
gpView_admin_prefix = "/admin"

gpDb = gpDatabase.gpDatabase()


@gpView_admin_blueprint.route(gpView_admin_prefix)
@gpDecorators.admin_panel_enabled
@gpDecorators.valid_admin
def main():
    return render_template("admin/admin_main.html")

###############################
#
# Users routes
#
###############################

@gpView_admin_blueprint.route(gpView_admin_prefix + "/users")
@gpDecorators.admin_panel_enabled
@gpDecorators.valid_admin
def users():
    all_users = gpDb.admin_get_all_users()
    if all_users[0] is not True:
        all_users[1] = []
    unified = gpDb.make_unified_user_gptrackers_list(all_users[1])
    return render_template("admin/users/admin_users.html", unified=unified)

@gpView_admin_blueprint.route(gpView_admin_prefix + "/users/delete/<string:uuid>")
@gpDecorators.admin_panel_enabled
@gpDecorators.valid_admin
def users_delete(uuid):
    resp = gpDb.remove_user(uuid)
    return gpReturns.return_message(resp[0], resp[1], 2, url_for("gpView_admin.users"))

@gpView_admin_blueprint.route(gpView_admin_prefix + "/users/edit/<string:uuid>")
@gpDecorators.admin_panel_enabled
@gpDecorators.valid_admin
def users_edit(uuid):
    user = gpDb.get_user(uuid=uuid)
    if user[0] is not True:
        return gpReturns.return_message("Error", user[1], 2, url_for("gpView_admin.users"))
    
    user = user[1]
    return render_template("admin/users/admin_users_edit.html", user=user)

@gpView_admin_blueprint.route(gpView_admin_prefix + "/users/edit/<string:uuid>/update", methods=['POST'])
@gpDecorators.admin_panel_enabled
@gpDecorators.valid_admin
def users_edit_update(uuid):
    user_uuid = str(uuid)
    user_name = request.form.get("nameInput", None)
    user_email = request.form.get("emailInput", None)

    if user_name is None \
        or user_email is None:
        return gpReturns.return_message("Error", "Try again", 2, url_for("gpView_admin.users"))
    
    resp = gpDb.update_user(user_uuid, user_name, user_email)
    return gpReturns.return_message(resp[0], resp[1], 2, url_for("gpView_admin.users"))

###############################
#
# Tracker routes
#
###############################

@gpView_admin_blueprint.route(gpView_admin_prefix + "/trackers")
@gpDecorators.admin_panel_enabled
@gpDecorators.valid_admin
def trackers():
    all_trackers = gpDb.admin_get_all_trackers()
    if all_trackers[0] is not True:
        all_trackers[1] = []
    return render_template("admin/trackers/admin_trackers.html", trackers=all_trackers[1])

@gpView_admin_blueprint.route(gpView_admin_prefix + "/trackers/add", methods=['POST'])
@gpDecorators.admin_panel_enabled
@gpDecorators.valid_admin
def trackers_add():
    gptracker_uuid = request.form.get("uuidInput", None)
    gptracker_name = request.form.get("nameInput", None)
    gptracker_owner_uuid = request.form.get("ownerUuidInput", None)

    if gptracker_name is None \
        or gptracker_uuid is None \
            or gptracker_owner_uuid is None:
            return gpReturns.return_message("Error", "Try again", 2, url_for("gpView_admin.trackers"))
    
    resp = gpDb.create_gptrack(gptracker_uuid, gptracker_name, gptracker_owner_uuid)
    return gpReturns.return_message(resp[0], resp[1], 3, url_for("gpView_admin.trackers"))

@gpView_admin_blueprint.route(gpView_admin_prefix + "/trackers/delete/<string:uuid>", methods=['GET'])
@gpDecorators.admin_panel_enabled
@gpDecorators.valid_admin
def trackers_delete(uuid):
    resp = gpDb.remove_gptrack(uuid)
    return gpReturns.return_message(resp[0], resp[1], 2, url_for("gpView_admin.trackers"))


@gpView_admin_blueprint.route(gpView_admin_prefix + "/trackers/edit/<string:uuid>", methods=['GET'])
@gpDecorators.admin_panel_enabled
@gpDecorators.valid_admin
def trackers_edit(uuid):
    tracker = gpDb.get_gptracker(uuid)
    tracker_data = gpDb.get_gptracker_data(uuid)
    if tracker[0] is not True:
        return gpReturns.return_message("Error", tracker[1], 2, url_for("gpView_admin.trackers"))
    if tracker_data[0] is not True:
        tracker_data[1] = {"gps": None, "hr": None}
    
    tracker = tracker[1]
    tracker_data = tracker_data[1]
    return render_template("admin/trackers/admin_trackers_edit.html",
     tracker=tracker, tracker_data=tracker_data)

@gpView_admin_blueprint.route(gpView_admin_prefix + "/trackers/edit/<string:uuid>/update_gps", methods=['POST'])
@gpView_admin_blueprint.route(gpView_admin_prefix + "/trackers/edit/<string:uuid>/update_hr", methods=['POST'])
@gpDecorators.admin_panel_enabled
@gpDecorators.valid_admin
def trackers_edit_update_gps(uuid):
    print(request.url_rule.rule)
    gptracker_uuid = str(uuid)
    
    if "update_gps" in request.url_rule.rule:
        gptracker_data = request.form.get("gpsInput", None)
    else:
        gptracker_data = request.form.get("hrInput", None)
    

    if gptracker_data is None:
        return gpReturns.return_message("Error", "Try again", 2, url_for("gpView_admin.trackers"))
    
    if "update_gps" in request.url_rule.rule:
        result = gpDb.update_gptracker_data_gps(gptracker_uuid,gptracker_data)
    else:
        result = gpDb.update_gptracker_data_hr(gptracker_uuid, gptracker_data)
    return gpReturns.return_message(result[0], result[1], 2, url_for("gpView_admin.trackers"))

    
    

@gpView_admin_blueprint.route(gpView_admin_prefix + "/trackers/edit/<string:uuid>/update", methods=['POST'])
@gpDecorators.admin_panel_enabled
@gpDecorators.valid_admin
def trackers_edit_update(uuid):
    gptracker_uuid = str(uuid)
    gptracker_name = request.form.get("nameInput", None)
    gptracker_owner_uuid = request.form.get("ownerUuidInput", None)

    if gptracker_name is None \
        or gptracker_owner_uuid is None:
        return gpReturns.return_message("Error", "Try again", 2, url_for("gpView_admin.trackers"))
    

    result = gpDb.update_gptracker(gptracker_uuid, gptracker_name,gptracker_owner_uuid)
    return gpReturns.return_message(result[0], result[1], 2, url_for("gpView_admin.trackers"))


###############################
#
# Auth routes
#
###############################

@gpView_admin_blueprint.route(gpView_admin_prefix+"/login", methods=['POST', 'GET'])
@gpDecorators.admin_panel_enabled
def login():
    if request.method == 'GET':
        return render_template("auth/auth_login.html", login_type = "ADMIN")
    admin_password = request.form.get("passwordInput", None)
    admin_email = request.form.get("emailInput", None)

    if admin_email is None \
        or admin_password is None:
        return gpReturns.return_message("Error", "Try again", 1,"")
    
    if admin_email == app_config.ADMIN_USERNAME:
        if admin_password == app_config.ADMIN_PASSWORD:
            adminSession = gpSession.gpSession(session)
            adminSession.login_admin(admin_email, admin_password)
            adminSession.update_ses(session)
            return gpReturns.return_message("Logged in!", "Haii admin :3",2, url_for("gpView_admin.main"))
    return gpReturns.return_message("Failed!", "Try again :p", 1, "")

@gpView_admin_blueprint.route(gpView_admin_prefix+"/logout", methods=['GET'])
@gpDecorators.admin_panel_enabled
@gpDecorators.valid_admin
def logout():
    userSession = gpSession.gpSession(session)
    userSession.logout_admin()
    userSession.update_ses(session)

    return gpReturns.return_message("Logged out!", "", 1, url_for("gpView_admin.main"))

@gpView_admin_blueprint.route(gpView_admin_prefix + "/wipe_this_shit")
@gpDecorators.admin_panel_enabled
@gpDecorators.valid_admin
def wipe_this_shit():
    gpDb.drop_all_dbs()
    return gpReturns.return_message("Database is wiped!", "You can start from scratch!", 2, url_for("map"))