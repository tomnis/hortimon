FROM balenalib/raspberry-pi:buster
MAINTAINER tomas

# install libs
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y \
      python3-pkg-resources \
      python3-dev \
      python3-pip && \
    pip3 install --upgrade pip && \
    apt-get clean

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY src /app

CMD [ "python3", "-u", "exhaust_fan.py", "-e",  "tent", "-p", "exhaust_fan", "--max-temperature", "74" ]
