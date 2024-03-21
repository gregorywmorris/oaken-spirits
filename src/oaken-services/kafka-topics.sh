# Create Kafka topics
kafka-topics.sh --create --topic mysql --bootstrap-server kafka1:9092 --replication-factor 1 --partitions 1
kafka-topics.sh --create --topic invoices --bootstrap-server kafka1:9092 --replication-factor 1 --partitions 1
kafka-topics.sh --create --topic shipping --bootstrap-server kafka1:9092 --replication-factor 1 --partitions 1