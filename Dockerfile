FROM python:3.7.0-alpine

LABEL Name=cheddar
EXPOSE 8000

WORKDIR /app
ADD cheddar/ /app
ADD Pipfile.lock /app/Pipfile.lock
ADD Pipfile /app/Pipfile

RUN python3 -m pip install pipenv
RUN pipenv install --ignore-pipfile
CMD ["pipenv", "run", "python3", "-u", "manage.py", "runserver", "0.0.0.0:80"]
