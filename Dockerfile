FROM python:3.13

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/app

RUN python -m pip install --upgrade pipenv wheel
RUN python -m pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --dev --system

COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

COPY . .
