# Chattum

# Requirements

### Prod
* docker
### Dev
* python 3.10
* poetry



# Running the application
Create .env file
```
MONGODB_URL =
```


To run the example in a machine running Docker and docker-compose, run:

    docker-compose build
    docker-compose up

To visit the FastAPI documentation of the resulting service, visit http://localhost:8000/docs with a web browser.
To visit the streamlit UI, visit http://localhost:8501.

Logs can be inspected via:

    docker-compose logs


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
Install https://www.thunderclient.com/
and set thunder-client.saveToWorkspace to true

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



## Deployment

To deploy the app, one option is deployment on Heroku (with [Dockhero](https://elements.heroku.com/addons/dockhero)). To do so:

- rename `docker-compose.yml` to `dockhero-compose.yml`
- create an app (we refer to its name as `<my-app>`) on a Heroku account
- install locally the Heroku CLI, and enable the Dockhero plugin with `heroku plugins:install dockhero`
- add to the app the DockHero add-on (and with a plan allowing enough RAM to run the model!)
- in a command line enter `heroku dh:compose up -d --app <my-app>` to deploy the app
- to find the address of the app on the web, enter `heroku dh:open --app <my-app>`
- to visualize the api, visit the address adding port `8000/docs`, e.g. `http://dockhero-<named-assigned-to-my-app>-12345.dockhero.io:8000/docs`(not `https`)
- visit the address adding `:8501` to visit the streamlit interface
- logs are accessible via `heroku logs -p dockhero --app <my-app>`
