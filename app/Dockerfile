
FROM python:3.8-alpine

WORKDIR /app

COPY . /app

COPY front-end/index.html /app/front-end/index.html

RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000


CMD ["python", "app.py"]