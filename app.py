from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy import ARRAY
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os




class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value

app = Flask(__name__)

image = os.path.join('static', 'image')
app.config['UPLOAD_FOLDER'] = image

app.config['SECRET_KEY'] = 'Thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NEWdatabase.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///bucket.db'
# app.config['SQLALCHEMY_BINDS']={'user': 'sqlite:///users.db'}
application = app
bootstrap = Bootstrap(app)

#intialize database
db=SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# db model



class NEWUser(UserMixin, db.Model):
    id= db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return NEWUser.query.get(int(user_id))


# class User(db.Model):
#     id= db.Column(db.Integer,primary_key=True)
#     username= db.Column(db.String(15), unique=True)
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(80))
#     def __repr__(self):
#         return '<User %r>' % self.username


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])


# class Bucket(db.Model):
#     id= db.Column(db.Integer,primary_key=True)
#     activity=db.Column(db.String(500),nullable=False)
#     def __repr__(self):
#         return '<Activity %r>' % self.id

# class Users(db.Model):
#     __bind_key__='user'
#     id= db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(500),nullable=False)
#     email=db.Column(db.String(500),nullable=False)
#     password=db.Column(db.String(500),nullable=False)
#     activities = db.Column(MutableList.as_mutable(ARRAY(db.String)))
#     def __repr__(self):
#         return '<User %r>' % self.id


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    img1 = os.path.join(app.config['UPLOAD_FOLDER'] , 'home1.jpg')
    return render_template('index.html' , user_image = img1) 
    
    #this is a temporary line that replaces the stuff below it
    # if request.method=="POST":
    #     activity_name=request.form['activity']
    #     new_activity=Bucket(activity=activity_name)
    #     try:
    #         db.session.add(new_activity)
    #         db.session.commit()
    #         return redirect('/')
    #     except:
    #         return "There was an error adding your activity"
         
    # else:
    #     all_activities=Bucket.query
    #     return render_template('index.html',all_activities=all_activities)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    activity_to_update= Bucket.query.get_or_404(id)
    if request.method=="POST":
        activity_to_update.activity=request.form['activity']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating your activity"
         
    else:
        return render_template('update.html',activity_to_update=activity_to_update)


@app.route('/delete/<int:id>')
def delete(id):
    activity_to_delete= Bucket.query.get_or_404(id)
    try:
        db.session.delete(activity_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that activity"


@app.route('/Home', methods=['GET', 'POST'])
def home():
    return render_template('Home.html')

@app.route('/SignUp', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()


    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method = 'sha256')
        new_user = NEWUser(username=form.username.data, email = form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))


        # return '<h1>' + form.username.data + form.password.data + form.email.data + '</h1>'

    return render_template('SignUp.html', form = form)


@app.route('/Login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = NEWUser.query.filter_by(username=form.username.data).first()
        if user: 
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('profile'))
                # return render_template('profile.html')


        return '<h1>invalid username or password</h1>'
        # return '<h1>' + form.username.data + form.password.data + '</h1>'


    return render_template('login.html', form = form)


@app.route('/Profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', name = current_user.username)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))











