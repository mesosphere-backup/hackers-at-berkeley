# hackers-at-berkeley
Example and demo source files for H@B workshop.

## Goal

To deploy an example "internet of things" ingestion pipeline using DCOS and related distributed systems.

## Workshop!

Exercises are provided in the bundled slide deck.

## Appendix

The text below refers to the components of the workshop that have already been set up and that we have provided for people to re-use if they so wish.

If you're taking part in the Hackers at Berkeley workshop, we have already provided you with a cluster - ignore the following sections!

### DCOS Cluster with Cassandra, Kafka and Spark

1. Stand up a [Mesosphere DCOS cluster on Amazon Web Services](https://mesosphere.com/product/). Configure the DCOS CLI to point to this cluster.

2. Install [Cassandra](https://docs.mesosphere.com/services/cassandra/):

    `dcos package install cassandra`

3. Install [Kafka](https://docs.mesosphere.com/services/kafka/):

    `dcos package install kafka`

4. Add and start a Kafka broker:

    ```
    dcos kafka add 0
    dcos kafka start 0
    ```

5. Optionally, create a nice hostname in Route53 and set it to CNAME the public IP address of your cluster. You will have to look this up using AWS's EC2 instance manager.


### Micstream

We use Raspberry Pis and PyAlsaAudio to send volume data to our cluster. See [micstream/README.md] for Raspberry Pi installation instructions.

### Perimeter

REST API that provides an interface to write values and read stored values. See [perimeter/README.md] for installation instructions.
