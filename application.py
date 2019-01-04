import os
import json
import requests
# import csv

from cs50 import SQL
from flask import Flask, flash, render_template, request, session, url_for
from flask_session import Session

from tempfile import mkdtemp
from helpers import apology, pyson, usd# login_required, lookup, # Necessary for later application



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
    if request.method == "GET":

        # pyson()  Gives PYSON data.

        q = pyson()
        p = []
        # For analysis block#####
        days = 9
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
            print(p[i])

        if BearFlip or BullFlip:
            if BearFlip and p[i]['close'] < Reference:
                CountDown = CountDown + 1
                if CountDown == 9:
                    """BuySignal"""
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
                        print('Doing things here')
                        # Strong_sell
                else:
                    print("Or doing stuff there")
                    # Strong_sell
                CountDown = 0
                BullFlip = 0
                BearFlip = 0
                Reference = 0
            else:
                CountDown = 0
                BullFlip = 0
                BearFlip = 0
                print("BUST")
                Reference = 0
        else:
            # Reference
            c1 = p[i-4]['close']
            c4 = p[i-1]['close']

            if i > 3 and c4 > c1 and p[i]['close'] < c1:
                # BearFlip
                print("BearFlip: ", p[i]['close'])
                BearFlip=1
                Reference = c4
                CountDown = CountDown + 1

            print('oh lawdie me, this a long if')

        return render_template("watch.html")


        # trend = []

        # for i in range(len(p)):
        #     # ID a trend
        #     if p[i]['u_d'] == "upper" and count <= 9:
        #         trend = []
        #         trend.append({
        #             'date': p[i]['date'],
        #             'open': p[i]['open'],
        #             'high': p[i],
        #             'low' : p[i],
        #             'close': p[i],
        #             'u_d': p[i]
        #         })
        #         count = count + 1

        #     elif p[i]['u_d'] == "downer" and count <= 9:
        #         trend = []
        #         trend.append({
        #             'date': i[0],
        #             'open': i[1],
        #             'high': i[2],
        #             'low' : i[3],
        #             'close': i[4],
        #             'u_d': i[7]
        #         })
        #         count = count + 1
        #     else:
        #         count = 0
        #         trend = []
        #     print(trend)


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

