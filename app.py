import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")
db = SQL(uri)


#Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

SUBJECTS = ["Ciencias Naturales", "Ciencias Sociales", "Lengua", "Matemáticas", "Varios", "Ciencia Ficción", "Poesía"]

# REGISTER
#-------------------------------------------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # check that none of the inputs were left blank.
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            print("All fields must be filled!")
            return render_template("register.html", error = 1, message = "¡Debes completar todos los campos!")

        # check that the name isn't already in use.
        same_username = db.execute("SELECT COUNT(username) FROM users WHERE username = ?", username)
        same_username = same_username[0]["count"]
        if same_username != 0:
            print("Username already exists!")
            return render_template("register.html", error = 1, message = "¡Nombre de usuario ya en uso!")
        # check that the password has at least six digits.
        if len(password) < 6:
            print("Password must be at least six digits long!")
            return render_template("register.html", error = 1, message = "¡La contraseña debe tener al menos seis caracteres!")
        # check that the password and its confirmation match.
        if password != confirmation:
            print("Password and confirmation do not match!")
            return render_template("register.html", error = 1, message = "¡La contraseña y su confirmación no coinciden!")

        # hash password and insert new user into database.
        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, password_hash)

        # insert principal subjects into subjects table for current user.
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)
        user_id = user_id[0]["id"]
        for subject in SUBJECTS:
            db.execute("INSERT INTO subjects(user_id, subject) VALUES (?, ?)", user_id, subject)

        # remember user in a session.
        session["user_id"] = user_id
        return redirect("/")
    else:
        return render_template("register.html", error = 0, )
#-------------------------------------------------------------------------------------------------


# LOGIN
#-------------------------------------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # If user reached route via POST:
    if request.method == "POST":

        # Ensure both username and password were submitted
        if not request.form.get("username") or not request.form.get("password"):
            print("All fields must be filled!")
            return render_template("login.html", error = 1, message = "¡Debes completar todos los campos!")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            print("invalid username and/or password")
            return render_template("login.html", error = 1, message = "¡Usuario o contraseña invalidos!")


        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # Else, if user reached route via GET:
    else:
        return render_template("login.html", error = 0)
#-------------------------------------------------------------------------------------------------


# LOGOUT
#-------------------------------------------------------------------------------------------------
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
#-------------------------------------------------------------------------------------------------


# INDEX
#-------------------------------------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # get user's id and username
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = username[0]["username"]

    if request.method == "POST":

         # Order by ID
        if request.form.get("order_by") == "ID":
            books = db.execute("SELECT * FROM books WHERE username = ? ORDER BY book_id", username)
            return render_template("index.html", books = books, username = username)

        # Order by subject
        if request.form.get("order_by") == "Tema":
            books = db.execute("SELECT * FROM books WHERE username = ? ORDER BY main_subject", username)
            return render_template("index.html", books = books, username = username)

        # Order by title
        elif request.form.get("order_by") == "Título":
            books = db.execute("SELECT * FROM books WHERE username = ? ORDER BY title", username)
            return render_template("index.html", books = books, username = username)

        # Order by author
        elif request.form.get("order_by") == "Autor":
            books = db.execute("SELECT * FROM books WHERE username = ? ORDER BY author", username)
            return render_template("index.html", books = books, username = username)

        # Order by colour
        elif request.form.get("order_by") == "Color":
            books = db.execute("SELECT * FROM books WHERE username = ? ORDER BY colour", username)
            return render_template("index.html", books = books, username = username)

        # Order by condition
        elif request.form.get("order_by") == "Condición":
            books = db.execute("SELECT * FROM books WHERE username = ? ORDER BY condition", username)
            return render_template("index.html", books = books, username = username)

        # Order by year of release
        elif request.form.get("order_by") == "Año":
            books = db.execute("SELECT * FROM books WHERE username = ? ORDER BY year", username)
            return render_template("index.html", books = books, username = username)

        # Order by type of cover
        elif request.form.get("order_by") == "Tapa":
            books = db.execute("SELECT * FROM books WHERE username = ? ORDER BY cover", username)
            return render_template("index.html", books = books, username = username)



    else:
        books = db.execute("SELECT * FROM books WHERE username = ?", username)
        if session.get("successfully_deleted") == 1:
            success = 2
            session.pop("successfully_deleted", None)
            return render_template("index.html", books = books, username = username, success = success, message = "El libro fue borrado con exito")

        elif session.get("successfully_added"):
            if not session.get("success"):
                success = 0
                session.pop("successfully_added", None)
                return render_template("index.html", books = books, username = username, success = success, message = "El libro no pudo ser agregado")
            else:
                success = 1
                book_id = session["book_id"]
                print()
                print(book_id)
                print()
                session.pop("success", None)
                session.pop("book_id", None)
                session.pop("successfully_added", None)
                return render_template("index.html", books = books, message = "Libro agregado exitosamente, ", success = success, username = username, book_id = book_id)
        else:
            return render_template("index.html", books = books, username = username)
#-------------------------------------------------------------------------------------------------


