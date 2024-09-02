FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements-dev.txt

EXPOSE 50010

ENV FLASK_APP=app.app

CMD ["flask", "run", "--host=0.0.0.0", "--port=50010"]

LABEL Name="WebApp" \
      Version="1.0"

ENV DB_HOST=postgres
ENV DB_NAME=mydatabase
ENV DB_USER=myuser
ENV DB_PASSWORD=mypassword
