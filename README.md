# Get Started

This project is tested under Python 3.6.8

## Run Locally

1. create & active a virtualenv(optional but recommended): 

    `virtualenv --python=/usr/bin/python3.6 venv`

    `. venv/bin/activate`

3. install dependencies: `pip install -r requirements.txt`

4. run tests(optional): `python -m pytest` 

5. start service: `gunicorn --bind 0.0.0.0:9000 run:app`

## Run with Docker Compose

`docker-compose up`

## Use the Service

Example: `curl 'http://localhost:9000/gene_suggest?species=homo_sapiens&query=abc&limit=10'`

Sample response:

["ABCA1","ABCA10","ABCA11P","ABCA12","ABCA13","ABCA17P","ABCA2","ABCA3","ABCA4","ABCA5"]

## Deployment

> Describe how would you deploy your web service. How would you ensure your solution can scale to meet increased demand?

## Testing

> What strategies would you employ to test your application? How would you automate testing?
