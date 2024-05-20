
FROM python:3.8-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000
EXPOSE 8080


CMD ["python", "app.py"]