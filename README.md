# SEED_SCHOOL BACKEND

## Prerequirement

#### Docker & Docker-Compose
>Link for Ubuntu: https://docs.docker.com/engine/install/ubuntu/

>Link for Window: https://docs.docker.com/desktop/windows/install/

>Link to install Docker-Compose: https://docs.docker.com/compose/install/

#### Virtualenv

> pip install virtualenv

#### Python 3

#### POSTMAN

## Install Environment
**Step 1: Clone this respository**

>git clone <respository_link>

>cd Back_Seed

**Step 2: Init virtual environment for python**

>python3 -m venv env

>source env/bin/activate

**Step 3: Run docker-compose file to init Database**

>docker-compose up -d

>docker ps 

#### Run Back_End Server
> make install

> make migrate

> make migrations

> make run

### API

**Import file in POSTMAN: Seed_School.postman_collection.json
