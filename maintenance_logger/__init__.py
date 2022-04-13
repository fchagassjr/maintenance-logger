import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager, current_user


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


from maintenance_logger.administration import EmployeeView, EquipmentView
from maintenance_logger.models import Employee, Equipment
from maintenance_logger.employee import bp_employees


admin = Admin(app,name='Admin Page',template_mode='bootstrap3')

admin.add_view(EmployeeView(Employee, db.session))
admin.add_view(EquipmentView(Equipment, db.session))

app.register_blueprint(bp_employees)

administrator = Employee.query.filter_by(email='admin@admin.com').first()
if administrator is None:
    administrator = Employee(0000,None,None,'admin@admin.com','admin')
    db.session.add(administrator)
    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')



