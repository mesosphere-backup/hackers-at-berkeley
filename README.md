# hackers-at-berkeley
Example and demo source files for H@B workshop.


## DCOS Cluster with Cassandra, Kafka and Spark

1. Stand up a [Mesosphere DCOS cluster on Amazon Web Services](https://mesosphere.com/product/). Configure the DCOS CLI to point to this cluster.

2. Install [Cassandra](https://docs.mesosphere.com/services/cassandra/):

    `dcos package install cassandra`

3. Install [HDFS](https://docs.mesosphere.com/services/hdfs/):

    `dcos package install hdfs`

4. Install [Spark](https://docs.mesosphere.com/services/spark/):

    `dcos package install spark`

5. Install [Kafka](https://docs.mesosphere.com/services/kafka/):

    `dcos package install kafka`

6. Add and start a Kafka broker:

    ```
    dcos kafka add 0
    dcos kafka start 0
    ```

6. Optionally, create a nice hostname in Route53 and set it to CNAME the "PublicSlaveDnsAddress" of your cluster. (See the [Public App tutorial](https://docs.mesosphere.com/tutorials/publicapp/) for details on how to get this.)


## Micstream

We use Raspberry Pis and PyAlsaAudio to send volume data to our cluster. See [micstream/README.md] for Raspberry Pi installation instructions.

## Perimeter

REST API that provides an interface to write values and read stored values.

### Installation

`dcos marathon app add perimeter/marathon.json`