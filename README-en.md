Admin Express Project
==============
An Admin console and business management application system for fast development and common usage.

Why would wheels be invented again?
The main purpose is to satisfy the requirements from the start-up teams and other small groups in company.

Mainly integrated frameworks list as follows:

 - Flask-Admin v1.6.0，fast-dev web framework, based on Flask and Bootstrap
 - AdminLTE v2.4.18，web-front js framework, based on jQuery + Bootstrap3
 - Flask 2.2.2，the most popular python web micro-framework.

## How to run?

### 1. Initialize the project
Open a shell under root directory of the local project, and activate the python environment 
with virtualenv or conda env. And then, tell flask where to find the app:
```shell
export FLASK_APP=manage.py
```
If under Windows cmd, just use set-command instead:
```shell
set FLASK_APP=manage.py
```

### 2. auto-initialize the database
```shell
flask db init
flask db migrate
flask db upgrade

# auto-create the admin account
flask account-init
```

### 3. start to run
you can run directly in the command window, or you can configure and run in Pycharm(strongly recommended).
```shell
flask run
```

The default administrator's account: admin/Abcd@1234, login the system and enjoy!

## Contribution

1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request