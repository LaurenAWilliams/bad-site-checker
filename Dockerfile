FROM python:3.7.7

MAINTAINER Lauren Williams "laurenwilliamssoftwareeengineer@gmail.com"

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]

CMD ["bad_site_checker/app.py"]