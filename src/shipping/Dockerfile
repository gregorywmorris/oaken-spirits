FROM python:3.11

ENV KAFKA_SERVER "your_kafka_server"
ENV INVOICES_TOPIC "invoices"
ENV SHIPPING_TOPIC "shipping"
ENV MYSQL_HOST "your_mysql_host"
ENV MYSQL_USER "your_mysql_user"
ENV MYSQL_PASSWORD "your_mysql_password"
ENV MYSQL_DATABASE "your_mysql_database"

RUN pip install kafka-python mysql-connector-python

COPY . /app

WORKDIR /app

CMD ["python", "shipping.py"]
