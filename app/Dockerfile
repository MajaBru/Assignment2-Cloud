
FROM python:3

WORKDIR /app

COPY . /app

RUN pip install  -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000


CMD ["python", "app.py"]