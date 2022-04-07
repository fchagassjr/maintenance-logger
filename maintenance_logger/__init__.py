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

from maintenance_logger.models import Employee, Equipment, Service
from maintenance_logger.forms import AddEmployee, LoginEmployee, AddService


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(user_id)


# Commom @app.routes:

@app.route('/')
def index():
    return render_template('index.html')



# Employee @app.routes:

@app.route('/employee/login', methods=['POST','GET'])
def loginEmployee():
    form = LoginEmployee()

    if form.validate_on_submit():
        user = Employee.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return render_template('login_employee.html', form=form, err="Email or/and Password incorrect")

        else:
            return render_template('login_employee.html', form=form, err="Email or/and Password incorrect")
    
    return render_template('login_employee.html', form=form)

@app.route('/employee/logout')
@login_required
def logoutEmployee():
    logout_user()
    return redirect(url_for('index'))



@app.route('/employee/add', methods=['GET','POST'])
def addEmployee():
    form = AddEmployee()

    if form.validate_on_submit():
        new_employee = Employee(form.employee_id.data,
                                form.first_name.data,
                                form.last_name.data,
                                form.email.data,
                                form.password.data)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('loginEmployee'))
    
    return render_template('add_employee.html', form=form)



@app.route('/employee/list')
@login_required
def listEmployee():
    employee_list = Employee.query.all()
    listOutput = ''
    for employee in employee_list:
        listOutput += f'<h3>{employee.first_name} {employee.last_name}</h3>{employee.email}<br>'
    
    return listOutput


# Equipment @app.routes:

# Service @app.routes:

@app.route('service/add')
@login_required
def addService():
    form = AddService()

    if form.validate_on_submit():
        equipment = Equipment.query.filter_by(entity = form.entity.data).first()
        new_service = Service(current_user.id, 
                              equipment.id,
                              form.description.data,
                              form.date.data)
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_service.html', form=form)


