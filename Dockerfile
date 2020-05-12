FROM python:3.8.1-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Prevent Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1

# Prevent Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python manage.py run -h 0.0.0.0