# ADD BOOK
#-------------------------------------------------------------------------------------------------
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    # get user's id and username
    user_id = session["user_id"]
    query = "SELECT " + '"username"' + " FROM " + '"users"' + " WHERE " + '"id" = ' + "'?'"
    username = db.execute(query, user_id)
    username = username[0]["username"]

    # get list of subjects
    query = "SELECT " + '"subject"' + " FROM " + '"subjects"' + " JOIN " + '"users"' + " ON " + '"users.id" = "subjects.user_id"' +  " WHERE " + '"user.id" = ' + "'?'"
    list_of_subjects = db.execute(query, user_id)
    subjects = list()
    for subject in list_of_subjects:
        subjects.append(subject["subject"])

    # If user reach rout via POST:
    if request.method == "POST":

        # Check that the user filled in the required fields
        if not request.form.get("title") or not request.form.get("subjects"):
            print("Please fill the obligatory fields")
            return render_template("add.html", subjects = subjects, error = 1, message = "¡Por favor rellena los campos obligatorios!", username = username)
        # store user's responses in variables
        title = request.form.get("title")
        colour = request.form.get("colour")
        year = request.form.get("year")
        year = str(year)
        condition = request.form.get("condition")
        form_subjects = request.form.getlist("subjects_opt")
        cover = request.form.get("cover")
        author = request.form.get("author")
        main_subject = request.form.get("subjects")

        # Convert any optional fields that weren't filled to "N/A"
        if len(form_subjects) == 3:
            subject0 = form_subjects[0]
            subject1 = form_subjects[1]
            subject2 = form_subjects[2]
        elif len(form_subjects) == 2:
            subject0 = form_subjects[0]
            subject1 = form_subjects[1]
            subject2 = "N/A"
        elif len(form_subjects) == 1:
            subject0 = form_subjects[0]
            subject1 = "N/A"
            subject2 = "N/A"
        else:
            subject0 = "N/A"
            subject1 = "N/A"
            subject2 = "N/A"
        if not colour:
            colour = "N/A"
        if  not year:
            year = "N/A"
        if not condition:
            condition = "N/A"
        if not cover:
            cover = "N/A"
        if not author:
            author = "N/A"

        # get the number to print to the spine of the book
        book_id = db.execute("SELECT COUNT(*) FROM books WHERE username = ?", username)
        book_id = book_id[0]["count"]
        # get the offset caused by deletions.
        offset = db.execute("SELECT offset FROM users WHERE username = ?", username)
        offset = offset[0]["offset"]
        print()
        print("OFFSET:")
        print(offset)
        print()
        book_id = book_id + offset
        # insert book info into the book table within the database;
        query0 = "INSERT INTO books(username, book_id, title, main_subject, subject0, subject1, subject2, author,"
        query1 = "colour, year, condition, cover) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        query = query0 + query1
        db.execute(query, username, book_id, title, main_subject, subject0, subject1, subject2, author, colour, year, condition, cover)
        session["successfully_added"] = 1
        session["success"] = 1
        session["book_id"] = book_id
        return redirect("/")
    else:
        return render_template("add.html", subjects = subjects, subjects_opt = subjects, username = username)
#-------------------------------------------------------------------------------------------------


