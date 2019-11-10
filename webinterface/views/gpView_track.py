from flask import Blueprint, request, render_template, url_for, session, redirect
import gpReturns
import gpDatabase
import gpDecorators
import gpSession

gpView_track_blueprint = Blueprint("gpView_track", __name__)
gpView_track_prefix = "/track"

gpDb = gpDatabase.gpDatabase()

@gpView_track_blueprint.route(gpView_track_prefix)
@gpDecorators.needs_to_be_user
@gpDecorators.needs_to_have_registered_gptrack
def index():
    return redirect(url_for("gpView_track.manage"))

@gpView_track_blueprint.route(gpView_track_prefix + "/api/get_data/<string:uuid>/<string:dtype>")
@gpDecorators.needs_to_be_user
@gpDecorators.needs_to_have_registered_gptrack
def api_get_data(uuid, dtype):
    
    gptracker_uuid = str(uuid)

    result = gpDb.get_gptracker_data(gptracker_uuid)
    if result[0] is not True:
        return gpReturns.return_api(False, error=result[1])
    return gpReturns.return_api(True, data=result[1][dtype])

@gpView_track_blueprint.route(gpView_track_prefix + "/api/get_data/<string:uuid>")
@gpDecorators.needs_to_be_user
@gpDecorators.needs_to_have_registered_gptrack
def api_get_data_all(uuid):
    result = gpDb.get_gptracker_data(uuid)
    if result[0] is not True:
        return gpReturns.return_api(False, error=result[1])
    return gpReturns.return_api(True, result[1])



@gpView_track_blueprint.route(gpView_track_prefix + "/manage/edit/<string:uuid>/<string:action>")
@gpDecorators.needs_to_be_user
@gpDecorators.needs_to_have_registered_gptrack
def manage_edit(uuid, action):
    gptracker_uuid = str(uuid)
    userSession = gpSession.gpSession(session)

    if userSession.user is None:
        raise Exception("Logic error #4")
    if action == 'unregister':
        result = gpDb.unregister_gptracker(gptracker_uuid)
        if result[0] is not True:
            return gpReturns.return_message("Error", result[1], 2, url_for("gpView_track.manage"))
        return gpReturns.return_message("Unregistered!", "Redirecting to manage page", 2, url_for("gpView_track.manage"))
    else:
        return gpReturns.return_message("Not implemented", "This function is not implemented!", 2, url_for("gpView_track.manage"))

@gpView_track_blueprint.route(gpView_track_prefix + "/manage", methods=['GET', 'POST'])
@gpDecorators.needs_to_be_user
@gpDecorators.needs_to_have_registered_gptrack
def manage():
    user = session.get("user", None)
    if user is None:
        raise Exception("Logic error #3")

    gp_trackers = gpDb.get_gptrackers(user['uuid'])
    
    if gp_trackers[0] is not True:
        return gpReturns.return_message("Error", "There are no gptrackers assigned!", 2, url_for("gpView_track.user_assign"))
    
    unified = gpDb.make_unified_gptracker_data(gp_trackers[1])
    return render_template("track/track_manage.html", gp_trackers_unified=unified, edit_url="/track/manage/edit")
    
@gpView_track_blueprint.route(gpView_track_prefix + "/user_assign", methods=['GET', 'POST'])
@gpDecorators.needs_to_be_user
def user_assign():
    user = session.get("user", None)
    if user is None:
        raise Exception("Logic error #2")

    if request.method == 'GET':
        assigned_devices = gpDb.get_gptrackers(user['uuid'])
        print(assigned_devices)
        return render_template("track/track_user_assign.html")

    gptrack_uuid = request.form.get("deviceUuidInput")
    gptrack_name = request.form.get("nameInput")

    if gptrack_uuid is None \
        or gptrack_name is None:
        return gpReturns.return_message("Error", "Try again!", 3, url_for("gpView_track.user_assign"))
    

    gptrack_owner_uuid = user['uuid']

    result = gpDb.register_gptracker(gptrack_uuid, gptrack_owner_uuid, gptrack_name)
    if result[0] is False:
        return gpReturns.return_message("Error", "{}".format(result[1]),2, url_for("gpView_track.manage"))
    
    return gpReturns.return_message("GPTracker assigned!", "Redirecting to your dashboard!", 1, url_for("gpView_dashboard.main"))
