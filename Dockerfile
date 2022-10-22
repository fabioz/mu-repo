FROM python:3.7-slim

RUN apt update && \
    apt install --yes git

RUN python3.7 -m pip install pytest
