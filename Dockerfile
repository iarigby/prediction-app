FROM python:3.10.9-slim as base

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pip install gunicorn

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy

COPY . /usr/src/app
RUN useradd -m appUser
RUN chown appUser:appUser /usr/src/app

USER appUser
CMD ["gunicorn", "--bind", ":5050", "app.api:app"]