import os

from cs50 import SQL # To handle the database - hopefully its large enough
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


@app.route("/")
@login_required
def index():
    """Show dashboard"""
    # Current user
    users = db.execute("SELECT cash FROM users WHERE user_id = :user_id", user_id=session["user_id"])
    stocks = db.execute("SELECT symbol, name, SUM(shares) as total_shares FROM portfolio WHERE user_id=:user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])

    quotes = {}

    for stock in stocks:
        quotes[stock["symbol"]] = lookup( stock["symbol"] )

    cash_remaining = users[0]["cash"]
    total = cash_remaining

    return render_template("index.html", quotes=quotes, stocks=stocks, total=total, cash_remaining=cash_remaining)

@app.route('/login', methods=["POST", "GET"])
def login():
    """Login user"""

    # Forget all other users
    session.clear()

    if request.method == "POST":
        # Username submitted?
        if not request.form.get("username"):
            flash("Invalid username")

        # Password submitted?
        elif not request.form.get("password"):
            flash("Invalid password")

        # Select user in db
        crntUser = db.execute("SELECT * FROM users WHERE username=:username", username=request.form.get("username"))

        if len(crntUser) != 1 or not check_password_hash(crntUser[0]["hash"], request.form.get("password")):
            return flash("Invalid username and/or password")

        # Remember user
        session["user_id"] = crntUser[0]["user_id"]

        # Return home after login
        return redirect(url_for("index"))

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log out user"""
    # Forget user_id
    session.clear()

    # Return to login form
    return redirect('/')

@app.route("/register", methods=["GET", "POST"])
def register():
    """Registers new users into db"""
    if request.method == "POST":
        # username submitted?
        if not request.form.get("username"):
            flash("Provide a valid username")

        # Password submitted?
        elif not request.form.get("password"):
            flash("Provide a valid password")

        # Confirmation submitted?
        elif not request.form.get("confirmation"):
            flash("Provide password confirmation")

        # Passwords match?
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords don't match!")

        res = db.execute("INSERT INTO users (username, hash)\
                                      VALUES (:username, :hash)",\
                        username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))
        if not res:
            flash("Username already exists")

        # Remember which user has logged in
        session["user_id"] = res

        # Redirect user home after register
        return redirect(url_for("index"))

    else:
        return render_template("register.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get a stock quote"""
    if request.method == "POST":
        # Wait for user to fill out form
        rowData = lookup(request.form.get("symbol"))
        if not rowData:
            return apology("Invalid symbol")
        else:
            return render_template("quoted.html", stock=rowData)
    else:
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy stocks"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        quote = lookup(request.form.get("symbol"))
        if not quote:
            flash("Invalid symbol!")

        try:
            shares = int(request.form.get("shares"))
        except:
            flash("Shares must be a positive number")
        # Did the user request 0 shares?
        if shares <= 0:
            flash("Cant buy less that or 0 shares")

        # Select user
        userCash = db.execute("SELECT cash FROM users WHERE user_id=:user_id", user_id=session["user_id"])

        # Isolate cash
        cash_remaining = userCash[0]["cash"]
        per_share = quote["price"]

        # Calculate price of requested shares
        total_price = per_share * shares

        if total_price > cash_remaining:
            return apology("insufficient funds! :( ")

        # Updates and portfolio
        db.execute("UPDATE users SET cash = cash - :price WHERE user_id = :user_id", price = total_price, user_id=session["user_id"])
        db.execute("INSERT INTO portfolio (user_id, symbol, name, shares, per_share) VALUES(:user_id, :symbol, :name, :shares, :price)", \
                        user_id=session["user_id"], symbol=quote["symbol"], name=quote['name'], shares=int(request.form.get("shares")), price=per_share )

        flash("Ka-Ching! Transaction complete!")
        return redirect(url_for("index"))

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock --- TODO """
    if request.method == "POST":

        symbol = lookup(request.form.get("symbol"))

        # ensure proper symbol
        if not symbol:
                return apology("Invalid Symbol", 400)

        # Positive number of shares?
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Shares must be a positive number!", 400)

        # Does the user have enough shares?
        stock = db.execute("SELECT SUM(shares) as total_shares FROM portfolio WHERE user_id = :user_id and symbol = :symbol GROUP BY symbol",\
                            user_id = session["user_id"], symbol = request.form.get("symbol"))

        # Shares must be more than 0
        if shares <= 0:
            return apology("0 is not a valid number of shares!", 400)


        # Select the user's cash
        rows = db.execute("SELECT cash FROM users WHERE user_id = :user_id", user_id = session["user_id"])

        # Calculate user's cash
        remaining = rows[0]["cash"]
        per_share = symbol["price"]

        total_price = per_share * shares



        # Updates for sale
        db.execute("UPDATE users SET cash = cash + :price WHERE user_id=:user_id", price = total_price, user_id = session["user_id"])
        db.execute("INSERT INTO portfolio (user_id, symbol, name, shares, per_share) \
                    VALUES (:user_id, :symbol, :name, :shares, :price)",\
                    user_id = session["user_id"], symbol = request.form.get("symbol"), name=symbol["name"], shares=-shares, price= per_share )

        # Update user shares
        user_shares = db.execute("SELECT shares FROM portfolio WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=symbol["symbol"] )#monitor

        if not user_shares or int(user_shares[0]["shares"]) < shares:
            return apology("Not enough shares")



        flash("Sold!")

        return redirect(url_for("index"))

    else:
        stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM portfolio WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id = session["user_id"])

        return render_template("sell.html", stocks=stocks)












    # if request.method == "POST":

    #     stock = lookup(request.form.get("symbol"))

    #     # ensure proper symbol
    #     if not stock:
    #             return apology("Invalid Symbol")

    #     # Proper number of shares?
    #     try:
    #         shares = int(request.form.get("shares"))
    #     except:
    #         return apology("shares must be a positive integer")

    #     # Select users symbol/shares
    #     user_shares = db.execute("SELECT SUM(shares) as total_shares FROM portfolio WHERE user_id = :user_id and symbol = :symbol GROUP BY symbol", user_id = session["user_id"], symbol=stock["symbol"])

    #     # Enough shares to sell?
    #     if not user_shares or int(user_shares[0]["shares"]) < shares:
    #         return apology("Not enough shares")

    #     # Upadte user cash
    #     db.execute("UPDATE users SET cash = cash + :purchase WHERE user_id=:user_id ", user_id=session["user_id"], purchase=stock["price"] * shares)

    #     # Decrement shares count
    #     shares_total = user_shares[0]["shares"] - shares

    #     # If shares is at 0 after sale - remove stock from db
    #     if shares_total == 0:
    #         db.execute("DELETE FROM porfolio WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=stock["symbol"])

    #     # If not at 0 just update count
    #     else:
    #         db.execute("UPDATE portfolio SET shares=:shares WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=stock["symbol"])

    #     # Return to the index after transaction
    #     return redirect(url_for("index"))