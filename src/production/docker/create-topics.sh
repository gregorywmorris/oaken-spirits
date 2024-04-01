#!/bin/bash

# Wait for Kafka to start
sleep 10

# Create topics using Kafka topic creation command
kafka-topics --create --zookeeper zoo1:2181 --replication-factor 3 --partitions 3 --topic mysql
kafka-topics --create --zookeeper zoo1:2181 --replication-factor 3 --partitions 3 --topic invoices
kafka-topics --create --zookeeper zoo1:2181 --replication-factor 3 --partitions 3 --topic shipping