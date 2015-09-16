// scalastyle:off println
package org.mesosphere.hab

import java.util.HashMap

import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._
import org.apache.spark.SparkConf

import com.datastax.driver.core.Cluster
import com.datastax.driver.core.Host
import com.datastax.driver.core.Metadata
import com.datastax.driver.core.Session

/**
* Consumes sound volume messages from one or more topics in Kafka,
* processes them, and sends them to Cassandra.
*
* Usage: KafkaMicstream <zkQuorum> <group> <topics> <numThreads> <cassandraNode>
*   <zkQuorum> is a list of one or more zookeeper servers that make quorum
*   <group> is the name of kafka consumer group
*   <topics> is a list of one or more kafka topics to consume from
*   <numThreads> is the number of threads the kafka consumer should use
*/
object SparkMicstream {
  def main(args: Array[String]) {
    if (args.length < 4) {
      System.err.println("Usage: SparkMicstream <zkQuorum> <group> <topics> <numThreads>")
      System.exit(1)
    }
    val node = "cassandra-dcos-node.cassandra.dcos.mesos"
    val Array(zkQuorum, group, topics, numThreads) = args

    val cluster = Cluster.builder().addContactPoint(node).build();
    val metadata = cluster.getMetadata()
    System.out.printf("Connected to cluster: %s\n",
        metadata.getClusterName())
    val session = cluster.connect()
    session.execute("CREATE KEYSPACE IF NOT EXISTS mesosphere " +
        "WITH replication = {'class':'SimpleStrategy', 'replication_factor':3}")
    session.execute("CREATE TABLE IF NOT EXISTS mesosphere.spark_results (" +
        "x int, " +
        "y int, " +
        "value int, " +
        "PRIMARY KEY (x, y)")

    val sparkConf = new SparkConf().setAppName("SparkMicstream")
    val ssc = new StreamingContext(sparkConf, Seconds(2))
    ssc.checkpoint("checkpoint")

    val topicMap = topics.split(",").map((_, numThreads.toInt)).toMap
    val packets = KafkaUtils.createStream(ssc, zkQuorum, group, topicMap)
    // packets.map(_.split(" ")).map(_._2.toInt)
    packets.foreachRDD { (rdd, time) =>
      rdd.foreach { case (kafkaMessageId, message) =>
        // ASSUMPTIONS:
        //  1. The tuple `t` represents a single message from kafka (KafkaMessageId, Message)
        //  2. The message should fit the following format "x,y amplitude1:amplitude2:amplitude3"

        val Array(xy, amplitudeStrings) = message.split(" ")
        val Array(xString, yString) = xy.split(",")
        val x = xString.toInt
        val y = yString.toInt
 
        val sensor_id = xy
        val vol_array = amplitudeStrings.split(":").map(_.toInt)
        val mean_volume = vol_array.sum / vol_array.length
        session.execute("DELETE from mesosphere.spark_results " +
                      s"WHERE sensor_id = $sensor_id")
        session.execute("INSERT INTO mesosphere.spark_results (x, y, value)" +
      	              s"VALUES ($x, $y, $mean_volume)")
      }
    }

    ssc.start()
    ssc.awaitTermination()
  }
}
// scalastyle:on println
