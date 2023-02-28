from flask import render_template, request, session, redirect, url_for, jsonify
from MyEmail import MyEmail
from _init_ import create_app
import json
from flask_mysqldb import MySQL


app = create_app()
db = MySQL(app)

@app.route("/", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form["email"] # get data from email input
        password = request.form["password"] # get data from password input
        cur = db.connection.cursor()
        query = "SELECT username, id FROM user WHERE email = %s AND password = md5(%s)"
        user_info = cur.execute(query, (email, password))

        if user_info > 0:
            detail = cur.fetchall()
            for i in detail:
                session['username'] = i[0] # insert name into session
                session['id'] = i[1]
            return redirect(url_for("dashboard"))

    return render_template("login.html")

# REGISTER PAGE
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data_submit = request.form['format_data']
        insert_data = json.loads(data_submit)
        name = insert_data["username"]
        email = insert_data["email"]
        password = insert_data["password"]
        cur = db.connection.cursor()
        query = "SELECT email FROM user"
        username_all = cur.execute(query)

        if username_all > 0:
            detail = cur.fetchall() # fecth all data 
            for user_email in detail:
                if email in user_email: # check existing data
                    return json.dumps({'data': 'fail'}), 200, {'ContentType': 'application/json'} # send back through AJAX (FAIL)
            cur = db.connection.cursor()
            cur.execute("INSERT INTO user (username, password, email) VALUES (%s, MD5(%s), %s)", (name, password, email))
            cur.connection.commit()
            cur.close()
            return json.dumps({'data': 'sucess'}), 200, {'ContentType': 'application/json'}  # send back through AJAX (SUCESS)
        else:
            cur = db.connection.cursor()
            cur.execute("INSERT INTO user (username, password, email) VALUES (%s, MD5(%s), %s)", (name, password, email))
            cur.connection.commit()
            cur.close()
            return json.dumps({'data': 'sucess'}), 200, {'ContentType': 'application/json'}  # send back through AJAX (SUCESS)

    return render_template("register.html") # click Link (after register redirect to login using javascript)
    
# DASHBOAD PAGE
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username=session['username'])
    else: # else go back to login
        return redirect(url_for("login"))

# GENERAL PAGE
@app.route("/general")
def get_general():
    if "username" in session: # check username in session
        cur = db.connection.cursor()
        query = "SELECT category_name FROM category"
        category = cur.execute(query)
        category_all = None
        if category > 0:
            category_all = cur.fetchall()
        return render_template("general.html", username=session['username'], category=category_all)

    else: # else go back to login
        return redirect(url_for("login"))

# LOGIN PAGE
@app.route("/login")
def logout():
    if "username" in session: # check username in session
        session.clear() # clear session
        return redirect(url_for("login")) # go to login page


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        request_email = request.form['email']
        smtp = MyEmail(request_email)
        smtp.email_generate()

    return render_template("forgot-password.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        action = request.form['action']
        if action == "get_user_detail":
            password = request.form["password"]
            cur = db.connection.cursor()
            query = "SELECT username, email, password from user where password = md5(%s)"
            cur.execute(query,(password,))
            user_detail = cur.fetchall()
            if user_detail:
                for data in user_detail:
                    username = data[0]
                    email = data[1]
                user_dict = {"username" : username, "email" : email}
                return json.dumps({'data': user_dict}), 200, {'ContentType': 'application/json'}
            else:
                return json.dumps({'data': "error"}), 200, {'ContentType': 'application/json'}

        if action == "update_data":
            data_user = request.form["data"]
            update_data = json.loads(data_user)
            if update_data['password'] ==  "":
                cur = db.connection.cursor()
                query = "UPDATE user set username = %s, email = %s where id = %s"
                cur.execute(query, (update_data['username'], update_data['email'], session['id']))
                cur.connection.commit()
                cur.close()
                session['username'] = update_data['username']
                return json.dumps({'status': 'save'}), 200, {'ContentType': 'application/json'}
                
            else:
                cur = db.connection.cursor()
                query = "UPDATE user set username = %s, email = %s , password = MD5(%s) where id = %s"
                cur.execute(query, (update_data['username'], update_data['email'], update_data['password'], session['id']))
                cur.connection.commit()
                cur.close()
                session['username'] = update_data['username']
                return json.dumps({'status': 'save'}), 200, {'ContentType': 'application/json'}

            

    if "username" in session:
        cur = db.connection.cursor()
        id_user = session['id']
        query = "SELECT username, email FROM user where id = %s"
        cur.execute(query, (id_user,))
        data_all = cur.fetchall()

        if data_all:
            data = data_all
        else:
            data = None
        return render_template("profile.html", username=session['username'], data=data)
    else:
        return redirect(url_for("login"))

    
if __name__ == "__main__":
    app.run(debug=True)

