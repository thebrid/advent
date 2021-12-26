FROM python:3.10

COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install -r /tmp/requirements.txt