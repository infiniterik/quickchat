from os import environ as env

from authlib.integrations.flask_client import OAuth

from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, url_for, flash

from components.authentication import create_auth_blueprint
from components.chat import chat

from helpers.decorators import login_required




ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

# initialize OAuth registry with this fetch_token function
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

app.register_blueprint(create_auth_blueprint(oauth))
app.register_blueprint(chat)

@app.route("/profile")
@login_required()
def profile():
    return "This should be secret"


@app.route("/not_logged_in")
def not_logged_in():
    flash("You are not logged in")
    return redirect(url_for("welcome"))

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000), debug=True)