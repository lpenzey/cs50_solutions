import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
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
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Select all symbols and amounts owned by the user
    portfolio_symbols = db.execute("SELECT shares, symbol FROM portfolio WHERE id = :id", id=session["user_id"])

    # Create net worth variable
    total_value = 0

    # Retrieve current stock prices and calculate total value
    for portfolio_symbol in portfolio_symbols:
        symbol = portfolio_symbol["symbol"]
        shares = portfolio_symbol["shares"]
        stock = lookup(symbol)
        total = shares * stock["price"]
        total_value += total
        db.execute("UPDATE portfolio SET price=:price, \
                    total=:total WHERE id=:id AND symbol=:symbol", \
                    price=usd(stock["price"]), \
                    total=usd(total), id=session["user_id"], symbol=symbol)

    # Update cash in portfolio
    updated_cash = db.execute("SELECT cash FROM users \
                               WHERE id=:id", id=session["user_id"])

    # Update net worth to equal cash plus stock value
    total_value += updated_cash[0]["cash"]

    # print portfolio in index homepage
    updated_portfolio = db.execute("SELECT * from portfolio \
                                    WHERE id=:id", id=session["user_id"])

    return render_template("index.html", stocks=updated_portfolio, \
                            cash=usd(updated_cash[0]["cash"]), total= usd(total_value) )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Ensure stock symbol is not blank
        if not request.form.get("symbol"):
            return apology("Stock symbol cannot be blank")

        elif not request.form.get("shares"):
            return apology("Number of shares cannot be blank")

        # Look up stock symbol
        else:
            quote = lookup(request.form.get("symbol"))

            # Ensure stock symbol is valid
            if not quote:
                return apology("Invalid stock symbol")

            # If stock symbol is valid check if user can afford purchase
            else:
                # Get share price
                share_price = quote["price"]

                # Create shares variable
                shares = int(request.form.get("shares"))

                # Calculate order cost
                order_cost = share_price * shares

                # Query db for users cash
                cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

                cash_money = cash[0]["cash"]

                if order_cost > cash_money:
                    return apology("You do not have enough money to buy this much stock")

                # Subtract order cost from cash if sufficient funds
                db.execute("UPDATE users SET cash = cash - :order_cost \
                    WHERE id = :id", id=session["user_id"], \
                    order_cost=share_price * int(request.form.get("shares")))

                # Select user shares of desired symbol
                existing_shares = db.execute("SELECT shares FROM portfolio \
                           WHERE id = :id AND symbol = :symbol", \
                           id=session["user_id"], symbol=quote["symbol"])

                # if user doesn't has shares of that symbol, create new stock object
                if not existing_shares:
                    db.execute("INSERT INTO portfolio (id, symbol, shares, price, name, total) \
                        VALUES (:id, :symbol, :shares, :price, :name, :total)", \
                        id=session["user_id"], symbol=quote["symbol"], \
                        shares=shares, price=quote["price"], name=quote["name"], total=order_cost)

                # Else increment the shares count
                else:
                    shares_total = existing_shares[0]["shares"] + shares
                    db.execute("UPDATE portfolio SET shares=:shares \
                                WHERE id = :id AND symbol = :symbol", \
                                shares=shares_total, id=session["user_id"], \
                                symbol=quote["symbol"])

                # Add purchase into histories table
                db.execute("INSERT INTO history (type, symbol, price, shares, id) \
                    VALUES(:type, :symbol, :price, :shares, :id)", \
                    type="Bought", symbol=quote["symbol"], price=usd(quote["price"]), \
                    shares=shares, id=session["user_id"])

                return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    histories = db.execute("SELECT * from history WHERE id=:id", id=session["user_id"])

    return render_template("history.html", histories=histories)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Ensure search is not blank
        if not request.form.get("symbol"):
            return apology("Search cannot be blank")

        # Look up stock symbol
        else:
            quote = lookup(request.form.get("symbol"))

            # Ensure stock symbol is valid
            if not quote:
                return apology("Invalid stock symbol")

            # If stock symbol is valid display the price
            else:
                return render_template("stock.html", stock=quote["price"])

    else:
        return render_template("quote.html")

@app.route("/money", methods=["GET", "POST"])
@login_required
def moola():
    """Print Money"""
    if request.method == "POST":
        moola = int(request.form.get("moola"))

        # Add cash
        db.execute("UPDATE users SET cash = cash + :moola \
            WHERE id = :id", id=session["user_id"], \
            moola=moola)

        return redirect("/")

    else:
        return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirm_password"):
            return apology("must confirm password", 403)

        # Ensure password confirmation was submitted
        elif not request.form.get("password") == request.form.get("confirm_password"):
            return apology("passwords must match", 403)

        # Encrypt password
        hash = generate_password_hash(request.form.get("password"))

        # Insert user into database
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=hash)

        # If user already exists return apology
        if not result:
            return apology("Username already exists")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return render_template("quote.html")

    else:
        return render_template("register.html")
    # return apology("TODO")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
         # Ensure stock symbol is not blank
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("Stock symbol cannot be blank")

        elif not shares:
            return apology("Number of shares cannot be blank")

        # Look up stock symbol
        else:
            quote = lookup(symbol)

            # Ensure stock symbol is valid
            if not quote:
                return apology("Invalid stock symbol")

            # If stock symbol is valid check if user has enough shares of said stock
            else:
                existing_shares = db.execute("SELECT shares FROM portfolio \
                    WHERE id = :id AND symbol = :symbol", id=session["user_id"], symbol=quote["symbol"])

                # decrement the shares count
                if not existing_shares:
                    return apology("You can't sell shares you don't own")

                shares_total = existing_shares[0]["shares"]

                if shares_total < shares:
                    return apology("you do not have that many shares to sell")

                else:
                    # Get share price
                    share_price = quote["price"]

                    # Calculate sale cost
                    sale_total = share_price * shares

                    # Query db for users cash
                    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

                    cash_money = cash[0]["cash"]

                    # Add sales total to cash
                    db.execute("UPDATE users SET cash = cash + :sale_total \
                        WHERE id = :id", id=session["user_id"], \
                        sale_total=sale_total)

                    # Update the shares count
                    shares_total = existing_shares[0]["shares"] - shares

                    # If shares go to zero delete stock from portfolio
                    if shares_total == 0:
                        db.execute("DELETE FROM portfolio \
                        WHERE id=:id AND symbol=:symbol", \
                        id=session["user_id"], \
                        symbol=quote["symbol"])

                    # If not zero, update portfolio
                    else:
                        db.execute("UPDATE portfolio SET shares=:shares \
                            WHERE id = :id AND symbol = :symbol", \
                            shares=shares_total, id=session["user_id"], \
                            symbol=quote["symbol"])

                    # Add sale into histories table
                    db.execute("INSERT INTO history (type, symbol, price, shares, id) \
                        VALUES(:type, :symbol, :price, :shares, :id)", \
                        type="Sold", symbol=quote["symbol"], price=usd(quote["price"]), \
                        shares=shares, id=session["user_id"])

                    return redirect("/")

    else:
        return render_template("sell.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
