FROM python:3.10

WORKDIR /app/

COPY ./deploy/workers/requirements.txt ./deploy/workers/entrypoint.sh /

RUN pip install -r /requirements.txt

COPY . ./