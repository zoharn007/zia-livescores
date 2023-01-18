FROM python:3.9-slim-bullseye
WORKDIR /app
#ENV APP_PATH="C:\Final_Project\services\backend"
ENV APP_PATH=services/backend
COPY . .
RUN apt-get update && apt-get install -y awscli
RUN pip install -r requirements.txt
CMD ["python3", "Backend.py"]