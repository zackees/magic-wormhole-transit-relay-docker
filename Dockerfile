FROM ubuntu:18.04
EXPOSE 4001/tcp
RUN apt-get update -y && apt-get install -y \
    python-virtualenv \
    python-pip
RUN virtualenv tr-venv
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN tr-venv/bin/pip install magic-wormhole-transit-relay
CMD ["tr-venv/bin/twist", "transitrelay", "--port=tcp:4001"]


