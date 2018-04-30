Starfish
=====
Starfish was originally written for Django 1.5 in Python 2, since this version is not secure anymore the project needed to be made compatible with a newer version of Django (Django 2.0). The readme file will be kept up to date as the project advances through the update. If for some reason the project needs to be compatible with django x.x.x one can find the dependancies/instructions etc for that version. At the moment of this commit the project is written for Django 1.7.

&copy; ICTO FNWI


## Dependencies
This system is written in Python 2.7.10 using Django 1.7 and requires PostgreSQL 10.3 or higher.
Python dependencies are listed in `requirements.txt`, which also will be updated if the project supports a new version of Django.

## Getting started

### Database
Make sure that PostgreSQL is installed and running and that a database with user is set up. A good guide how to do this can be found [here](https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/content/optional_postgresql_installation/) (NOTE: stop before the 'Update settings' part).

### Python version
Make sure you're using Python 2.7.10 You are strongly encouraged to use a [virtual environment](https://virtualenv.pypa.io/en/stable/).


```shell
$ virtualenv venv --python=python2.7.10
$ source venv/bin/activate
```

Now install dependencies:

```shell
(venv) $ pip install -r requirements.txt
```

### Settings
In this project there is a example settings file which in this case is not sufficient to run the project locally without a hassle.
#TODO create proper settings file which uses get_secret

### Check, double check
To make sure everything is set up and configured well, run:

```shell
(venv) $ ./manage.py check
```


### Create and run migrations
Now that everything is setup, we can set up the datastructures.
```shell
(venv) $ ./manage.py migrate
```

### Create a superuser
In order to use the admin site, you'll need a superuser account.
```shell
(venv) $ ./manage.py createsuperuser
```

### Run development server
You are now ready to run the development server:

```shell
(venv) $ ./manage.py runserver
```

### Using your user account...
To use your user account, first login to the admin page and create a person for
the user.

## Maintaining database migrations
Every time fields in any of the models change, a [database migration](https://docs.djangoproject.com/en/1.11/topics/migrations/)
needs to be created and applied. The first documents a database change and its
inverse, the second actually changes the database.

Make sure to commit the migration to GIT after applying it, so other developers
can use them.

```shell
(venv) $ ./manage.py makemigration
(venv) $ ./manage.py migrate
```

