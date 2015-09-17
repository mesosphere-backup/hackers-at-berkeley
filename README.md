# hackers-at-berkeley
Example and demo source files for H@B workshop.

## Hardware

We use Raspberry Pis of either version 1 B+ or version 2 B with [Raspbian](https://www.raspbian.org/) installed. The Raspberry Pis must be connected to the internet.

On each Raspberry Pi we use the [USB Kinobo microphone](http://www.amazon.com/Kinobo-Microphone-Desktop-Recognition-Software/dp/B00IR8R7WQ/ref=sr_1_4?s=pc&ie=UTF8&qid=1441404716&sr=1-4&keywords=usb+microphone).


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

Reads input from an ALSA-compatible microphone and transmits at regular
intervals HTTP GET requests containing a colon-delimited list of integers.

See [micstream/README.md] for installation instructions.

## Perimeter

REST API that provides an interface to write values and read stored values.

### Installation

`dcos marathon app add perimeter/marathon.json`