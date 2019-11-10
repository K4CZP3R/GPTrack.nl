from flask import Blueprint, session, render_template, url_for, redirect, request
from flask_session import Session
import gpReturns
import gpDatabase
import gpDecorators
import gpEncryption
import gpSession


gpView_login_blueprint = Blueprint('gpView_login', __name__)
gpView_login_prefix = "/auth"

gpDb = gpDatabase.gpDatabase()

@gpView_login_blueprint.route(gpView_login_prefix)
@gpDecorators.needs_to_be_guest
def index():
    return redirect(url_for("gpView_login.login"))

@gpView_login_blueprint.route(gpView_login_prefix + "/register", methods=['GET', 'POST'])
@gpDecorators.needs_to_be_guest
def register():
    if request.method == 'GET':
        return render_template("auth/auth_register.html")
    user_password = request.form.get("passwordInput", None)
    user_email = request.form.get("emailInput", None)
    user_name = request.form.get("nameInput", None)

    if user_password is None \
        or user_email is None \
            or user_name is None:
        return gpReturns.return_message("Error", "Try again.", 3, url_for("gpView_login.register"))

    resp = gpDb.add_user(user_name, user_email, user_password)
    if resp[0] is not True:
        return gpReturns.return_message("Error", resp[1], 3, url_for("gpView_login.register"))

    return gpReturns.return_message("Ok!", "Account created!", 3, url_for("gpView_login.login"))


@gpView_login_blueprint.route(gpView_login_prefix + "/login", methods=['GET', 'POST'])
@gpDecorators.needs_to_be_guest
def login():
    if request.method == 'GET':
        return render_template("auth/auth_login.html", login_type = "Dashboard")

    user_password = request.form.get("passwordInput", None)
    user_email = request.form.get("emailInput", None)

    if user_password is None \
            or user_email is None:
        return gpReturns.return_message("Error", "Try again.", 3, url_for("gpView_login.login"))

    resp = gpDb.get_user(email=user_email)
    if resp[0] is not True:
        return gpReturns.return_message("Error", resp[1], 3, url_for("gpView_login.login"))

    user = resp[1]

    user_hash = user['hash']
    resp = gpEncryption.gpEncryption.verify_password(user_password, user_hash)
    if not resp:
        return gpReturns.return_message("Error", "Wrong email/password combination", 2, url_for("gpView_login.login"))

    userSession = gpSession.gpSession(session)
    userSession.login_user(user)
    userSession.update_ses(session)

    return gpReturns.return_message("Hello, {name}".format(name=user['name']), "You are logged in!", 2, url_for("gpView_dashboard.main"))


@gpView_login_blueprint.route(gpView_login_prefix + "/logout")
@gpDecorators.needs_to_be_user
def logout():
    userSession = gpSession.gpSession(session)
    userSession.logout_user()
    userSession.update_ses(session)
    return gpReturns.return_message("Logged out!", "Redirecting to login page", 1, url_for("gpView_login.login"))
