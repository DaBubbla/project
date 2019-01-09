import os
import json
import requests
import csv
import sqlite3

from cs50 import SQL
from flask import Flask, flash, render_template, request, session, url_for
from flask_session import Session

from tempfile import mkdtemp
from helpers import apology, logic, pyson, usd# login_required, lookup, # Necessary for later application



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


        # Returns 50 days worth of stock data
        # analysis returns Bull / Bear flip
        # logic()
        rows = logic()
        # print(rows)




        return render_template("watch.html", rows=rows)
