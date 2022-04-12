import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

basedir = os.path.abspath(os.path.dirname(__file__))

secret = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db=SQLAlchemy(app)

Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)

admin = Admin(app,name='Admin Page',template_mode='bootstrap3')

from maintenance_logger.models import Employee, Equipment, Service
from maintenance_logger.forms import LoginEmployee, AddService
from maintenance_logger.administration.views import EmployeeView, EquipmentView



admin.add_view(EmployeeView(Employee, db.session))
admin.add_view(EquipmentView(Equipment, db.session))


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(user_id)


# Commom @app.routes:

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/database')
@login_required
def database():
    employee_list = Employee.query.all()
    equipment_list = Equipment.query.all()
    service_list = Service.query.all()

    return render_template('database.html', 
                            employee_list=employee_list,
                            equipment_list=equipment_list,
                            service_list=service_list)




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
                return render_template('login_employee.html', form=form, login_err=True)

        else:
            return render_template('login_employee.html', form=form, login_err="Email or/and Password incorrect")
    
    return render_template('login_employee.html', form=form)

@app.route('/employee/logout')
@login_required
def logoutEmployee():
    logout_user()
    return redirect(url_for('index'))



# @app.route('/employee/add', methods=['GET','POST'])
# def addEmployee():
#     form = AddEmployee()

#     if form.validate_on_submit():
#         new_employee = Employee(form.employeeid.data,
#                                 form.firstname.data,
#                                 form.lastname.data,
#                                 form.email.data,
#                                 form.password.data)
#         db.session.add(new_employee)
#         db.session.commit()
#         return redirect(url_for('loginEmployee'))
    
#     return render_template('add_employee.html', form=form)



# Equipment @app.routes:

# @app.route('/equipment/add', methods=['GET','POST'])
# @login_required
# def addEquipment():
#     form = AddEquipment()

#     if form.validate_on_submit():
#         new_equipment = Equipment(form.entity.data,
#                                 form.description.data,
#                                 form.location.data)
#         db.session.add(new_equipment)
#         db.session.commit()
#         return redirect(url_for('index'))
    
#     return render_template('add_equipment.html', form=form)



# Service @app.routes:

@app.route('/service/add', methods=['GET', 'POST'])
@login_required
def addService():
    form = AddService()

    if form.validate_on_submit():
        equipment = Equipment.query.filter_by(entity = form.entity.data).first()
        new_service = Service(current_user.id, 
                              equipment.id,
                              form.description.data,
                              form.servdate.data)
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_service.html', form=form)


