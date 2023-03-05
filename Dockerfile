FROM ubuntu:jammy

COPY ./b2-transaction-tracker /b2-transaction-tracker
COPY ./requirements.txt /b2-transaction-tracker
WORKDIR /b2-transaction-tracker


RUN apt-get update && apt-get install libmariadb-dev python3 python3-pip -y && \
  pip install --no-cache-dir -r requirements.txt && \
  chmod -R +x /b2-transaction-tracker


ENTRYPOINT ["/usr/bin/python3","/b2-transaction-tracker/run.py"]

