# Get Started

## Run Locally

1. create a virtualenv(recommend): `virtualenv --python=/usr/bin/python3.6 venv`
2. active virtualenv: `. venv/bin/activate`
3. install dependencies: `pip install -r requirements.txt`
4. run tests(optional): `python -m pytest` 
5. start service: `gunicorn --bind 0.0.0.0:9000 run:app`

## Run with Docker Compose

`docker-compose up`

## Use the Service

Example: `curl 'http://localhost:9000/gene_suggest?species=homo_sapiens&query=abc&limit=10'`

Sample output:

["ABCA1","ABCA10","ABCA11P","ABCA12","ABCA13","ABCA17P","ABCA2","ABCA3","ABCA4","ABCA5"]

