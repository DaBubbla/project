import requests
import urllib.parse
import sqlite3
import json

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
    a = cur.execute("SELECT * FROM aapl ORDER BY date DESC LIMIT 0, 99")

    # Fetchall will grab all results of a query
    b = a.fetchall()
    b.reverse()
    c = []
    conn.close()


    for i in b:
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
    return c


def logic():
    # For analysis block#####
    days = 99
    pre = pyson()


    p = []

    Bear = 0
    Bull = 0
    CountDown = 0
    Reference = 0

    for i in range(days-1):

        p.append({
            'date': pre[i]['date'],
            'open': pre[i]['open'],
            'high': pre[i]['high'],
            'low':  pre[i]['low'],
            'close': pre[i]['close'],
            'signal': pre[i]['u_d']
        })


        if Bear or Bull:
            if Bear and p[i]['close'] < Reference:
                # Process a close in a Bear Signal Sequence
                CountDown = CountDown + 1

                if CountDown == 9:
                    low6 = p[i-3]['close']
                    low7 = p[i-2]['close']
                    low8 = p[i-1]['close']
                    low9 = p[i]['close']

                    if low6 < low7:
                        low1 = low6
                    else:
                        low1 = low7

                    if low8 < low9:
                        low2 = low8
                    else:
                        low2 = low9

                    if low1 > low2:
                        p[i]['signal'] = "BUY_PERF"
                    else:
                        p[i]['signal'] = "BUY_SIGNAL"
                    # Resets counters
                    CountDown = 0
                    Bull = 0
                    Bear = 0
                    Reference = 0
            else:
                # No continuing Bear continuation - check for Bull continuation
                if Bull and p[i]['close'] > Reference:
                    # Process a close in a Bull signal seq.
                    CountDown = CountDown + 1
                    if CountDown == 9:
                        low6 = pre[i-3]['close']
                        low7 = pre[i-2]['close']
                        low8 = pre[i-1]['close']
                        low9 = pre[i]['close']

                        if low6 > low7:
                            low1 = low6
                        else:
                            low1=low7

                        if low8 > low9:
                            low2 = low8
                        else:
                            low2 = low9

                        if low1 < low2:
                            # Perfect sell Signal
                            p[i]['signal'] = 'SELL_PERF'
                        else:
                            # Weak sell signal
                            p[i]['signal'] = 'SELL_SIGNAL'
                        # Reset counters
                        CountDown = 0
                        Bull = 0
                        Bear = 0
                        Reference = 0
                else:
                    # Process a BUST in Bull / Bear Signal sequence
                    CountDown = 0
                    Bull = 0
                    Bear = 0
                    p[i]['signal'] == 'BUST'
                    Reference = 0

        else:
            # Detect Start of sequential setup
            c4 = pre[i-1]['close']
            c1 = pre[i-3]['close']

            if i > 3 and c4 > c1 and p[i]['close'] < c1:
                p[i]['signal'] = 'BEAR'
                Bear = 1
                Reference = c4
                CountDown = CountDown + 1
            if i > 3 and c4 < c1 and p[i]['close'] > c1:
                p[i]['signal'] = "BULL"
                Bull = 1
                Reference = c4
                CountDown = CountDown + 1
    return(p)

def usd(value):
    """Format value as USD."""
    return f"${value:,.3f}"







# def lookup(symbol):
#     """Look up quote for symbol."""

#     # Contact API
#     try:
#         response = requests.get(f"https://api.iextrading.com/1.0/stock/{urllib.parse.quote_plus(symbol)}/chart/3m")
#         response.raise_for_status()
#     except requests.RequestException:
#         return None

#     # Parse response
#     try:
#         quote = response.json()
#         return [{
#             "date" : quote['date'],
#             "open" : float(quote['open']),
#             "high" : float(quote['high']),
#             "low"  : float(quote['low']),
#             "close": float(quote['close'])
#         }]
#     except (KeyError, TypeError, ValueError):
#         return None

#     print(quote)




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