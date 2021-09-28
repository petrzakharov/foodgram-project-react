FROM python:3.8.5
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
CMD gunicorn recipe.wsgi:application --bind 0.0.0.0:8000