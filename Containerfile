FROM python:3.10-slim

RUN apt-get update -y && apt-get clean

RUN groupadd devops-map && useradd -g devops-map -m -d /devops-map devops-map

USER devops-map

ADD --chown=devops-map:devops-map ./ /devops-map

RUN pip install --upgrade pip && pip install -r /devops-map/requirements.txt --user

VOLUME /devops-map/data

EXPOSE 5000

WORKDIR /devops-map

ENV FLASK_APP=app.py

ENTRYPOINT [ "python", "app.py", "--host", "0.0.0.0", "--port", "5000" ]

