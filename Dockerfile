FROM selenium/standalone-chrome:latest

USER root
WORKDIR /app

# Спочатку копіюємо тільки dependencies-файл
COPY requirements.txt .

# Встановлюємо Python, pip та залежності
RUN apt update && \
    apt install -y python3 python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Тепер копіюємо весь код
COPY . .

# Стартова команда
CMD ["python3", "rain_pinger.py"]