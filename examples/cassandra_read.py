from cassandra.cluster import Cluster

# This uses mesos-dns to locate our cassandra cluster.  Cassandra
# always runs on the same port.
cassandra_cli = Cluster(['cassandra-dcos-node.cassandra.dcos.mesos'],
                        protocol_version=3)

def read_cassandra():
    session = cassandra_cli.connect()
    results = session.execute('SELECT x, y, value '
                              'FROM TEMPLATE_CASSANDRA_KEYSPACE.spark_results',
                              timeout=5)
    rows = [{"x": r.x, "y": r.y, "intensity": r.value} for r in results]

    return jsonify(rows)
