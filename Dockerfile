FROM ubuntu:18.04

MAINTAINER Lauren Williams "laurenwilliamssoftwareeengineer@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

EXPOSE 5000

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]

CMD ["url_lookup_service/app.py"]