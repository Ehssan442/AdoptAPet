from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask import Flask, request, render_template, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError

from models import db, User
from forms import SignUp, LogIn

''' Begin boilerplate code '''

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

''' End Flask Login Functions '''

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  login_manager.init_app(app)
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()
db.create_all(app=app)
''' End Boilerplate Code '''

@app.route('/', methods=['GET'])
def index():
  form = LogIn()
  return render_template('login.html', form=form)
  
@app.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): 
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): #checks database for match
        flash('Welcome back.') 
        login_user(user) 
        return render_template('main.html') 
  flash('Invalid credentials, Please try again or create an account if you do not currently have one')
  return redirect(url_for('index'))

@app.route('/signup', methods=['GET'])
def signup():
  form = SignUp() # create form object
  return render_template('signup.html', form=form)

@app.route('/signup', methods=['POST'])
def signupAction():
  form = SignUp() # create form object
  if form.validate_on_submit():
    data = request.form # get data from form submission
    newUser = User(username=data['username'], email=data['email']) # create user object
    newUser.set_password(data['password']) # set password
    db.session.add(newUser) 
    db.session.commit()
    flash('Account Created successfully. Welcome to the adopt-a-pet family!')
    return redirect(url_for('index'))
  flash('Error invalid input, Please try again.')
  return redirect(url_for('signup'))

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  flash('Logged Out, Thank You for Visiting!')
  return redirect(url_for('index')) 

app.run(host='0.0.0.0', port=8080, debug=True)