# //////////////////
#  1
# step 1
@app.route("/logout")
# step 2
# step 3
def logout():
    session.clear()
# step 6
    flash("You have been logged out", "register")
# step 9
    return redirect('/')
# step 10

# ///////////////// 2 
# step 1
@app.route('/success')
# step 2
def success():
    # step 3
    query = "SELECT id, email, created_at FROM users;"
    emails = mysql.query_db(query)
    # step 6
    return render_template('success.html', emails = emails)
    # step 9

# /////////////////// 3
# step 1
@app.route('/delete/<id>')
# step 2
def delete(id):
    # step 3
    query = "DELETE FROM users WHERE id = %(id)s;"
    data = {"id": id}
    result = mysql.query_db(query, data)
    print('result from deleting', result)
    #  step 6
    return redirect('/success')
    # step 9

# ////////////////// 4
#  step 1
@app.route("/createUser", methods=['POST'])
# step 2
def create():
    #  step 3
    data = request.form
    emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    errors = False
    for key, value in data.items():
        if len(value)<1:
            #  step 6
            flash("This field is required", key)
            errors = True
    if data['email'] and not emailRegex.match(data['email']):
        #  step 6
        flash("Invalid email address", "email")
        errors = True
    if not errors:
        unique = mysql.query_db("SELECT * FROM users WHERE email = %s;", data['email'])
        if unique:
            #  step 6
            flash("This email has already been taken", "email")
        else:
            pw_hash = bcrypt.generate_password_hash(data['password'])
            query = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw_hash)s, NOW());"
            newuser = {"first_name" : data["first_name"],
                        "last_name" : data["last_name"],
                        "email" : data["email"],
                        "pw_hash" : pw_hash}
            created = mysql.query_db(query, newuser)
            if created:
                #  step 6
                flash("You've been successfully registered", "success")
                session['userid'] = created
                return redirect('/success')
    #  step 6
    flash("We're sorry, you could not be registered at this moment", "register")
    return redirect("/")
    #  step 9