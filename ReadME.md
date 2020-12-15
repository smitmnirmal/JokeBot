## Knock Knock chat bot

### To run the project:

- Clone this repo
- Create virtual environment (Windows)
```
python -m venv env
```
- Install requirements
```
python -m pip install requirements.txt
```
- Create migrations
```
python manage.py makemigrations chatbot
```
- Perform sql migrations
```
python manage.py sqlmigrate chatbot 0001
```
- Migrate the app
```
python manage.py migrate
```
- Run app
```
python manage.py runserver
```

### Visit http://127.0.0.1:8000/