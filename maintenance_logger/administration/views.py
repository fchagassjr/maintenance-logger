import os
from base64 import b64encode
from flask_admin.contrib.sqla import ModelView
from maintenance_logger.administration.forms import AddEmployee, AddEquipment, EditEmployee
from werkzeug.security import generate_password_hash

class EmployeeView(ModelView):

    # column_excluded_list = ['password_hash']
    form_excluded_columns = ['services', 'password_hash']

    def create_form(self):
        form = AddEmployee()
        return form
    
    def edit_form(self, obj=None):
        form = EditEmployee()
        if form.validate_on_submit():
            print('after submit')
            return form
        form.firstname.data = obj.firstname
        form.lastname.data = obj.lastname
        form.email.data = obj.email
        form.hidden_email.data = obj.email
        return form
    

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password_hash = generate_password_hash(form.password.data)
        else:
            if form.password.data is not None:
                model.password_hash = generate_password_hash(form.password.data)
        return super().on_model_change(form, model, is_created)

class EquipmentView(ModelView):
    def create_form(self):
        form = AddEquipment()
        return form