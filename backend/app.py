from flask import Flask, jsonify, redirect
import app_config
from views.gpView_arduino import gpView_arduino_blueprint

app = Flask(__name__)
app.register_blueprint(gpView_arduino_blueprint)

@app.route("/")
def index():
    return redirect("/arduino/")

if __name__ == "__main__":
    app.run(
        host=app_config.HOST,
        port=app_config.PORT,
        ssl_context=app_config.SSL_CONTEXT,
        debug=app_config.DEBUG
    )