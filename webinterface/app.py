from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
import app_config, gpHelpers

from views.gpView_login import gpView_login_blueprint
from views.gpView_track import gpView_track_blueprint
from views.gpView_dashboard import gpView_dashboard_blueprint
from views.gpView_admin import gpView_admin_blueprint 


app = Flask(__name__)
app.register_blueprint(gpView_login_blueprint)
app.register_blueprint(gpView_dashboard_blueprint)
app.register_blueprint(gpView_track_blueprint)
app.register_blueprint(gpView_admin_blueprint)

SESSION_TYPE = app_config.SESSION_TYPE
app.config.from_object(__name__)
Session(app)


@app.route("/")
def index():
    return render_template("landing/landing_main.html")


@app.route("/map")
def map():
    links = gpHelpers.generate_map_view(app.url_map.iter_rules)
    return render_template("map.html", links=links)


if __name__ == "__main__":
    app.run(
        host=app_config.HOST,
        port=app_config.PORT,
        ssl_context=app_config.SSL_CONTEXT,
        debug=app_config.DEBUG
    )
