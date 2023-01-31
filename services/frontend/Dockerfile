FROM python:3.11.1-slim-bullseye
WORKDIR /app
ENV APP_PATH=/app/services/frontend
COPY . .
RUN apt-get update
RUN apt remove -fy libaom0:amd64
RUN pip install -r /app/services/frontend/requirements.txt

CMD ["python3", "/app/services/frontend/frontend.py"]