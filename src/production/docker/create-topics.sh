#!/bin/bash

# Wait for Kafka to start
sleep 10

# Create topics using Kafka topic creation command
kafka-topics --create --bootstrap-server kafka1:19092,kafka2:19093,kafka3:19094,kafka1:9092,kafka2:9093,kafka3:9094 --replication-factor 3 --partitions 3 --topic mysql
kafka-topics --create --bootstrap-server kafka1:19092,kafka2:19093,kafka3:19094,kafka1:9092,kafka2:9093,kafka3:9094 --replication-factor 3 --partitions 3 --topic invoices
kafka-topics --create --bootstrap-server kafka1:19092,kafka2:19093,kafka3:19094,kafka1:9092,kafka2:9093,kafka3:9094 --replication-factor 3 --partitions 3 --topic shipping
