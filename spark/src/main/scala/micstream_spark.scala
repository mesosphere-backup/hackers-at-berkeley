// scalastyle:off println
package org.mesosphere.hab

import java.util.HashMap

import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._
import org.apache.spark.SparkConf

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.Host;
import com.datastax.driver.core.Metadata;
import com.datastax.driver.core.Session;

/**
* Consumes sound volume messages from one or more topics in Kafka,
* processes them, and sends them to Cassandra.
*
* Usage: KafkaMicstream <zkQuorum> <group> <topics> <numThreads> <cassandraNode>
*   <zkQuorum> is a list of one or more zookeeper servers that make quorum
*   <group> is the name of kafka consumer group
*   <topics> is a list of one or more kafka topics to consume from
*   <numThreads> is the number of threads the kafka consumer should use
*   <cassandraNode> is the IP address of the Cassandra node
*/
object SparkMicstream {
  def main(args: Array[String]) {
    if (args.length < 4) {
      System.err.println("Usage: SparkMicstream <zkQuorum> <group> <topics> <numThreads> <cassandraNode>")
      System.exit(1)
    }

    val Array(zkQuorum, group, topics, numThreads, node) = args

    val cluster = Cluster.builder().addContactPoint(node).build();
    val metadata = cluster.getMetadata()
    System.out.printf("Connected to cluster: %s\n",
        metadata.getClusterName())
    val session = cluster.connect()
    session.execute("CREATE TABLE mesosphere.hab (" +
        "sensor_id text PRIMARY KEY, volume int)")

    val sparkConf = new SparkConf().setAppName("SparkMicstream")
    val ssc = new StreamingContext(sparkConf, Seconds(2))
    ssc.checkpoint("checkpoint")

    val topicMap = topics.split(",").map((_, numThreads.toInt)).toMap
    val packets = KafkaUtils.createStream(ssc, zkQuorum, group, topicMap)
    val volumes = packets.map(_.split(" ")).map(_._2.toInt)
    volumes.foreachRDD{
      val sensor_id = _._1
      val mean_volume = _._2.split(":").sum / vol_array.length
      session.execute("DELETE from mesosphere.hab " +
                      s"WHERE sensor_id = $sensor_id")
      session.execute("INSERT INTO mesosphere.hab (x, y, value)" +
      	              s"VALUES ($x, $y, $mean_volume)")
    }

    ssc.start()
    ssc.awaitTermination()
  }
}
// scalastyle:on println