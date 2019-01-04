import requests
import urllib.parse
import sqlite3

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

def pyson():
    """Convert SQLite data to mutable data"""
    # Take data in reverse order + sectioned (100 days)
    try:
        conn = sqlite3.connect("project.db")
    except:
        print("Error with db connect")
        return None
    # Appoint cursor to exec queries against db
    cur = conn.cursor()
    # Fetch 1st 100 rows from watch table
    a = cur.execute("SELECT * FROM watch ORDER BY date DESC LIMIT 0, 99")

    # Fetchall will grab all results of a query
    b = a.fetchall()
    c = []


    for i in b:
        # print(i[0]) Got-eem!
        c.append({
            'date': i[0],
            'open': i[1],
            'high': i[2],
            'low' : i[3],
            'close': i[4],
            'u_d': i[7]
            })
    # Indicates if day trend is going up or down
    for i in range(len(c)):
        Open = c[i]['open'] # 0.5
        High = c[i]['high']
        Low = c[i]['low']
        Close= c[i]['close']# 0.5
        u_d  = c[i]["u_d"]# 'down'
        if Open <= Close:
            c[i]['u_d']='upper'
        else:
            c[i]['u_d']='down'
        # print(c)
    return c

# def login_required(f):
#     """
#     Decorate routes to require login.

#     http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
#     """
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if session.get("user_id") is None:
#             return redirect("/login")
#         return f(*args, **kwargs)
#     return decorated_function


# def lookup(symbol):
#     """Look up quote for symbol."""

#     # Contact API
#     try:
#         response = requests.get(f"https://api.iextrading.com/1.0/stock/{urllib.parse.quote_plus(symbol)}/quote")
#         response.raise_for_status()
#     except requests.RequestException:
#         return None

#     # Parse response
#     try:
#         quote = response.json()
#         return {
#             "name": quote["companyName"],
#             "price": float(quote["latestPrice"]),
#             "symbol": quote["symbol"]
#         }
#     except (KeyError, TypeError, ValueError):
#         return None



def usd(value):
    """Format value as USD."""
    return f"${value:,.3f}"


