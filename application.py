import os
import json
import requests
import sqlite3 # SQL might handle as well
import csv

from cs50 import SQL
from flask import Flask, flash, render_template, request, redirect, session, url_for # For UI / UX
from flask_session import Session # For UI / UX

from tempfile import mkdtemp
from helpers import login_required, lookup, apology, usd

from werkzeug.security import check_password_hash, generate_password_hash # For login info


# Configure application
app = Flask(__name__)

# Auto reload - unsure if necessary
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.route("/", methods=["GET", "POST"])
def index():
    # take csv as input
    try:
        conn = sqlite3.connect("project.db")
    except:
        return apology("Error with db connect")
    # Appoint cursor to exec queries against db
    cur = conn.cursor()
    # Fetch 1st 100 rows from watch table
    a = cur.execute("SELECT * FROM watch ORDER BY date DESC LIMIT 0, 99")

    # Fetchall will grab all results of a query
    b = a.fetchall()

    # print(type(b)) # Indicates list

    c = []
    for i in b:
        # print(i[0]) Got-eem!
        c.append({
            'date': i[0],
            'open': i[1],
            'close': i[4],
            'x': i[3]
            })
        # print(c) Successfully prints array of objects

    for w in range(len(c)):
        Open = c[w]['open'] # 0.5
        Close= c[w]['close']# 0.5
        u_d  = c[w]["x"]# 'down'
        if Open <= Close:
            c[w]['x']='upper'
        else:
            c[w]['x']='down'
        print(c[w])







    return render_template("watch.html")



    # x = {}
    #     # 'date': thingy[0],
    #     # 'open': thingy[1],
    #     # 'high': thingy[2],
    #     # 'low':  thingy[3],
    #     # 'close':thingy[4],
    #     # 'adj_close':thingy[5],
    #     # 'volume': thingy[6],
    #     # 'updown': thingy[7]

    # i=0
    # for i in range(len(thingy)):
    #     x.append(thingy[i])
    #     i = i + 1

    # print(x) #returns csv list





    # for row in rows:
    #     Open = db.execute("SELECT 'open' FROM watch")
    #     Close = db.execute("SELECT 'close' FROM watch")
    #     updown = db.execute("SELECT 'updown' FROM watch")

    #     if Open < Close:
    #         cur.executemany("UPDATE watch SET updown=0 WHERE rowid=?")
    #     else:
    #         cur.executemany("UPDATE 'watch' SET 'updown'=0 WHERE rowid=$rowid")






        # for col in rows:
        #     count = 0
        #     Open = col[1]
        #     High = col[2]
        #     Low = col[3]
        #     Close = col[4]
        #     updown = col[7]

        #     if col[1] <= col[4]:
        #       db.execute("UPDATE watch SET 'updown'=1 WHERE rowid=rows[i]")# UPPER
        #       countDown = countDown + 1


        #     else:
        #         db.execute("UPDATE watch SET 'updown'=0")# DOWNER
        #         countDown = 0

        #     count = count + 1

            # Stuff into database
            # col = db.execute("INSERT INTO table poopie (date, open, high, low, close, updown) VALUES ( date=col[0], open=col[1], high=col[2],low=col[3], close=col[4], updown=col[7] ", )




        # BullFlip = 0
        # BearFlip = 0
        # CountDown = 0
        # Reference = 0
        # Support = 0
        # min = 999.00
        # max = 0

    # if bearFlip or bullFlip:
    #     if bearFlip and close < reference:
    #         countDown = countDown + 1
    #         # Light up table slot to buy
    #         if countDown == 9:
    #             """change css to blinking buy"""
    #             # Reference table work
    #     else:
    #         if bullFlip and close > reference:
    #             countDown = countDown + 1
    #             # light up table slots to sell
    #             if countDown == 9:
    #                 """change css to blinking sell"""
    #                 # Reference table work
    # else:
    #     if i > 3 and :

