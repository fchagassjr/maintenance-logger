# Maintenance Logger

## A Flask application to manage your maintenance related database

## Installation

It's highly recommended to create a virtual enviroment before proceding.
Install all the required libraries using pip:

```
$ pip install -r requirements.txt
```


## Application Structure 
```
maintenance-logger
|
|--flask_app.py
|
|--maintenance_logger
|  |
|  |--__init__.py
|  |--data.sqlite
|  |--models.py
|  |
|  |--templates
|  |  |
|  |  |--index.html
|  |  |--base.html
|  |
|  |--administration
|  |  |
|  |  |--__init__.py
|  |  |--forms.py
|  |   
|  |  
|  |--employee
|     |
|     |--__init__.py
|     |--forms.py
|     |--templates
|        |
|        |--database.html
|        |--login_employee.html
|        |--add_service.html
|
|--migrations  

```


## Flask Configuration

First of all set your Flask app variable 

MacOS/Linux users run:
```
$ export FLASK_APP=flask_ap.py
```

Windows Users need to run:
```
$ set FLASK_APP=flask_app.py
```

After set the application, initialize the data base and migrate
```
$ flask db init
$ flask db migrate -m "first commit"
$ flask db upgrade
```

## Start the application

To start your application 
```
$ flask run
```
The application should start at http://127.0.0.1:5000/


## Levels of access

Main pages will be accessible to regular user, but when the application starts for the first time, the user admin is created.
```
email: admin@admin.com
password: admin
```
By typing http://127.0.0.1:5000/admin on the browser, administrative level is accessed
