FROM python:3.10-buster as base

WORKDIR /frontend
RUN pip install poetry

COPY pyproject.toml poetry.lock /frontend/

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN pip install -r requirements.txt


COPY . /frontend


CMD streamlit run main.py
