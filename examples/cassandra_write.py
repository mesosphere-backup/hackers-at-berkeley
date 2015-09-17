from cassandra.cluster import Cluster

# This uses mesos-dns to locate our cassandra cluster.  Cassandra
# always runs on the same port.
cassandra_cli = Cluster(['cassandra-dcos-node.cassandra.dcos.mesos'],
                        protocol_version=3)

def write_cassandra(x, y, average_value):
    session = cassandra_cli.connect()
    results = session.execute('INSERT INTO '
                              'TEMPLATE_CASSANDRA_KEYSPACE.spark_results '
                              '(x, y, value) '
                              'VALUES (%s, %s, %d)' % (x, y, average_value),
                              timeout=5)
