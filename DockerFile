FROM node:19 as builder 

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ENV PORT=8080

EXPOSE 8080

RUN echo "variable value is $port"

CMD ["python", "start"]