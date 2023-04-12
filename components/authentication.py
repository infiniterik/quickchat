from flask import Blueprint
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from authlib.oauth2.rfc6750 import BearerTokenValidator

from flask import redirect, session, url_for

def create_auth_blueprint(oauth):
    auth = Blueprint('auth', __name__, template_folder='templates')

    @auth.route('/login')
    def login():
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("auth.callback", _external=True)
        )

    @auth.route('/callback', methods=["GET", "POST"])
    def callback():
        token = oauth.auth0.authorize_access_token()
        session["user"] = token
        return redirect(url_for("chat.home"))

    @auth.route('/logout')
    def logout():
        session.clear()
        return redirect(
            "https://" + env.get("AUTH0_DOMAIN")
            + "/v2/logout?"
            + urlencode(
                {
                    "returnTo": url_for("welcome", _external=True),
                    "client_id": env.get("AUTH0_CLIENT_ID"),
                },
                quote_via=quote_plus,
            )
        )
    return auth