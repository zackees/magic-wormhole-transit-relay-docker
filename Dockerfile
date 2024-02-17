FROM python:3.10.13-bullseye
EXPOSE 4001/tcp
RUN python3 -venv tr-venv
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN tr-venv/bin/pip install magic-wormhole-transit-relay
CMD ["tr-venv/bin/twist", "transitrelay", "--port=tcp:4001"]


