FROM python:3.11-alpine3.17
ENV PYTHONUNBUFFERED 1

RUN mkdir /notificator
WORKDIR /notificator

COPY . .

RUN pip install --upgrade pip; \
    pip install -r /notificator/requirements.txt; \
    python manage.py migrate; \
    python manage.py createsuperuser --noinput --username=$ADMIN_USERNAME --email=$ADMIN_MAIL --password=$ADMIN_PASSWORD; \
    adduser --disabled-password service-user

USER service-user

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
