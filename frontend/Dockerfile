FROM python:3.10-buster as requirements-stage

WORKDIR /tmp

RUN pip install poetry==1.6.1

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10-buster

WORKDIR /frontend

COPY --from=requirements-stage /tmp/requirements.txt /frontend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /frontend/requirements.txt

COPY . /frontend

CMD ["streamlit", "run", "🤖_bots.py"]
