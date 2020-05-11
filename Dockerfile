FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements_freeze.txt /app/requirements_freeze.txt

WORKDIR /app

#RUN pip install --upgrade setuptools
RUN pip install -r requirements_freeze.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]