import os
import requests
import json

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup

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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///library.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of notes"""
    uid = session["user_id"]
    rows = db.execute("SELECT * FROM users WHERE id = :id",id=uid)
    username = rows[0]["username"]
    details = db.execute("SELECT * FROM books WHERE userid = :userid",userid = uid)
    return render_template("index.html", username = username, details = details)


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
        #print(rows[0]["hash"])
        #print(check_password_hash(rows[0]["hash"], request.form.get("password")))
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

        elif not request.form.get("confirm_password"):
            return apology("must confirm password", 403)

        elif request.form.get("password")!=request.form.get("confirm_password") :
            return apology("passwords must match", 400)

        # Query database for username
        db.execute("INSERT INTO users (username,hash) VALUES(:username,:hashval)",
                          username=request.form.get("username"),hashval=generate_password_hash(request.form.get("password")))

        # Redirect user to login page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/about/about_quikbooks", methods=["GET"])
def about():
    """About quikbooks"""
    return render_template("about.html")


@app.route("/about/getting_started", methods=["GET"])
def getting_started():
    """Getting started with quikbooks"""
    return render_template("started.html")

@app.route("/about/get_involved", methods=["GET"])
def get_involved():
    """Getting started with quikbooks"""
    return render_template("get_involved.html")



@app.route("/settings/profile", methods=["GET", "POST"])
@login_required
def profile():
    """view your profile"""
    uid = session["user_id"]
    # data = request.get_json()
    # if(data):
    #     img_src = data["img_src"]
    #     db.execute("UPDATE users SET img_src =:new_img_src WHERE id =:user_id",new_img_src=img_src,user_id=uid)
    user_info = db.execute("SELECT * FROM users WHERE id = :id",id=uid)
    username = user_info[0]["username"]
    return render_template("profile.html",username = username,user_info = user_info[0])

@app.route("/settings/account", methods=["GET", "POST"])
@login_required
def account():
    """view your account information"""
    uid = session["user_id"]
    account_info = db.execute("SELECT * FROM users WHERE id = :id",id=uid)
    return render_template("account.html", account_info = account_info[0])



