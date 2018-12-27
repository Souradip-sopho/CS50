import requests
import urllib.parse
import libgenapi

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

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(params,criteria):
    """Look up book."""

    # Contact API
    lg=libgenapi.Libgenapi(["http://libgen.io","http://libgen.pw","http://library1.org","http://booksdescr.org","http://gen.lib.rus.ec"])
    if criteria =="title":
        res = lg.libgen.search(params)
    else:
        res = lg.libgen.search(params,"author")
    return res
    # try:
    #     response = requests.get("https://api.iextrading.com/1.0/stock/{urllib.parse.quote_plus(symbol)}/quote")
    #     response.raise_for_status()
    # except requests.RequestException:
    #     return None

    # # Parse response
    # try:
    #     quote = response.json()
    #     return {
    #         "name": quote["companyName"],
    #         "price": float(quote["latestPrice"]),
    #         "symbol": quote["symbol"]
    #     }
    # except (KeyError, TypeError, ValueError):
    #     return None
