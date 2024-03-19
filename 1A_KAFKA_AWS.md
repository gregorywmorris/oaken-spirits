# Kafka EC2 Set up

## 1 Create Instance

1. Edit security to allow traffic
1. `sudo apt-get update`
1. `sudo apt-get install net-tools`

## 2 Install and Configure Kaka

1. SSH into instance
1. Install Kafka
    -`wget https://downloads.apache.org/kafka/3.7.0/kafka_2.12-3.7.0.tgz`
    - `tar -xvf kafka_2.12-3.7.0.tgz`
1. Install java
    - For Ubuntu
    1. `sudo sudo apt install default-jre`
    1. `sudo vi /etc/profile.d/jdk11.sh`
        - Enter the following:

        ```bash
        # create new
        export JAVA_HOME="/usr/lib/jvm/java-1.11.0-openjdk-amd64"
        export PATH=$PATH:$JAVA_HOME/bin
        export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"
        ```

    - See top answer here for [heap explanation](https://stackoverflow.com/questions/21448907/kafka-8-and-memory-there-is-insufficient-memory-for-the-java-runtime-environme)
1. `source /etc/profile.d/jdk11.sh`
1. `java --version`
1. `echo JAVA_HOME`

1. kafka is pointing to private server IP, change server.properties so that it can run in public IP. Update advertized.listeners to be active (remove '#' with current host name.
1. `sudo vi kafka_2.12-3.7.0/config/server.properties`

    ```bash
    advertised.listeners=PLAINTEXT://<Enter Public IP Here>:9092
    ```

## 3 Start Zoo-keeper

1. SSh into instance in a new window
1. `kafka_2.12-3.7.0/bin/zookeeper-server-start.sh kafka_2.12-3.7.0/config/zookeeper.properties`

## 4 Start Kafka-server

1. SSh into instance in a new window
1. `kafka_2.12-3.7.0/bin/kafka-server-start.sh kafka_2.12-3.7.0/config/server.properties`

## 5 Create the topic

1. SSh into instance in a new window
1. `kafka_2.12-3.7.0/bin/kafka-topics.sh --create --topic invoices --bootstrap-server <Enter Public IP Here>:9092 --replication-factor 1 --partitions 1`
1. `kafka_2.12-3.7.0/bin/kafka-topics.sh --create --topic shipping --bootstrap-server <Enter Public IP Here>:9092 --replication-factor 1 --partitions 1`
