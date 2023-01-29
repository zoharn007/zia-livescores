FROM python:3.11.1-slim-bullseye
WORKDIR /app
ENV APP_PATH=/app/services/backend
COPY . .
RUN apt-get update && apt-get install -y awscli
RUN apt remove -fy libaom0:amd64
RUN pip install -r /app/services/backend/requirements.txt

CMD ["python3", "/app/services/backend/Backend.py"]