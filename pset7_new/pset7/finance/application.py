from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    info=db.execute("SELECT username,cash FROM users WHERE id = :user_id",user_id=session["user_id"])
    buy_history = db.execute("SELECT symbol,sum(shares),price FROM transactions WHERE userid =:user_id AND type ='BUY' GROUP BY symbol",user_id=session["user_id"])
    sell_history = db.execute("SELECT symbol,sum(shares),price FROM transactions WHERE userid =:user_id AND type ='SELL' GROUP BY symbol",user_id=session["user_id"])
    if buy_history == None or sell_history == None:
        return apology("No transactions done")
    history=[]
    net=10000
    for brow in buy_history:
        row = brow
        for srow in sell_history:
            if srow["symbol"]==brow["symbol"]:
                row["sum(shares)"]=brow["sum(shares)"]-srow["sum(shares)"]
                net=net+srow["price"]*srow["sum(shares)"]- brow["price"]*srow["sum(shares)"]
        history.append(row)   
    n=len(history)
    if n>=1:
        stocks=[]
        for i in range(n):
            row=lookup(history[i]["symbol"])
            stocks.append(row)
        return render_template("index.html",info=info,history=history,stocks=stocks,n=n,net=net)
    else:
        return render_template("index.html",info=info,history=[],stocks=[],n=0,net=net)
        
        
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        if not request.form.get("stock_symbol"):
            return apology("must provide a symbol")
        stock = lookup(request.form.get("stock_symbol"))
        if stock == None:
            return apology("Invalid symbol")    
        if not request.form.get("shares"):
            return apology("must provide amount")
        elif not request.form.get("shares").isnumeric():
            return apology("Invalid shares")
        elif int(request.form.get("shares")) <= 0:
            return apology("must provide a postive share")
        shares = db.execute("SELECT * FROM users WHERE id = :user_id",user_id=session["user_id"])
        if shares[0]["cash"] < int(request.form.get("shares"))*stock["price"]:
            return apology("not enough shares")
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",cash=(shares[0]["cash"]-int(request.form.get("shares"))*stock["price"]),user_id=session["user_id"])
        db.execute("INSERT INTO transactions (type,userid,symbol,shares,price,total) VALUES('BUY',:user_id,:symbol,:share,:price,:total)",user_id=session["user_id"],symbol = stock["symbol"],share = int(request.form.get("shares")),price = stock["price"],total=int(request.form.get("shares"))*stock["price"])
        return redirect(url_for("index"))
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    history = db.execute("SELECT * FROM transactions WHERE userid =:user_id ORDER BY time",user_id=session["user_id"])
    n=len(history)
    if n>=1:
        stocks=[]
        for i in range(n):
            row=lookup(history[i]["symbol"])
            stocks.append(row)
        return render_template("history.html",history=history,stocks=stocks,n=n)        
    else:
        return render_template("history.html",history=[],stocks=[],n=0)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("stock_symbol"):
            return apology("must provide a symbol")
        
        stock=lookup(request.form.get("stock_symbol"))
        if stock == None:
            return apology("Invalid symbol")
        return render_template("quoted.html",name=stock["name"],price=stock["price"],symbol=stock["symbol"])
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
            
        # ensure password was confirmed
        elif not request.form.get("password_confirm"):
            return apology("must confirm password")    
            
        # ensure passwords match    
        elif request.form.get("password")!=request.form.get("password_confirm"):
            return apology("passwords do not match")
            
        # insert new user into database
        db.execute("INSERT INTO users (username,hash) VALUES(:username,:pass_hash)",username=request.form.get("username"),pass_hash=pwd_context.hash(request.form.get("password")))

        return redirect(url_for("login"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    buy_history = db.execute("SELECT symbol,sum(shares) FROM transactions WHERE userid =:user_id AND type ='BUY' GROUP BY symbol",user_id=session["user_id"])
    sell_history = db.execute("SELECT symbol,sum(shares) FROM transactions WHERE userid =:user_id AND type ='SELL' GROUP BY symbol",user_id=session["user_id"])
    history=[]
    for brow in buy_history:
        row = brow
        for srow in sell_history:
            if srow["symbol"]==brow["symbol"]:
                row["sum(shares)"]=brow["sum(shares)"]-srow["sum(shares)"]
        history.append(row)   
    if request.method == "POST":
        if not request.form.get("stock_symbol"):
            return apology("must provide a symbol")
        stock = lookup(request.form.get("stock_symbol"))
        if stock == None:
            return apology("Invalid symbol")
        flag = 0
        index = 0
        for row in history:
            if row["symbol"] == request.form.get("stock_symbol"):
                flag=1
                break
            else:
                index=index+1
        if flag == 0:
            return apology("No shares available")
        if not request.form.get("shares"):
            return apology("must provide amount")
        elif not request.form.get("shares").isnumeric():
            return apology("Invalid shares")
        elif history[index]["sum(shares)"] < int(request.form.get("shares")):
            return apology("Not enough shares")
        shares = db.execute("SELECT * FROM users WHERE id = :user_id",user_id=session["user_id"])
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",cash=(shares[0]["cash"]+int(request.form.get("shares"))*stock["price"]),user_id=session["user_id"])
        db.execute("INSERT INTO transactions (type,userid,symbol,shares,price,total) VALUES('SELL',:user_id,:symbol,:share,:price,:total)",user_id=session["user_id"],symbol = stock["symbol"],share = int(request.form.get("shares")),price=stock["price"],total=int(request.form.get("shares"))*stock["price"])
        
        return redirect(url_for("index"))
    else:
        return render_template("sell.html",history=history)
    
    
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("old_password"):
            return apology("must provide your old password")

        # ensure password was submitted
        elif not request.form.get("new_password"):
            return apology("must provide a new password")
        
        elif not request.form.get("password_confirm"):
            return apology("Must confirm new password")
            
        # query database for username
        rows = db.execute("SELECT * FROM users WHERE id=:user_id", user_id=session["user_id"])

        # ensure username exists and password is correct
        if not pwd_context.verify(request.form.get("old_password"), rows[0]["hash"]):
            return apology("invalid password")
        
        if request.form.get("new_password") != request.form.get("password_confirm"):
            return apology("Passwords do not match")
        db.execute("UPDATE users SET hash =:new_hash WHERE id =:user_id",new_hash=pwd_context.hash(request.form.get("new_password")),user_id=session["user_id"])
        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_password.html")
    