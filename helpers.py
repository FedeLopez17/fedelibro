import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def translateTemplate(template, username):
    language = db.execute("SELECT language FROM users WHERE username = ?", username)
    language = language[0]["language"]
    translated_template = template + "-" + language + ".html"
    return translated_template

def getUsername():
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = username[0]["username"]
    return username

def getUserId():
    user_id = session["user_id"]
    return user_id
