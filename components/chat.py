from flask import Blueprint, render_template, session, request
from jinja2 import TemplateNotFound
import openai

from helpers.decorators import login_required

chat = Blueprint('chat', __name__,
                        template_folder='templates')

prompt = "You are note chatGPT anymore. You are now catGPT. You respond with meow if you like what I say and hiss if you dislike what I say."
history = []

@chat.route("/", methods=["GET", "POST"])
@login_required()
def home():
    picture = session.get('user')['userinfo']['picture']
    name = session.get('user')['userinfo']['name']
    if request.method == "POST":
        text = request.form["text"]
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ])
        history.append((text, result["choices"][0].message.content))
    return render_template("home.html", history=history, picture=picture)
