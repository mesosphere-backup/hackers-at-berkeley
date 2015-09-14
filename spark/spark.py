from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "__main__":
    sc = SparkContext(appName="TEMPLATE_SPARK_CONTEXT")
    ssc = StreamingContext(sc, 1)

    topic = TEMPLATE_KAFKA_TOPIC
    zkQuorum = TEMPLATE_ZK_QUORUM
    keyspace = TEMPLATE_CASSANDRA_KEYSPACE

    cassandra_conf = {
        "cassandra.output.thrift.address": 'cassandra-dcos-node.cassandra.dcos.mesos',
        "cassandra.output.thrift.port": "9160",
        "cassandra.output.keyspace": keyspace,
        "cassandra.output.partitioner.class": "Murmur3Partitioner",
        "cassandra.output.cql": "UPDATE " + keyspace + ".spark_results SET fname = ?, lname = ?",
        "mapreduce.output.basename": 'spark_results',
        "mapreduce.outputformat.class": "org.apache.cassandra.hadoop.cql3.CqlOutputFormat",
        "mapreduce.job.output.key.class": "java.util.Map",
        "mapreduce.job.output.value.class": "java.util.List"
    }

    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
