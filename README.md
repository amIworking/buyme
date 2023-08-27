# buyme

# Local Run
- create venv with Python 3.10
- install requirements: `pip install requirements.txt`
- run database locally: `docker-compose up -d db`
- apply migrations: `python app/manage.py migrate`
- run server: `python app/manage.py runserver`
- create super user: `python app/manage.py createsuperuser`
- go http://127.0.0.1:8000/admin