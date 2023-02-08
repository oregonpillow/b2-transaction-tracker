FROM python:3.9-bullseye

COPY ./b2-transaction-tracker /b2-transaction-tracker
COPY ./requirements.txt /b2-transaction-tracker
WORKDIR /b2-transaction-tracker

RUN pip install --no-cache-dir -r requirements.txt && \
  chmod -R +x /b2-transaction-tracker


ENTRYPOINT ["/usr/local/bin/python","/b2-transaction-tracker/run.py"]

