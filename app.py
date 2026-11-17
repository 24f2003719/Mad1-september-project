from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3
from werkzeug.security import check_password_hash,generate_password_hash
app=Flask(__name__)
app.secret_key="replace-with-a-random-secret"
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

       
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = request.form.get("role", "")

        
        if user not in ("student", "examiner"):
            return "Invalid role selected", 400

        
        if not name or not email or not password:
            return "All fields are required", 400

        
        connection = sqlite3.connect("examination.db")
        cursor = connection.cursor()

        try:
            
            cursor.execute(
                "SELECT id FROM users WHERE email = ?",
                (email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:
                return "Email already registered", 400

            
            password_hash = generate_password_hash(password)

            
            status = "pending" if user == "examiner" else "active"

            
            cursor.execute(
                """
                INSERT INTO users
                (name, email, password_hash, role, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, email, password_hash, user, status)
            )

            connection.commit()

           
            return redirect(url_for("home"))

        except sqlite3.IntegrityError:
            connection.rollback()
            return "This email is already registered", 400

        finally:
            connection.close()

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email=request.form.get("email", "").strip().lower()
        password=request.form.get("password", "")
        
        connection=sqlite3.connect("examination.db")
        connection.row_factory =sqlite3.Row
        
        try:
            cursor=connection.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE email =?",
                (email,)
            )
            user=cursor.fetchone()
        finally:
            connection.close()
            
        if user is None or not check_password_hash(
            user["password_hash"],password
        ):
            return "Invalid email or password",401
        
        if user["status"] !="active":
            return "Your account is pending approval or inactive.", 403
        
        session.clear()
        session["user_id"]=user["id"]
        session["role"]=user["role"]
        
        if user["role"] =="admin":
            return redirect(url_for("admin_dashboard"))
        elif user["role"] == "examiner":
            return redirect(url_for("examiner_dashboard"))    
        else:
            return redirect(url_for('student_dashboard'))
        
    return render_template("login.html")
    
if __name__== "__main__":
    app.run(debug=True)
    