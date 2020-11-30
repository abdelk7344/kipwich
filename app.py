from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
application = app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingredients.db'
# Initialize the database
db = SQLAlchemy(app)

migrate = Migrate(app, db)


bootstrap = Bootstrap(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    ingredient = None
    form = IngForm()
    if form.validate_on_submit():
        new_ingredient = Ingredients(name=form.ingredient.data)

        # Push to Database
        try:
            db.session.add(new_ingredient)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding your ingredient"


       # ingredient = form.ingredient.data #OLD FROM ASSG07
       # form.ingredient.data = ''    #OLD FROM ASSG07
    else:
        ingredients = Ingredients.query.order_by(Ingredients.date_created)
        return render_template('index.html', form=form, ingredients = ingredients)

@app.route('/asg10/update/<int:idD>', methods=['GET', 'POST'])
def hello(idD):
    ingredient_to_up = Ingredients.query.get_or_404(idD)

    form =UpdateForm()
    if form.validate_on_submit():
        ingredient_to_up.name = form.updatedingredient.data
        try: 
            db.session.commit()
            return redirect('/')
        except:
            return "ERROR Updating"
    else: 
        return render_template('update.html', ingredient_to_up = ingredient_to_up, form =form)

    

@app.route('/asg10/delete/<int:idC>')
def delete(idC):
    ingredient_to_del = Ingredients.query.get_or_404(idC)

    try:
        db.session.delete(ingredient_to_del)
        db.session.commit()
        return redirect('/')

    except:
        return "ERROR Deleting"
