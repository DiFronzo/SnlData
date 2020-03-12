FROM ubuntu:18.04
FROM python:3.7

MAINTAINER DiFronzo <root@vfiles.no>

ENV LC_ALL C.UTF-8

RUN apt-get update

COPY /snldata /src

WORKDIR /src

RUN pip3 install -r /src/requirements.txt

CMD python3 setup.py
