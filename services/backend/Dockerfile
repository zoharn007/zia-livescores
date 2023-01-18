FROM python:3.9-slim-bullseye
WORKDIR /app
ENV APP_PATH=/app/services/backend
COPY . $APP_PATH
RUN apt-get update && apt-get install -y awscli
RUN pip install -r $APP_PATH/requirements.txt

CMD ["python3", "/app/services/backend/Backend.py"]