FROM python:2.7.13

MAINTAINER Thomas Kroes "t.kroes@lumc.nl"

WORKDIR /flask

ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

CMD ["python", "app.py"]