#SEARCH FOR A BOOK
#-------------------------------------------------------------------------------------------------
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():

    # get user's id and username
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = username[0]["username"]

    # get list of subjects
    list_of_subjects = db.execute("SELECT subject FROM subjects JOIN users ON users.id = subjects.user_id WHERE users.id = ?", user_id)
    subjects = list()
    for subject in list_of_subjects:
        subjects.append(subject["subject"])

    # If user reach rout via POST:
    if request.method == "POST":

        # Delete books in case the user wants to.
        if request.form.get("delete") == "Borrar libro/s seleccionados":
            #selected = request.form.get("deletethis")
            if request.form.get("deletethis") == None:
                print("NO SELECCIONO NADA PARA BORRAR")
                return render_template("search.html", subjects = subjects, error = 1, message = "¡No seleccionaste ningun libro para borrar!", username = username)
            todelete = request.form.getlist("deletethis")
            for book in todelete:
                db.execute("DELETE FROM books WHERE username = ? AND book_id = ?", username, book)
                #update offset
                offset = db.execute("SELECT offset FROM users WHERE username = ?", username)
                offset = offset[0]["offset"]
                updated_offset = offset + 1
                db.execute("UPDATE users SET offset = ? WHERE username = ?", updated_offset, username)
            session["successfully_deleted"] = 1
            return redirect("/")

        # Check that the user filled in the required fields
        if not request.form.get("title") or not request.form.get("subjects"):
            print("Please fill the obligatory fields")
            return render_template("search.html", subjects = subjects, error = 1, message = "¡Por favor rellena los campos obligatorios!", username = username)

        # store user's responses in variables
        title = request.form.get("title")
        colour = request.form.get("colour")
        year = request.form.get("year")
        year = str(year)
        condition = request.form.get("condition")
        form_subjects = request.form.getlist("subjects_opt")
        cover = request.form.get("cover")
        author = request.form.get("author")
        main_subject = request.form.get("subjects")

        # Convert any optional fields that weren't filled to "N/A"
        if len(form_subjects) == 3:
            subject0 = form_subjects[0]
            subject1 = form_subjects[1]
            subject2 = form_subjects[2]
        elif len(form_subjects) == 2:
            subject0 = form_subjects[0]
            subject1 = form_subjects[1]
            subject2 = "N/A"
        elif len(form_subjects) == 1:
            subject0 = form_subjects[0]
            subject1 = "N/A"
            subject2 = "N/A"
        else:
            subject0 = "N/A"
            subject1 = "N/A"
            subject2 = "N/A"
        if not colour:
            colour = "N/A"
        if  not year:
            year = "N/A"
        if not condition:
            condition = "N/A"
        if not cover:
            cover = "N/A"
        if not author:
            author = "N/A"

        # "%" represents zero or more characters, I use it in case the user didn't type the full name
        title = "%" + title + "%"
        author = "%" + author + "%"

        #check if a book within the database meets the exact requirements provided
        subjects_list = [main_subject, subject0, subject1, subject2]
        query0 = "SELECT * FROM books WHERE title LIKE ? AND username = ? AND main_subject IN (?) AND subject0 IN (?) AND subject1 IN (?) AND subject2 IN (?) AND colour = ?"
        query1 = " AND year = ? AND condition = ? AND cover = ? AND author LIKE ?"
        query = query0 + query1
        print(title, username, subjects_list, colour, year, condition, cover, author)
        check_book = db.execute(query, title, username, subjects_list, subjects_list, subjects_list, subjects_list, colour, year, condition, cover, author)
        print(check_book) # JUST FOR DEBUGGING PURPOSES
        if len(check_book) != 0:
            attempt = 10
            amount_of_books_found = len(check_book)
            return render_template("found.html", books = check_book, amount = amount_of_books_found, attempt = attempt, username = username)


        # If unable to find a book, check again but this time only check for title and main subject, in case the user made a mistake
        query = "SELECT * FROM books WHERE title LIKE ? AND username = ? AND main_subject IN (?)"
        check_book = db.execute(query, title,  username, subjects_list)
        print(check_book) # JUST FOR DEBUGGING PURPOSES
        if len(check_book) != 0:
            print("POSSIBLY FOUND YOUR BOOK")
            attempt = 11
            amount_of_books_found = len(check_book)
            return render_template("found.html", books = check_book, amount = amount_of_books_found, attempt = attempt, username = username)

        # If still unable to find a book, check for the last time, this time only check for a similar title
        query = "SELECT * FROM books WHERE title LIKE ? AND username = ?"
        check_book = db.execute(query, title, username)
        print("VAMOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        print(check_book) # JUST FOR DEBUGGING PURPOSES
        if len(check_book) != 0:
            print("IS THIS YOUR BOOK?")
            attempt = 12
            amount_of_books_found = len(check_book)
            return render_template("found.html", books = check_book, amount = amount_of_books_found, attempt = attempt, username = username)
        else:
            print("THE BOOK WASN'T FOUND")
            attempt = 0
            amount_of_books_found = len(check_book)
            return render_template("found.html", books = check_book, amount = amount_of_books_found, attempt = attempt, username = username)
    else:
        return render_template("search.html", subjects = subjects, username = username)
#-------------------------------------------------------------------------------------------------

# SETTINGS
#-------------------------------------------------------------------------------------------------
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    # get user's id and username
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = username[0]["username"]

    if request.method == "POST":
        if request.form.get("new_subject") != None:
            if not request.form.get("new_subject"):
                print("Subject field is empty!")
                return redirect("/")
            new_subject = request.form.get("new_subject")
            db.execute("INSERT INTO subjects(user_id, subject) VALUES(?, ?)", user_id, new_subject)
            return render_template("settings.html", username = username, alert = 1, message = "Tema agregado correctamente")
        if request.form.get("old_pass") != None:
            oldpass = request.form.get("old_pass")
            newpass = request.form.get("new_pass")
            newpass_confirm = request.form.get("new_pass_confirm")
            user_info = db.execute("SELECT * FROM users WHERE username = ?", username)
            user_hash = user_info[0]["hash"]
            if check_password_hash(user_hash, oldpass) != True:
                print("Incorrect old password!")
                return render_template("settings.html", username = username, alert = 2, message = "¡Contraseña vieja incorrecta!")
            else:
                if newpass != newpass_confirm:
                    print("New password and confirmation don't match!")
                    return render_template("settings.html", username = username, alert = 3, message = "¡La nueva contraseña y su confirmación no coinciden!")
                elif len(newpass) < 6:
                    print("New password must be at least six digits long!")
                    return render_template("settings.html", username = username, alert = 4, message = "¡La contraseña debe ser de al menos 6 caracteres!")
                else:
                    newpass_hash = generate_password_hash(newpass)
                    db.execute("UPDATE users SET hash = ? WHERE username = ?", newpass_hash, username)
                    print("password updated successfully")
                    return render_template("settings.html", username = username, alert = 5, message = "¡Contraseña actualizada correctamente!")

    return render_template("settings.html", username = username)
#-------------------------------------------------------------------------------------------------
