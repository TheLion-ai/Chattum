<!--
Hey, thanks for using the awesome-readme-template template.
If you have any enhancements, then fork this project and create a pull request
or just open an issue with the label "enhancement".

Don't forget to give this project a star for additional support ;)
Maybe you can mention me or this repo in the acknowledgements too
-->
<div align="center">

  <img src="frontend/img/logo.png" alt="logo" width="300" height="auto" />
  <h1>Chattum</h1>

  <p>
    Open-source bot platform based on Large Language Models
  </p>


<!-- Badges -->
<p>
  <a href="https://github.com/TheLion-ai/Chattum/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/TheLion-ai/Chattum" alt="contributors" />
  </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/TheLion-ai/Chattum" alt="last update" />
  </a>
  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
    <img src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg" alt="license" />
  </a>

</p>

<h4>
    <a href="https://www.youtube.com/watch?v=BuqH4uodK54">View Demo</a>
  <span> · </span>
    <a href="https://github.com/TheLion-ai/Chattum/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/TheLion-ai/Chattum/issues/">Request Feature</a>
  </h4>
</div>

<br />

<!-- Table of Contents -->


<!-- About the Project -->
## 🤩 About the Project
```
Warning: This project is currently in alpha stage and may be subject to major changes
```

<!-- Screenshots -->
### :camera: Demo



https://github.com/TheLion-ai/Chattum/assets/12778421/93dbf48e-9f03-47ed-9a0b-ac9899fedb3a



<!-- TechStack -->
### :space_invader: Tech Stack

<details>
  <summary>Frontend</summary>
  <ul>
    <li><a href="https://streamlit.io/">Streamlit</a></li>
  </ul>
</details>

<details>
  <summary>Backend</summary>
  <ul>
    <li><a href="https://www.python.org/">Python</a></li>
    <li><a href="https://python.langchain.com/">Langchain</a></li>
    <li><a href="https://fastapi.tiangolo.com/">FastAPI</a></li>
  </ul>
</details>

<details>
<summary>Database</summary>
  <ul>
    <li><a href="https://www.mongodb.com/">MongoDB</a></li>
  </ul>
</details>

<details>
<summary>DevOps</summary>
  <ul>
    <li><a href="https://www.docker.com/">Docker</a></li>
  </ul>
</details>


<!-- Getting Started -->
# 	:toolbox: Getting Started

<!-- Prerequisites -->
## :bangbang: Prerequisites

* docker
* OpenAI api key
<!-- Installation -->

## Standalone deployment
<!-- Env Variables -->
### :key: Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file
```bash
MONGODB_URL = mongodb://<mongo_username>:<mongo_pass>@mongo:27017 #based on following
MONGO_INITDB_ROOT_PASSWORD = <mongo_username> #choose anything
MONGO_INITDB_ROOT_USERNAME = <mongo_pass> #choose anything

S3_ENDPOINT = 'http://minio:9000'
S3_BUCKET = <bucket_name> #choose anything e.g "chattum"
S3_ACCESS_KEY = <s3_access_key> #choose anything
S3_SECRET_KEY= <s3_access_key> #choose anything

OPENAI_API_KEY = <your_api_key> #for embeddings
API_KEY = <api_key> "choose anything, used for API protection"

```
### :gear: Running the aplication

Run the app using docker-compose

```bash
docker-compose --env-file .env --profile standalone up
```
To visit the FastAPI documentation of the resulting service, visit`` http://localhost:8000/docs`` with a web browser.

To access the UI, visit `http://localhost:8501`.

Logs can be inspected via:
```bash
docker-compose logs
```
## Using external mongo datastabse
### :key: Environment Variables

set your connection string in the env `.env` file
```bash
MONGODB_URL = <your_mongo_uri>
```
You can skip
`MONGO_INITDB_ROOT_PASSWORD` and `MONGO_INITDB_ROOT_USERNAME`as those variables are only important for mongo container that we will not hese


### :gear: Running the aplication

Run the app using docker-compose

```bash
docker-compose --env-file .env --profile minio up
```

## Using external s3 compatible service
### :key: Environment Variables


set your s3 creditionals string in the `.env` file
```bash
S3_ENDPOINT = <s3_endpoint> #your s3 endpoint
S3_BUCKET = <bucket_name> # your bucket name
S3_ACCESS_KEY = <s3_access_key> #your access key id
S3_SECRET_KEY= <s3_access_key> #your secret access key

```
### :gear: Running the aplication

Run the app using docker-compose

```bash
docker-compose --env-file .env --profile mongo up
```
## Using both exteral mongo database and s3 service
### :key: Environment Variables
Set your env variables for both s3 and mongo as described above
### :gear: Running the aplication

Run the app using docker-compose

```bash
docker-compose --env-file .env up
```


## :compass: Roadmap

* [x] Sources
* [x] Chat
* [x] Conversation browsing
* [x] Dynamic APIs
* [ ] Tools
* [ ] Users management
* [ ] Variables in prompts
* [ ] Embedd chat on website
* [ ] Custom language models

<!-- Contributing -->
## :wave: Contributors

<a href="https://github.com/TheLion-ai/Chattum/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=TheLion-ai/Chattum" />
</a>


Contributions are always welcome!




<!-- Contact -->
## :handshake: Contact

[Aleksander Obuchowski](https://www.linkedin.com/in/aleksander-obuchowski/)

[TheLion.AI](https://www.linkedin.com/company/53394525/)




# Development
## Pre-commits
Install pre-commits
https://pre-commit.com/#installation

If you are using VS-code install the extention https://marketplace.visualstudio.com/items?itemName=MarkLarah.pre-commit-vscode

To make a dry-run of the pre-commits to see if your code passes run
```
pre-commit run --all-files
```


## Adding python packages
Dependencies are handeled by `poetry` framework, to add new dependency run
```
poetry add <package_name>
```
inside the `/frontend`  or `/backend` directory

## Debugging

To modify and debug the app, [development in containers](https://davidefiocco.github.io/debugging-containers-with-vs-code) can be useful .

## Testing
```bash
run_tests.sh
```

## Running the aplication without docker

### Frontend

Modify the `BACKEND_URL` variable in `constants.py` to `localhost:5000`

```bash
cd frontend

poetry install

poetry run poetry run streamlit run ui.py
```
### Backend

```bash
cd backend

poetry install

poetry poetry run uvicorn api:app --host 0.0.0.0 --port 5000 --reload
```
