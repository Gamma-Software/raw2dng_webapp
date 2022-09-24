FROM docker:dind
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /app

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install psycopg2-binary tzdata

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt
RUN pip3 install docker
COPY . /app/
#RUN /bin/sh project/setup_server.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]