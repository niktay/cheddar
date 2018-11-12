FROM python:3.7.0-alpine

LABEL Name=cheddar
EXPOSE 80

WORKDIR /app
ADD . /app


RUN python3 -m pip install pipenv
RUN apk add git
RUN pipenv install --dev --ignore-pipfile
# CMD ["pipenv", "run", "python3", "-u", "manage.py", "runserver", "0.0.0.0:80"]
