FROM python:3.7-buster

RUN pip install pipenv

COPY . .

RUN pipenv install --deploy --system