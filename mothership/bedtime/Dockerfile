FROM ubuntu:16.04
MAINTAINER tomas

EXPOSE 5000

RUN apt-get update -y && \
    apt-get install -y \
      python3-dev \
      python3-pip \
    vim && \
    pip3 install --upgrade pip && \
    apt-get clean

# We copy just the requirements.txt first to better leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app

ENTRYPOINT [ "python3" ]
CMD [ "-u", "src/app.py" ]
