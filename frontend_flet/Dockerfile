FROM python:3.10-alpine as base

WORKDIR /frontend_flet

COPY . /frontend_flet

RUN pip install poetry

RUN poetry lock

RUN poetry install

EXPOSE 8080

CMD ["poetry", "run", "python", "./main.py", "--recursive"]