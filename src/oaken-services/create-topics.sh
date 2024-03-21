/bin/kafka-topics --create --topic mysql --bootstrap-server kafka1:9092 --replication-factor 1 --partitions 1
/bin/kafka-topics --create --topic invoices --bootstrap-server kafka1:9092 --replication-factor 1 --partitions 1
/bin/kafka-topics --create --topic shipping --bootstrap-server kafka1:9092 --replication-factor 1 --partitions 1