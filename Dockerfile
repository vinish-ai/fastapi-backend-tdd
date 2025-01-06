FROM python:3.12.8-slim-bookworm

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install netcat-traditional gcc postgresql \
  && apt-get clean

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY ./scripts/entrypoint.sh .
RUN chmod +x /usr/src/app/scripts/entrypoint.sh

ENTRYPOINT ["/usr/src/app/scripts/entrypoint.sh"]