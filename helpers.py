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
    conn.close()


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

def logic():
    # For analysis block#####
    days = 50
    q = pyson()
    p = []
    for i in range(days):
        p.append(
            q[i]
            )
    #########################

    # Evaluate trends in data
    Min = 0
    Max = 9999.99
    BullFlip = 0
    BearFlip = 0
    CountDown = 0
    count = 0
    Reference = 0
    Support = 0

    switch = 1

    for i in range(len(p)):
        if switch == 0:
            if p[i]['low'] < Min:
                Min = p[i]['low']
            if p[i]['high'] > Max:
                Max = p[i]['high']
        else:
            # Initialize min, max, last close on 1st iteration
            Min = p[i]['low']
            Max = p[i]['high']
            Last = p[i]['close']
            switch = 0 # Turn this off for rest of loop
        # print(p[i])

    if BearFlip or BullFlip:
        if BearFlip and p[i]['close'] < Reference:
            CountDown = CountDown + 1
            if CountDown == 9:
                print("Buy", CountDown, p[i]['close'], Reference)
                # Reference
                low1 = p[i-8]['low']
                low2 = p[i-7]['low']
                low3 = p[i-6]['low']
                low4 = p[i-5]['low']
                low5 = p[i-4]['low']
                low6 = p[i-3]['low']
                low7 = p[i-2]['low']
                low8 = p[i-1]['low']
                low9 = p[i]
                if low6 < low7:
                    # discuss logic
                    low1 = low6
                else:
                    low1 = low7
                    ###############
                if low8 < low9:
                    # discuss logic
                    low2 = low8
                else:
                    low2 = low9
                    ###############
                if low1 > low2:
                    print('BuyPERF: ', CountDown, Reference, low1)
                    print(p[i]['date'],"Strong_Buy", p[i]['close'], Reference, low1)
                    # Strong_Buy
            else:
                print("BuySignal", CountDown, Reference, low1)
                print(p[i]['date'], "Buy", p[i]['close'], Reference, low1)
                # Strong_sell
            CountDown = 0
            BullFlip = 0
            BearFlip = 0
            Reference = 0
        else:
            if BullFlip and p[i]['close'] > Reference:
                print("Trace: ", CountDown, p[i]['close'], Reference)
                CountDown = CountDown + 1
                # TD-Sell CountDown Close Reference
                if CountDown == 9:
                    if low6 > low7:
                        low1 = low6
                    else:
                        low1 = low7
                    if low8 > low9:
                        low2 = low8
                    else:
                        low2 = low9
                    if low1 < low2:
                        print("SellPERF: ", CountDown, Reference, low1)
                        print(p[i]['date'], "Strong_sell", p[i]['close'], low1, Reference)
                    else:
                        print("SELLSignal", CountDown, low1, Reference)
                        print(p[i]['date'], "Sell", Reference, low1)

                    CountDown = 0
                    BullFlip = 0
                    BearFlip = 0
                    Reference = 0

            else:
                CountDown = 0
                BullFlip = 0
                BearFlip = 0
                Reference = 0
                print("Bust", p[i]['close'], Reference)
    else:
        # Reference
        c1 = p[i-3]['close']
        c4 = p[i-1]['close']

        if i > 3 and c4 > c1 and p[i]['close'] < c1:
            # BearFlip
            print("BearFlip: ", p[i]['date'], p[i]['close'], c1)
            indicatorBR = p[i]['date'], p[i]['close']
            BearFlip = 1
            Reference = c4
            CountDown = CountDown + 1
        if i > 3 and c4 < c1 and p[i]['close'] > c1:
            print("BullFlip", p[i]['date'], p[i]['close'], c1)
            indicatorBL = p[i]['date'], p[i]['close']
            BullFlip = 1
            Reference = c4
            CountDown = CountDown + 1

    # Change in open / close
    change_since_open = p[i]['open'] - p[i]['close']
    chance_since_close = p[i-1]['close'] - p[i]['open']
    # print(p[i])
    return(p)


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


