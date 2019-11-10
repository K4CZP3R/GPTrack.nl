from functools import wraps
from flask import g, request, redirect, url_for, session, render_template
from flask_session import Session
import gpReturns
import gpDatabase
import app_config
import gpSession

gpDb = gpDatabase.gpDatabase()


def valid_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        adminSession = gpSession.gpSession(session)

        if adminSession.admin_username is None \
                or adminSession.admin_password is None:
            return gpReturns.return_message("You don't have access to this page!", ":(", 3, url_for("gpView_admin.login"))

        if adminSession.admin_username != app_config.ADMIN_USERNAME \
                or adminSession.admin_password != app_config.ADMIN_PASSWORD:
            return gpReturns.return_message("You don't have access to this page (anymore)!", 2, url_for("gpView_admin.login"))
        return f(*args, **kwargs)
    return decorated_function


def admin_panel_enabled(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if app_config.ADMIN_PANEL_ENABLED:
            return f(*args, **kwargs)
        return gpReturns.return_message("Panel is disabled", "You can't use it!", 60, "")
    return decorated_function


def needs_to_have_registered_gptrack(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        userSession = gpSession.gpSession(session)
        if userSession.user is None:
            raise Exception("Logic error #1")

        user_uuid = userSession.user['uuid']
        trackers_list = gpDb.get_gptrackers(user_uuid)
        if trackers_list[0] is False:
            return gpReturns.return_message("You need to register an GPTracker", "Will redirect you to the GPTrack Register page", 2, url_for("gpView_track.user_assign"))
        return f(*args, **kwargs)
    return decorated_function


def needs_to_be_guest(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if gpSession.gpSession(session).logged_in is True:
            return gpReturns.return_message("You need to be logged out!", "Redirecting to dashboard", 2, url_for("gpView_dashboard.main"))
        return f(*args, **kwargs)

    return decorated_function


def needs_to_be_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        userSession = gpSession.gpSession(session)
        if userSession.logged_in is False or userSession.logged_in is None:
            userSession.logout_user()
            userSession.update_ses(session)
            return gpReturns.return_message("You need to be logged in!", "Redirecting to login page", 1, url_for("gpView_login.login"))

        if gpDb.get_user(uuid=userSession.user['uuid'])[0] is False:
            userSession.logout_user()
            userSession.update_ses(session)
            return gpReturns.return_message("Your account is no longer valid!", "Try to login again!", 1, url_for("gpView_login.login"))

        return f(*args, **kwargs)
    return decorated_function