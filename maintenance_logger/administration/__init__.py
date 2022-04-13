from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import AdminIndexView, expose
from maintenance_logger.administration.forms import AddEmployee, AddEquipment, EditEmployee, EditEquipment
from werkzeug.security import generate_password_hash


class EmployeeView(ModelView):

    def is_accessible(self):
        if current_user.is_anonymous:
            return False
        else:
            if current_user.email == 'admin@admin.com':
                return True
            else:
                return False


    column_excluded_list = ['password_hash']
    form_excluded_columns = ['services', 'password_hash']

    def create_form(self):
        form = AddEmployee()
        return form
    
    def edit_form(self, obj=None):
        form = EditEmployee()
        
        if form.validate_on_submit():
            return form
        
        form.employeeid.data = obj.employeeid
        form.firstname.data = obj.firstname
        form.lastname.data = obj.lastname
        form.email.data = obj.email
        
        return form
    

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password_hash = generate_password_hash(form.password.data)
        else:
            if form.password.data is not None:
                model.password_hash = generate_password_hash(form.password.data)
        return super().on_model_change(form, model, is_created)


class EquipmentView(ModelView):

    def is_accessible(self):
        if current_user.is_anonymous:
            return False
        else:
            if current_user.email == 'admin@admin.com':
                return True
            else:
                return False


    form_excluded_columns = ['services']

    def create_form(self):
        form = AddEquipment()
        return form

    def edit_form(self, obj=None):
        form = EditEquipment()
        if form.validate_on_submit():
            return form
        
        form.description.data = obj.description
        form.location.data = obj.location
        return form


