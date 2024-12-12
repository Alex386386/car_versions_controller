FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

COPY .. .

CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --no-input && gunicorn src.wsgi:application --bind 0.0.0.0:8000 --access-logfile - --error-logfile -"]
