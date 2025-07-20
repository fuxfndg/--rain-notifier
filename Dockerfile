FROM selenium/standalone-chrome:114.0

USER root
WORKDIR /app

COPY requirements.txt .

RUN apt update && \
    apt install -y python3 python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "rain_pinger.py"]