from cassandra.cluster import Cluster

# This uses mesos-dns to locate our cassandra cluster.  Cassandra
# always runs on the same port.
cassandra_cli = Cluster(['cassandra-dcos-node.cassandra.dcos.mesos'],
                        protocol_version=3)

def create_table():
    cc = cassandra_cli.connect()
    cc.execute("""
    CREATE KEYSPACE IF NOT EXISTS TEMPLATE_CASSANDRA_KEYSPACE
    WITH replication = {'class':'SimpleStrategy', 'replication_factor':3}""")
    cc.execute("""
    CREATE TABLE IF NOT EXISTS TEMPLATE_CASSANDRA_KEYSPACE.spark_results (
      x int,
      y int,
      value int,
      PRIMARY KEY (x, y)
    )""")
