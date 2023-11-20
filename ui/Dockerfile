FROM python:3.11 as base

WORKDIR /ui

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

COPY . /ui
COPY .web /ui/.web

RUN pip install poetry

RUN poetry lock

RUN poetry install


# RUN mkdir /streamlit

# COPY requirements.txt /streamlit

# WORKDIR /streamlit

# RUN pip install -r requirements.txt

# COPY . /streamlit
# RUN poetry shell
RUN poetry run reflex init
CMD poetry run reflex run
