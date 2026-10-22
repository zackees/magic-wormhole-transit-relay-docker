# Keep the Python 3.10 runtime line while taking Debian's patched NGINX.
FROM python:3.10-slim-trixie
# Require Debian's DSA-6575-1 fixes, not an unpatched cached distro package.
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3-twisted nginx \
 && dpkg --compare-versions "$(dpkg-query -W -f='${Version}' nginx)" ge "1.26.3-3+deb13u10" \
 && rm -rf /var/lib/apt/lists/*
EXPOSE 80

RUN python3 -m venv tr-venv
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN tr-venv/bin/pip install magic-wormhole-transit-relay
COPY nginx.conf /etc/nginx/nginx.conf
COPY ./entrypoint /entrypoint
CMD ["/bin/bash", "/entrypoint"]


