FROM python:3.9-slim-bullseye
WORKDIR /app
ENV APP_PATH=/app/services/repeater
COPY . .

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r /app/services/repeaterrequirements.txt

CMD ["python3", "/app/services/repeaterrepeater.py"]