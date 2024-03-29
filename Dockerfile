FROM python:3.9.16-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./ .

RUN pip install -r requirements.txt

CMD ["/bin/sh", "-c", "python manage.py runserver 0.0.0.0:8000"]