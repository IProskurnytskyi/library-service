# Library Service

Library API service system for creating and borrowing books written on DRF

## Installing using GitHub
Python3 must be already installed

```shell
git clone https://github.com/IProskurnytskyi/library-service
cd library-service
git checkout -b develop
python -m venv venv
if macOS: source venv/bin/activate
if Windows: venv\Scripts\activate.bat
pip install -r requirements.txt
Copy .env.sample > .env and populate with all required data
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Getting access
* create user via /api/users/register
* get access token via /api/users/token
* look for documentation via /api/doc/swagger
* admin panel via /admin
* return a book via /api/books/{id}/return

## Features
* Managing books and borrowings
* JWT Authentication
* New permission classes
* Using email instead of username
* Throttling
* API documentation
* Tests
* Filtering

# Contributing

If you'd like to contribute, please fork the repository and use a develop branch. 
Pull requests are warmly welcome.
