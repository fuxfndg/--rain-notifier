FROM selenium/standalone-chrome:latest

USER root
WORKDIR /app

RUN apt update && apt install -y python3 python3-pip \
    && pip3 install -r requirements.txt

COPY . .

CMD ["python3", "rain_pinger.py"]