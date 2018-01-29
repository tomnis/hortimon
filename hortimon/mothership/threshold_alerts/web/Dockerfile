FROM ubuntu:latest
MAINTAINER tomas
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /usr/local/threshold_alerts/web
WORKDIR /usr/local/threshold_alerts/web
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
