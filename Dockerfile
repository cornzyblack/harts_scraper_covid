FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
ENV PYTHONPATH "/usr/src/app/:/usr/src/utils/"

WORKDIR /src
COPY ./app ./utils /src
