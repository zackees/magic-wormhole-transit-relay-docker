FROM python:3.10.13-bullseye
RUN apt-get update && apt-get install -y python3-twisted nginx
EXPOSE 80

RUN python3 -m venv tr-venv
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN tr-venv/bin/pip install magic-wormhole-transit-relay
COPY nginx.conf /etc/nginx/nginx.conf
COPY ./entrypoint /entrypoint
CMD ["/bin/bash", "/entrypoint"]


