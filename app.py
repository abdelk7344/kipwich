from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from sqlalchemy.ext.mutable import Mutable

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
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///bucket.db'
# app.config['SQLALCHEMY_BINDS']={'user': 'sqlite:///users.db'}
application = app
bootstrap = Bootstrap(app)

#intialize database
db=SQLAlchemy(app)
#db model
class Bucket(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    activity=db.Column(db.String(500),nullable=False)
    def __repr__(self):
        return '<Activity %r>' % self.id

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
    if request.method=="POST":
        activity_name=request.form['activity']
        new_activity=Bucket(activity=activity_name)
        try:
            db.session.add(new_activity)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding your activity"
         
    else:
        all_activities=Bucket.query
        return render_template('index.html',all_activities=all_activities)

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



@app.route('/SignUp', methods=['GET', 'POST'])
def signup():
    return render_template('SignUp.html')


@app.route('/Login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

