# django-quiz
Django Quiz App

## Running the project locally

Clone the repository to your local machine:

```bash
git clone https://github.com/dmanojlo/django-quiz.git
```

Create your own virtual environment
```bash
py -m venv project-name
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Apply the migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create new superuser
```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```



The project will be available at **127.0.0.1:8000**.
