## Setup

The text below refers to the components of the workshop that have already been set up and that we have provided for people to re-use if they so wish.

If you're taking part in the Hackers at Berkeley workshop, we have already provided you with a cluster - ignore the following sections!

### DCOS Cluster with Cassandra, Kafka and Spark


![DCOS services](/img/dcos-architecture.png?raw=true)

1. Stand up a [Mesosphere DCOS cluster on Amazon Web Services](https://mesosphere.com/product/). Configure the DCOS CLI to point to this cluster.

2. Install [Cassandra](https://docs.mesosphere.com/services/cassandra/):

    `dcos package install cassandra`

3. Optionally, create a nice hostname in Route53 and set it to CNAME the public IP address of your cluster. You will have to look this up using AWS's EC2 instance manager. Our install script uses `http://hackers-at-berkeley.mesosphere.io`.


### Micstream

We use Raspberry Pis and PyAlsaAudio to send volume data to our cluster. See [micstream/README.md](micstream/README.md) for Raspberry Pi installation instructions.

### Perimeter

REST API that provides an interface to write values and read stored values. See [perimeter/README.md](perimeter/README.md) for installation instructions.

Once you've deployed Perimeter for the first time, be sure to hit `http://hackers-at-berkeley.mesosphere.io/init` (or whatever domain name you've used) to initialise the Cassandra keyspace.