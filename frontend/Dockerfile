FROM python:3.10-buster as base

WORKDIR /frontend

COPY . /frontend

RUN pip install poetry

RUN poetry install


# RUN mkdir /streamlit

# COPY requirements.txt /streamlit

# WORKDIR /streamlit

# RUN pip install -r requirements.txt

# COPY . /streamlit

EXPOSE 8501

CMD poetry run streamlit run ui.py