FROM ubuntu:latest
MAINTAINER tomas
EXPOSE 5000
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev build-essential && \
    pip3 install --upgrade pip && \
    apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /app
ENTRYPOINT ["python3"]
CMD ["src/app.py"]
