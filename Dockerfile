FROM python:3.12.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /home/

RUN sh -c 'apt-get update  -y  && apt-get install build-essential curl python3-dev musl-dev git -y && apt-get clean -y'

COPY Pipfile* /home/

RUN git config --global http.sslverify false

RUN pip install --upgrade pip

RUN pip install pipenv 

RUN pipenv install --system

COPY . /home/

USER root

EXPOSE 5001

ENTRYPOINT ["python", "-m", "main"]