@app.route("/library")
@login_required
def library():
    """view your library"""
    return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    uid = session["user_id"]
    rows = db.execute("SELECT * FROM users WHERE id = :id",id=uid)
    username = rows[0]["username"]
    trans_details = db.execute("SELECT * FROM transactions WHERE userid = :userid ORDER BY time DESC",userid = uid)
    return render_template("history.html", username = username, trans_details = trans_details)

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Book search."""
    uid = session["user_id"]
    rows = db.execute("SELECT * FROM users WHERE id = :id",id=uid)
    username = rows[0]["username"]
    if request.method == "POST":
        if not request.form.get("book"):
            return apology("must provide a title/author")
        option = None
        if "options" in request.form:
            option = request.form["options"]
        if option == "title":
            book_details = lookup(request.form.get("book"),"title")
        elif option == "author":
            book_details = lookup(request.form.get("book"),"author")
        else:
            return apology("Invalid search")
        #print(book_details)

        md5={}
        book_ids = []
        present_ids = set()
        md5_url = "http://libgen.io/json.php"

        present_books = db.execute("SELECT bookid FROM books WHERE userid = :uid",uid=uid)
        for book in present_books:
            present_ids.add(book["bookid"])
        #print(present_ids)
        book_details = [item for item in book_details if int(item["id"]) not in present_ids]
        book_ids = [item["id"] for item in book_details]
        #print(book_details)
        #print(book_ids)

        if len(book_ids) > 0:
            book_ids = ','.join(book_ids)
            #print(book_ids)
            params = dict(
                ids = book_ids,
                fields ='MD5'
            )
            full_url = md5_url+'?ids='+book_ids+'&fields=MD5'
            #response = requests.get(url = md5_url, params = params)
            response = requests.get(url = full_url)
            response_text = response.text
            #response_text = response_text[2:]
            print(response_text)
            result = json.loads(response_text)
            print(result)
            for detail in book_details:
                md5[detail["id"]] = result[0]["md5"]
            #print(md5)
        return render_template("searched.html",username = username,book_details = book_details, md5 = md5)
    else:
        return render_template("search.html",username = username)

# @app.route('/addImgsrc', methods = ['POST'])
# def addImgsrc():
#     # read json + reply
#     uid = session["user_id"]
#     data = request.get_json()
#     if(data):
#         img_src = data["img_src"]
#         print(img_src)
#         db.execute("UPDATE users SET img_src =:new_img_src WHERE id =:user_id",new_img_src=img_src,user_id=uid)
#     return redirect("/")

@app.route('/addItem', methods = ['POST'])
def addItem():
    # read json + reply
    uid = session["user_id"]
    data = request.get_json()
    if data:
        book_id = data["book_id"]
        #print(book_id)
        row = db.execute("SELECT * FROM books WHERE bookid=:bid and userid =:uid",bid=book_id,uid=uid)
        if len(row) == 0:
            md5_url = "http://libgen.io/json.php"
            params = dict(
                ids = book_id,
                fields ='Title,Author,Publisher,Year,Pages,MD5'
            )
            full_url = md5_url+'?ids='+book_id+'&fields=Title,Author,Publisher,Year,Pages,MD5'
            #response = requests.get(url = md5_url, params = params)
            response = requests.get(url = full_url)
            response_text = response.text
            #response_text = response_text[2:]
            print(response_text)
            result = json.loads(response_text)
            print(result)
            md5 = result[0]["md5"]
            mlink = "http://libgen.io/get.php?md5="+md5+"&oftorrent"
            pdflink = "http://libgen.io/get.php?md5="+md5
            db.execute("INSERT INTO books (userid,bookid,title,author,magnetlink,pdflink,year,pages,publisher) VALUES(:uid,:bid,:title,:author,:mlink,:pdflink,:year,:pages,:publisher)",uid = uid ,bid=book_id, title = result[0]["title"],author = result[0]["author"],mlink = mlink,pdflink = pdflink,year = result[0]["year"],pages = result[0]["pages"],publisher = result[0]["publisher"])
            db.execute("INSERT INTO transactions (userid,bookid,title,author,action) VALUES(:uid,:bid,:title,:author,:action)",uid = uid,bid = book_id,title = result[0]["title"],author = result[0]["author"],action ="Added")
    return redirect("/")


@app.route('/removeItem', methods = ['POST'])
def removeItem():
    # read json + reply
    uid = session["user_id"]
    data = request.get_json()
    if data:
        book_id = data["book_id"]
        #print(book_id)
        row = db.execute("SELECT * FROM books WHERE bookid=:bid and userid=:uid",bid=book_id,uid = uid)
        #print(row)
        db.execute("INSERT INTO transactions (userid,bookid,title,author,action) VALUES(:uid,:bid,:title,:author,:action)",uid = uid,bid = book_id,title = row[0]["title"],author = row[0]["author"],action ="Removed")
        db.execute("DELETE FROM books WHERE bookid=:bid and userid=:uid",bid=book_id, uid = uid)
    return redirect("/")

@app.route("/change_pwd", methods=["GET", "POST"])
@login_required
def change_pwd():

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
        if not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
            return apology("invalid password")

        if request.form.get("new_password") != request.form.get("password_confirm"):
            return apology("Passwords do not match")
        db.execute("UPDATE users SET hash =:new_hash WHERE id =:user_id",new_hash=generate_password_hash(request.form.get("new_password")),user_id=session["user_id"])
        # redirect user to home page
        return redirect("/")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_pwd.html")

@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # delete user from database
        db.execute("DELETE FROM transactions WHERE userid=:user_id", user_id=session["user_id"])
        db.execute("DELETE FROM books WHERE userid=:user_id", user_id=session["user_id"])
        db.execute("DELETE FROM users WHERE id=:user_id", user_id=session["user_id"])

    # redirect user to home page
    session.clear()
    return redirect("/login")

@app.route("/update_profile", methods=["POST"])
@login_required
def update_profile():

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        uid = session["user_id"]
        data = request.get_json()
        print(data)
        if(data):
            img_src = data["img_src"]
            print(img_src)
            db.execute("UPDATE users SET img_src =:new_img_src WHERE id =:user_id",new_img_src=img_src,user_id=uid)
        if request.form.get("fullname"):
            db.execute("UPDATE users SET full_name = :full_name WHERE id=:uid", full_name =request.form.get("fullname"),uid = uid)
        if request.form.get("email"):
            db.execute("UPDATE users SET email = :email WHERE id=:uid", email =request.form.get("email"),uid = uid)
        if request.form.get("website"):
            db.execute("UPDATE users SET website = :website WHERE id=:uid", website =request.form.get("website"),uid = uid)
        #if request.form.get("aboutme"):
        db.execute("UPDATE users SET about_me = :aboutme WHERE id=:uid", aboutme =request.form.get("aboutme"),uid = uid)
    return redirect("/settings/profile")

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
