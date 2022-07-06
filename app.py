from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User
from forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
connect_db(app)

@app.route("/")
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email= form.email.data
        user = User.register(username, password, first_name, last_name, email)
        db.session.commit()
        session['username'] = user.username
        return redirect('/secret')
    return render_template('register.html', form=form)

@app.route('/secret')
def secret():
    if 'username' not in session:
        return redirect('/login')
    return render_template('secret.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect("/secret")
        
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user: 
            session['username'] = user.username
            return redirect('/secret')
            
        else:
            form.username.errors = ['invalid']
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop("username")
    return redirect("/login")



