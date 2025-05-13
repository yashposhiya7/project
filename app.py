from crypt import methods
from curses import flash
import email
from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from db1 import execute_query
import time


app = Flask(__name__)
app.secret_key = "Affinity@2005"

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        check = execute_query("SELECT EXISTS( SELECT 1 FROM user_data WHERE email = %s);", (email,))
        if check[0][0] == True:
            info = execute_query("SELECT pass,full_name FROM user_data WHERE email = %s;", (email,))[0]
            pass_word = info[0]
            full_name = info[1]
            if pass_word == password:
                flash(f"Weclcome Back {full_name}! 👏", 'success')
                return redirect(url_for("landing"))
            else:
                flash("Password Is Wrong ⚠️", "error")
                return redirect(url_for("signin"))
        else:
            flash("Account Doesn't Exists!⚠️", "error")
            return redirect(url_for("signin"))
    return render_template("signin.html")


@app.route("/signup", methods =["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        try:
            check = execute_query("SELECT EXISTS( SELECT 1 FROM user_data WHERE email = %s);", (email,))

            if not confirm_password == password:
                flash("Password Doesn't Match!", "error")
                return render_template("signup.html")

            else:
                execute_query("INSERT INTO user_data(full_name,email,pass) VALUES (%s,%s,%s);", (name,email,password))
                flash(f"Sign Up Successful! {name}", "success")
                return redirect(url_for("landing"))

        except Exception as e:
            flash("Something Went Wrong!", "error")
            return redirect(url_for("signup"))
    return render_template("signup.html")



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5556, debug=True)



# check = execute_query("SELECT EXISTS( SELECT 1 FROM user_data WHERE email = 'yashposhiya');")#, #(email,))
# print(check)


# pass_word = execute_query("SELECT pass,full_name FROM user_data WHERE email = %s;", ('poshiyayash7@gmail.com',))[0]
# pass_word = pass_word[1]
# print(pass_word)