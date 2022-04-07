import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)

from maintenance_logger.models import Personnel, Equipment, Service
from maintenance_logger.forms import AddPersonnel, LoginPersonnel


@login_manager.user_loader
def load_user(user_id):
    return Personnel.query.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personnel/login', methods=['POST','GET'])
def loginPersonnel():
    form = LoginPersonnel()

    if form.validate_on_submit():
        user = Personnel.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return render_template('login_personnel.html', form=form, err="Email or/and Password incorrect")

        else:
            return render_template('login_personnel.html', form=form, err="Email or/and Password incorrect")
    
    return render_template('login_personnel.html', form=form)

@app.route('/personnel/logout')
@login_required
def logoutPersonnel():
    logout_user()
    return redirect(url_for('index'))



@app.route('/personnel/add', methods=['GET','POST'])
def addPersonnel():
    form = AddPersonnel()

    if form.validate_on_submit():
        new_personnel = Personnel(form.first_name.data,
                                form.last_name.data,
                                form.email.data,
                                form.password.data)
        db.session.add(new_personnel)
        db.session.commit()
        return redirect(url_for('loginPersonnel'))
    
    return render_template('add_personnel.html', form=form)

@app.route('/personnel/list')
@login_required
def listPersonnel():
    personnel_list = Personnel.query.all()
    listOutput = ''
    for personnel in personnel_list:
        listOutput += f'<h3>{personnel.first_name} {personnel.last_name}</h3>{personnel.email}<br>'
    
    return listOutput