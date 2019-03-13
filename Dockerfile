# this is an official Python runtime, used as the parent image
FROM python:3.6.8

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
COPY . /app

# execute everyone's favorite pip command, pip install -r
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# run unit test
RUN python -m pytest

# unblock port for the Flask app to run on
EXPOSE 9000

# execute the Flask app
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9000", "run:app"]
