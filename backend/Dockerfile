# base image
FROM python:3.8-slim-buster

# install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# working directory
WORKDIR /backend

# virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# add and install requirements
RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install -r req.txt
COPY . /backend/
CMD ["alembic revision --autogenerate -m "First commit""]