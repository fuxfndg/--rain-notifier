FROM selenium/standalone-chrome:latest

USER root
WORKDIR /app

# Копіюємо файл з залежностями
COPY requirements.txt .

# Встановлюємо Python, pip і залежності
RUN apt update && \
    apt install -y python3 python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Копіюємо інші файли проекту
COPY . .

# Запускаємо бота
CMD ["python3", "rain_pinger.py"]