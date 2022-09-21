FROM python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /app

RUN apt update -y
RUN apt install python3-psycopg2 -y
RUN pip install psycopg2-binary

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app/
RUN bash project/setup_server.sh
CMD ["/app/docker-entrypoint.sh"]