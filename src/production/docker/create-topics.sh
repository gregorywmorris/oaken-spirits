#!/bin/bash

# Wait for Kafka to start
sleep 10

# Create topics using Kafka topic creation command
kafka-topics --create --bootstrap-server kafka1:9092,${DOCKER_HOST_IP:-127.0.0.1}:19092 --replication-factor 1 --partitions 3 --topic mysql
kafka-topics --create --bootstrap-server kafka1:9092,${DOCKER_HOST_IP:-127.0.0.1}:19092 --replication-factor 1 --partitions 3 --topic invoices
kafka-topics --create --bootstrap-server kafka1:9092,${DOCKER_HOST_IP:-127.0.0.1}:19092 --replication-factor 1 --partitions 3 --topic shipping