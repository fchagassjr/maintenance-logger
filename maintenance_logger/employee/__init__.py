from maintenance_logger import db
from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_required, login_user, logout_user
from maintenance_logger.models import Employee, Equipment, Service
from maintenance_logger.employee.forms import LoginEmployee, AddService

bp_employees = Blueprint('employees', __name__,
                        template_folder='templates')


@bp_employees.route('/database')
@login_required
def database():
    employee_list = Employee.query.all()
    equipment_list = Equipment.query.all()
    service_list = Service.query.all()

    return render_template('database.html', 
                            employee_list=employee_list,
                            equipment_list=equipment_list,
                            service_list=service_list)




# Employee related routes:

@bp_employees.route('/employee/login', methods=['POST','GET'])
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

@bp_employees.route('/employee/logout')
@login_required
def logoutEmployee():
    logout_user()
    return redirect(url_for('index'))


@bp_employees.route('/service/add', methods=['GET', 'POST'])
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
