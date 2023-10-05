FROM ubuntu:latest

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install python3.9 python3-pip \
    curl

RUN pip3 install dash plotly pandas pytest

WORKDIR /app

COPY . /app

ENV PATH="/usr/bin/:${PATH}"
ENV PYTHONPATH="/usr/bin/python3"

EXPOSE 8050

CMD ["python3", "app.py"]