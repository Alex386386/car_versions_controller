FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY .. .

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --no-input && gunicorn src.wsgi:application --bind 0.0.0.0:8000 --access-logfile - --error-logfile -"]
