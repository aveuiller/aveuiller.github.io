Title: Apache Kafka: Apprentice Cookbook
Slug: kafka_apprentice_cookbook
Date: 2021-06-29
Category: Software Engineering
Tags: Cheat sheet, Kafka
Author: Antoine Veuiller
Summary: Apache Kafka is a distributed event streaming platform built over strong concepts. Let's dive into the possibilities it offers.
-----

### Availability Disclaimer

This article is not yet published anywhere else.
<!--
This article can be found on other sources:

- Medium: [link]()
- Dev.to: [link]()
-->
-----

![Apache Kafka Logo](/images/posts/2021-06-01_Kafka-Apprentice-Cookbook/kafka_logo.png)

Apache Kafka is a distributed event streaming platform built over strong concepts.
Let’s dive into the possibilities it offers.

[Apache Kafka](https://kafka.apache.org/) is a distributed event streaming platform built with an emphasis on reliability,
performance, and customization. Kafka can send and receive messages in a [publish-subscribe](https://aws.amazon.com/pub-sub-messaging/) fashion.
To achieve this, the ecosystem relies on few but strong basic concepts,
which enable the community to build many features solving [numerous use cases](https://kafka.apache.org/uses), for instance:

*   Processing messages as an [Enterprise Service Bus](https://www.confluent.io/blog/apache-kafka-vs-enterprise-service-bus-esb-friends-enemies-or-frenemies/).
*   Tracking Activity, metrics, and telemetries.
*   Processing Streams.
*   Supporting [Event sourcing](https://www.confluent.io/blog/event-sourcing-cqrs-stream-processing-apache-kafka-whats-connection/).
*   Storing logs.

This article will see the concepts backing up Kafka and the different tools available to handle data streams.

## Architecture

The behaviour of Kafka is pretty simple: **Producers** push _Messages_ into a particular _Topic_,
and **Consumers** subscribe to this _Topic_ to fetch and process the _Messages_.
Let’s see how it is achieved by this technology.

### Infrastructure side

Independently of the use, the following components will be deployed:

*   One or more **Producers** sending messages to the brokers.
*   One or more Kafka **Brokers**, the actual messaging server handling communication between producers and consumers.
*   One or more **Consumers** fetching and processing messages, in clusters named **Consumer Groups**.
*   One or more [**Zookeeper**](https://zookeeper.apache.org/) instances managing the brokers.
*   (Optionally) One or more **Registry** instances uniformizing message schema.

As a scalable distributed system, Kafka is heavily relying on the concept of _clusters_.
As a result, on typical production deployment, there will likely be multiple instances of each component.

A **Consumer Group** is a cluster of the same consumer application.
This concept is heavily used by Kafka to balance the load on the applicative side of things.

![Kafka Architecture](/images/posts/2021-06-01_Kafka-Apprentice-Cookbook/kafka_architecture.svg)

_Note: The dependency on Zookeeper will be removed soon, Cf._ [_KIP-500_](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum)

> Further Reading:
>
> [Design & Implementation Documentation](https://kafka.apache.org/documentation/#majordesignelements)
>
> [Kafka Basics and Core Concepts: Explained  — Aritra Das](https://hackernoon.com/kafka-basics-and-core-concepts-explained-dd1434dv)

### Applicative side

A **Message** in Kafka is a `key-value` pair.
Those elements can be anything from an integer to a [Protobuf message](https://developers.google.com/protocol-buffers),
provided the right serializer and deserializer.

The message is sent to a **Topic**, which will store it as a **Log**.
The topic should be a collection of logs semantically related, but without a particular structure imposed.
A topic can either keep every message as a new log entry or only keep the last value for each key
(a.k.a. [Compacted log](https://docs.confluent.io/platform/current/kafka/design.html#log-compaction)).

To take advantage of the multiple brokers, topics are [sharded](https://en.wikipedia.org/wiki/Shard_%28database_architecture%29)
into **Partitions** by default.
Kafka will assign any received message to one partition depending on its key,
or using [a partitioner algorithm](https://www.confluent.io/blog/apache-kafka-producer-improvements-sticky-partitioner) otherwise,
which results in a random assignment from the developer's point of view.
Each partition has a **Leader** responsible for all I/O operations, and **Followers** replicating the data.
A follower will take over the leader role in case of an issue with the current one.

The partition holds the received data in order, increasing an **offset** integer for each message.
However, there is no order guarantee between two partitions.
So for order-dependent data, one must ensure that they end up in the same partition by using the same key.

Each partition is assigned to a specific consumer from the consumer group.
This consumer is the only one fetching messages from this partition.
In case of shutdown of one customer, the brokers will [reassign partitions](https://medium.com/streamthoughts/understanding-kafka-partition-assignment-strategies-and-how-to-write-your-own-custom-assignor-ebeda1fc06f3)
among the customers.

Being an asynchronous system, it can be hard and impactful on the performances to have every message delivered exactly one time to the consumer.
To mitigate this, Kafka provides [different levels of guarantee](https://kafka.apache.org/documentation/#semantics)
on the number of times a message will be processed (_i.e._ at most once, at least once, exactly once).

> Further Reading:
>
> [Log Compacted Topics in Apache Kafka — Seyed Morteza Mousavi](https://towardsdatascience.com/log-compacted-topics-in-apache-kafka-b1aa1e4665a7)
>
> [(Youtube) Apache Kafka 101: Replication — Confluent](https://www.youtube.com/watch?v=Vo6Mv5YPOJU&list=PLa7VYi0yPIH0KbnJQcMv5N9iW8HkZHztH&index=5)
>
> [Replication Design Doc](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Replication)
>
> [Processing Guarantees in Details — Andy Briant](https://medium.com/@andy.bryant/processing-guarantees-in-kafka-12dd2e30be0e)

### Schema and Registry

Messages are serialized when quitting a producer and deserialized when handled by the consumer.
To ensure compatibility, both must be using the same data definition.
Ensuring this can be hard considering the application evolution.
As a result, when dealing with a production system, it is recommended to use a schema to explicit a contract on the data structure.

To do this, Kafka provides a **Registry** server, storing and binding schema to topics.
Historically only [Avro](https://avro.apache.org/docs/current/) was available, but the registry is now modular and can also handle
[JSON](https://json-schema.org/) and [Protobuf](https://developers.google.com/protocol-buffers) out of the box.

Once a producer sent a schema describing the data handled by its topic to the registry, other parties
(_i.e._ brokers and consumers) will fetch this schema on the registry to validate and deserialize the data.

> Further Reading:
>
> [Schema Registry Documentation](https://docs.confluent.io/platform/current/schema-registry/index.html)
>
> [Kafka tutorial #4-Avro and the Schema Registry— Alexis Seigneurin](https://aseigneurin.github.io/2018/08/02/kafka-tutorial-4-avro-and-schema-registry.html)
>
> [Serializer-Deserializer for Schema](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#serializer-and-formatter)


## Integrations

Kafka provides multiple ways of connecting to the brokers,
and each can be more useful than the others depending on the needs.
As a result, even if a library is an abstraction layer above another, it is not necessarily better for every use case.

### Kafka library

There are client libraries available in [numerous languages](https://docs.confluent.io/platform/current/clients/index.html)
which help develop a producer and consumer easily.
We will use Java for the example below, but the concept remains identical for other languages.

The producer concept is to publish messages at any moment, so the code is pretty simple.

```java
public class Main {
  public static void main(String[] args) throws Exception {
    // Configure your producer
    Properties producerProperties = new Properties();
    producerProperties.put("bootstrap.servers", "localhost:29092");
    producerProperties.put("acks", "all");
    producerProperties.put("retries", 0);
    producerProperties.put("linger.ms", 1);
    producerProperties.put("key.serializer", "org.apache.kafka.common.serialization.LongSerializer");
    producerProperties.put("value.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
    producerProperties.put("schema.registry.url", "http://localhost:8081");
    
    // Initialize a producer
    Producer<Long, AvroHelloMessage> producer = new KafkaProducer<>(producerProperties);
    
    // Use it whenever you need
    producer.send(new AvroHelloMessage(1L, "this is a message", 2.4f, 1));
  }
}
```

The code is a bit more complex on the consumer part since the consumption loop needs to be created manually.
On the other hand, this gives more control over its behaviour.
The consumer state is automatically handled by the Kafka library.
As a result, restarting the worker will start at the most recent offset he encountered.

```java
public class Main {
    public static Properties configureConsumer() {
        Properties consumerProperties = new Properties();

        consumerProperties.put("bootstrap.servers", "localhost:29092");
        consumerProperties.put("group.id", "HelloConsumer");
        consumerProperties.put("key.deserializer", "org.apache.kafka.common.serialization.LongDeserializer");
        consumerProperties.put("value.deserializer", "io.confluent.kafka.serializers.KafkaAvroDeserializer");
        consumerProperties.put("schema.registry.url", "http://localhost:8081");
        // Configure Avro deserializer to convert the received data to a SpecificRecord (i.e. AvroHelloMessage)
        // instead of a GenericRecord (i.e. schema + array of deserialized data).
        consumerProperties.put(KafkaAvroDeserializerConfig.SPECIFIC_AVRO_READER_CONFIG, true);

        return consumerProperties;
    }

    public static void main(String[] args) throws Exception {
        // Initialize a consumer
        final Consumer<Long, AvroHelloMessage> consumer = new KafkaConsumer<>(configureConsumer());

        // Chose the topics you will be polling from.
        // You can subscribe to all topics matching a Regex.
        consumer.subscribe(Pattern.compile("hello_topic_avro"));

        // Poll will return all messages from the current consumer offset
        final AtomicBoolean shouldStop = new AtomicBoolean(false);
        Thread consumerThread = new Thread(() -> {
            final Duration timeout = Duration.ofSeconds(5);

            while (!shouldStop) {
                for (ConsumerRecord<Long, AvroHelloMessage> record : consumer.poll(timeout)) {
                    // Use your record
                    AvroHelloMessage value = record.value();
                }
                // Be kind to the broker while polling
                Thread.sleep(5);
            }

            consumer.close(timeout);
        });

        // Start consuming && do other things
        consumerThread.start();
        // [...]

        // End consumption from customer
        shouldStop.set(true);
        consumerThread.join();
    }
}
```

> Further Reading:
>
> [Available Libraries](https://docs.confluent.io/platform/current/clients/index.html)
>
> [Producer Configuration](https://docs.confluent.io/platform/current/installation/configuration/producer-configs.html)
>
> [Consumer Configuration](https://docs.confluent.io/platform/current/installation/configuration/consumer-configs.html)

### Kafka Streams

Kafka Streams is built on top of the consumer library.
It continuously reads from a topic and processes the messages with code declared with a functional DSL.

During the processing, transitional data can be kept in structures called [KStream](https://kafka.apache.org/23/javadoc/org/apache/kafka/streams/kstream/KStream.html)
and [KTable](https://kafka.apache.org/23/javadoc/org/apache/kafka/streams/kstream/KTable.html),
which are stored into topics. The former is equivalent to a standard topic, and the latter to a compacted topic.
Using these data stores will enable automatic tracking of the worker state by Kafka, helping to get back on track in case of restart.

The following code sample is extracted from the [tutorial provided by Apache](https://kafka.apache.org/28/documentation/streams/tutorial).
The code connects to a topic named `streams-plaintext-input` containing strings values, without necessarily providing keys.
The few lines configuring the `StreamsBuilder` will:

1.  Transform each message to lowercase.
1.  Split the result using whitespaces as a delimiter.
1.  Group previous tokens by value.
1.  Count the number of tokens for each group and save the changes to a KTable named `counts-store`.
1.  Stream the changes in this Ktable to send the values in a KStream named `streams-wordcount-output`.

```java
public class Main {
  public static void main(String[] args) throws Exception {
    Properties props = new Properties();
    props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-wordcount");
    props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:29092");
    props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
    props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

    final StreamsBuilder builder = new StreamsBuilder();

    builder.<String, String>stream("streams-plaintext-input")
            .flatMapValues(value -> Arrays.asList(value.toLowerCase(Locale.getDefault()).split("\\W+")))
            .groupBy((key, value) -> value)
            .count(Materialized.<String, Long, KeyValueStore<Bytes, byte[]>>as("counts-store"))
            .toStream()
            .to("streams-wordcount-output", Produced.with(Serdes.String(), Serdes.Long()));

    final Topology topology = builder.build();
    final KafkaStreams streams = new KafkaStreams(topology, props);
    final CountDownLatch latch = new CountDownLatch(1);

    // attach shutdown handler to catch control-c
    Runtime.getRuntime().addShutdownHook(new Thread("streams-shutdown-hook") {
      @Override
      public void run() {
        streams.close();
        latch.countDown();
      }
    });

    // The consumer loop is handled by the library
    streams.start();
    latch.await();
  }
}
```

> Further Reading:
>
> [Kafka Streams Concepts](https://docs.confluent.io/platform/current/streams/concepts.html)
>
> [Developer Guide](https://docs.confluent.io/platform/current/streams/developer-guide/write-streams.html)
>
> [Kafka Stream Work Allocation — Andy Briant](https://medium.com/@andy.bryant/kafka-streams-work-allocation-4f31c24753cc)

### Kafka Connect

Kafka Connect provides a way of transforming and synchronizing data between almost any technology with the use of **Connectors**.
Confluent is hosting a [Hub](https://www.confluent.io/hub/), on which users can share connectors for various technologies.
This means that integrating a Kafka Connect pipeline is most of the time only a matter of configuration, without code required.
A single connector can even handle both connection sides:

*   Populate a topic with data from any system: _i.e._ a **Source**.
*   Send data from a topic to any system: _i.e._ a **Sink**.

The source will read data from CSV files in the following schema then publish them into a topic.
Concurrently, the sink will poll from the topic and insert the messages into a MongoDB database.
Each connector can run in the same or a distinct worker, and workers can be grouped into a cluster for scalability.

![Kafka Connect Example](/images/posts/2021-06-01_Kafka-Apprentice-Cookbook/kafka_connect.png)

The connector instance is created through a configuration specific to the library.
The file below is a configuration of the [MongoDB connector](https://www.confluent.io/hub/mongodb/kafka-connect-mongodb).
It asks to fetch all messages from the topic `mongo-source` to insert them into the collection `sink` of the database named `kafka-connect`.
The credentials are provided from an external file, which is a feature of Kafka Connect to [protect secrets](https://docs.confluent.io/platform/current/connect/security.html#externalizing-secrets).

```json
{
  "name": "mongo-sink",
  "config": {
    "topics": "mongo-source",
    "tasks.max": "1",
    "connector.class": "com.mongodb.kafka.connect.MongoSinkConnector",
    "connection.uri": "mongodb://${file:/auth.properties:username}:${file:/auth.properties:password}@mongo:27017",
    "database": "kafka_connect",
    "collection": "sink",
    "max.num.retries": "1",
    "retries.defer.timeout": "5000",
    "document.id.strategy": "com.mongodb.kafka.connect.sink.processor.id.strategy.BsonOidStrategy",
    "post.processor.chain": "com.mongodb.kafka.connect.sink.processor.DocumentIdAdder",
    "delete.on.null.values": "false",
    "writemodel.strategy": "com.mongodb.kafka.connect.sink.writemodel.strategy.ReplaceOneDefaultStrategy"
  }
}
```

Once the configuration complete, registering the connector is as easy as an HTTP call on the running [Kafka Connect instance](https://docs.confluent.io/home/connect/userguide.html#configuring-and-running-workers).
Afterwards, the service will automatically watch the data without further work required.

```shell
$ curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" \
  http://localhost:8083/connectors -d @sink-conf.json
```

> Further Reading:
>
> [Getting Started Documentation](https://docs.confluent.io/platform/current/connect/userguide.html#connect-userguide)
>
> [Connector Instance API Reference](https://docs.confluent.io/platform/current/connect/references/restapi.html)
>
> [(Youtube) Tutorials Playlist — Confluent](https://www.youtube.com/playlist?list=PLa7VYi0yPIH1MB2n2w8pMZguffCDu2L4Y)

### KSQL Database

Ksql is somehow equivalent to Kafka Streams, except that every transformation is declared in an SQL-like language.
The server is connected to the brokers and can create **Streams** or **Tables** from topics.
Those two concepts behave in the same way as a KStream or KTable from Kafka Streams (_i.e._ respectively a topic and a compacted topic).

There are three types of query in the language definition:

1.  **Persistent Query** (_e.g._ `CREATE TABLE <name> WITH (...)`): Creates a new stream or table that will be automatically updated.
2.  **Pull Query** (_e.g._ `SELECT * FROM <table|stream> WHERE ID = 1`): Behaves similarly to a standard DBMS. Fetches data as an instant snapshot and closes the connection.
3.  **Push Query** (_e.g._ `SELECT * FROM <table|stream> EMIT CHANGES`): Requests a persistent connection to the server, asynchronously pushing updated values.

The database can be used to browse the brokers' content. Topics can be discovered through the command `list topics`, and their content displayed using `print <name>`.

```sql
ksql> list topics;
 Kafka Topic      | Partitions | Partition Replicas
----------------------------------------------------
 hello_topic_json | 1          | 1
----------------------------------------------------

ksql> print 'hello_topic_json' from beginning;
Key format: KAFKA_BIGINT or KAFKA_DOUBLE or KAFKA_STRING
Value format: JSON or KAFKA_STRING
rowtime: 2021/05/25 08:44:20.922 Z, key: 1, value: {"user_id":1,"message":"this is a message","value":2.4,"version":1}
rowtime: 2021/05/25 08:44:20.967 Z, key: 1, value: {"user_id":1,"message":"this is another message","value":2.4,"version":2}
rowtime: 2021/05/25 08:44:20.970 Z, key: 2, value: {"user_id":2,"message":"this is another message","value":2.6,"version":1}
```

The syntax to create and query a stream, or a table is very close to SQL.

```sql
-- Let's create a table from the previous topic
ksql> CREATE TABLE messages (user_id BIGINT PRIMARY KEY, message VARCHAR) 
> WITH (KAFKA_TOPIC = 'hello_topic_json', VALUE_FORMAT='JSON');

-- We can see the list and details of each table
ksql> list tables;
 Table Name | Kafka Topic      | Key Format | Value Format | Windowed
----------------------------------------------------------------------
 MESSAGES   | hello_topic_json | KAFKA      | JSON         | false
----------------------------------------------------------------------

ksql> describe messages;
Name                 : MESSAGES
 Field   | Type
------------------------------------------
 USER_ID | BIGINT           (primary key)
 MESSAGE | VARCHAR(STRING)
------------------------------------------
For runtime statistics and query details run: DESCRIBE EXTENDED <Stream,Table>;

-- Appart from some additions to the language, the queries are almost declared in standard SQL. 
ksql> select * from messages EMIT CHANGES;
+--------+------------------------+
|USER_ID |MESSAGE                 |
+--------+------------------------+
|1       |this is another message |
|2       |this is another message |
```

Kafka recommends using a [headless ksqlDB server](https://www.confluent.io/blog/deep-dive-ksql-deployment-options/)
for production, with a file declaring all streams and tables to create.
This avoids any modification to the definitions.

_Note: ksqlDB servers can be grouped in a cluster like any other consumer._

> Further Reading:
>
> [Official Documentation](https://docs.confluent.io/platform/current/streams-ksql.html)
>
> [KSQL Query Types In Details](https://docs.ksqldb.io/en/latest/concepts/queries/)
>
> [(Youtube) Tutorials Playlist — Confluent](https://www.youtube.com/playlist?list=PLa7VYi0yPIH2eX8q3mPpZAn3qCS1eDX8W)

## Conclusion

This article gives a broad view of the Kafka ecosystem and possibilities, which are numerous.
This article only scratches the surface of each subject.
But worry not, as they are all well documented by Apache, Confluent, and fellow developers.
Here are a few supplementary resources to dig further into Kafka:

*   [(Youtube) Kafka Tutorials - _Confluent_](https://www.youtube.com/playlist?list=PLa7VYi0yPIH0KbnJQcMv5N9iW8HkZHztH)
*   [Kafka Tutorials in Practice](https://kafka-tutorials.confluent.io/)
*   [Top 5 Things Every Apache Kafka Developer Should Know — Bill Bejeck](https://www.confluent.io/blog/5-things-every-kafka-developer-should-know/)
*   [Kafkacat user Guide](https://docs.confluent.io/platform/current/app-development/kafkacat-usage.html)
*   [Troubleshooting KSQL Part 2: What’s Happening Under the Covers? — Robin Moffatt](https://www.confluent.io/blog/troubleshooting-ksql-part-2)
*   [Apache Kafka Internals — sudan](https://ssudan16.medium.com/kafka-internals-47e594e3f006)

_The complete experimental code is available on my [GitHub repository](https://github.com/aveuiller/frameworks-bootstrap/tree/master/Kafka)._
