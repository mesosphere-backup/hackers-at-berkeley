from cassandra.cluster import Cluster
from flask import Flask, render_template, jsonify
from kafka import SimpleProducer, KafkaClient
import srvlookup

# This uses mesos-dns to locate our cassandra cluster.  Cassandra
# always runs on the same port.
cassandra_cli = Cluster(['cassandra-dcos-node.cassandra.dcos.mesos'],
                        protocol_version=3)

# Setup cassandra if necessary
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

# Kafka may not always run on the same port, so we need to perform
# an SRV record lookup in order to find it.
kafka_location = srvlookup.lookup('broker-0', 'tcp', 'kafka.mesos')[0]
kafka = KafkaClient("%s:%s" % (kafka_location.host, kafka_location.port))

# Real-world Kafka workloads will gain an order of magnitude++
# more throughput when using async mode.  The trade-off is your
# requests may have higher latency (the cli will instantly return
# however.)  This is the classic throughput-latency trade-off at play.
producer = SimpleProducer(kafka, async=True)

app = Flask(__name__)

@app.route('/')
@app.route('/whatever/<value>')
def index(value=None):
    # serve code that periodically hits /read to get the
    # latest spark results from Cassandra
    return render_template('index.html', value=value)

@app.route('/read')
def read():
    # read data from cassandra, if it's been populated yet
    session = cassandra_cli.connect()
    results = session.execute('SELECT x, y, value '
                              'FROM TEMPLATE_CASSANDRA_KEYSPACE.spark_results')
    rows = [{"x": r.x, "y": r.y, "value": r.value} for r in results]
    return jsonify(rows)

@app.route('/submit/<sensor_id>/<int:sensor_value>')
def write(sensor_id, sensor_value):
    (x, y) = sensor_id.split(',')
    producer.send_messages(b'TEMPLATE_KAFKA_TOPIC',
                           b"%s %d" % (sensor_id, sensor_value))
    session = cassandra_cli.connect()
    results = session.execute('INSERT INTO '
                              'TEMPLATE_CASSANDRA_KEYSPACE.spark_results '
                              '(x, y, value) '
                              'VALUES (%s, %s, %d)' % (x, y, sensor_value))
    return 'sensor %s submitted value %d' % (sensor_id, sensor_value)

if __name__ == "__main__":
    # In a real environment, never run with debug=True
    # because it gives you an interactive shell when you
    # trigger an unhandled exception.
    app.run(host="0.0.0.0", debug=True, port=8080)
