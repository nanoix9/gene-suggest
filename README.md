# Get Started

This service provides a single RESTful endpoint `/gene_suggest`, which accepts three params: 
species, query, and limit, and return a "limit"-length list of suggested gene names, belonged 
to "species", having the prefix of "query", and sorted in alphabetic order.

This project is tested under Python 3.6.8

## Run Locally

1. create & active a virtualenv(optional but recommended): 

    `virtualenv --python=/usr/bin/python3.6 venv`

    `. venv/bin/activate`

3. install dependencies: `pip install -r requirements.txt`

4. run tests(optional): `python -m pytest` 

5. start service: `gunicorn --bind 0.0.0.0:9000 run:app`

## Run with Docker Compose

If you have Docker & Docker Compose installed, you can run it easily:

`docker-compose up`

## Use the Service

Example: `curl 'http://localhost:9000/gene_suggest?species=homo_sapiens&query=abc&limit=10'`

Sample response:

["ABCA1","ABCA10","ABCA11P","ABCA12","ABCA13","ABCA17P","ABCA2","ABCA3","ABCA4","ABCA5"]

## Deployment

> Describe how would you deploy your web service. How would you ensure your solution can scale to meet increased demand?

This service can be deployed with gunicorn, with an nginx in front of it serving as port forwarding 
and load balancing. However, I would strongly prefer to deloy it with Docker, which is a much more
easier way for environment and dependency management. 

In terms of scalability, since this service is stateless, it can be easily scaled horizontally. 
However, the database would be the bottleneck. To tackle this, I have some proposals below:

1. Introduce slave DB and increase the number of copies. This service only read from DB instead of 
    modifying it, so there will be no consistency issue.

2. Incorporate an cache layer, such as Memcached or Redis, to improve the speed of data accessing.

3. Introduce advanced data structure, such as Trie tree, or prefix hashing table, which will significantly
    speeding up the searching. As we are only searching for one species, we can build separated Trie trees
    or prefix hashing tables for each species. As shown by simple query, the number of genes for one species
    is roughly 10k+, which can be fit into memory without difficulty.

## Testing

> What strategies would you employ to test your application? How would you automate testing?

I am using `pytest` as unit test framework in this project, which is easy-to-use. I have already setup
automatic testing which can be executed by a single command. Moreover, integration testing can also be 
introduced, in which we will have a real deployed service and send testing requests to it. Powered by
Docker, HTTP tools/libraries(e.g. curl, Python's request) and testing framework, this approach would be 
feasible and useful. In detail, we can setup a Docker image for service, and another image to run our
integration test script. 
