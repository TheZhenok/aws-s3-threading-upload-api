FROM python:3.11.2-buster

WORKDIR /app

ADD ./tools/requirements/base.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app

EXPOSE 8080

CMD ["python3", "app.py"]