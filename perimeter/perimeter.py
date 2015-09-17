import sys

from cassandra.cluster import Cluster
from flask import Flask, render_template, jsonify
from kafka import SimpleProducer, KafkaClient
import srvlookup

# This uses mesos-dns to locate our cassandra cluster.  Cassandra
# always runs on the same port.
cassandra_cli = Cluster(['cassandra-dcos-node.cassandra.dcos.mesos'],
                        protocol_version=3)

# Setup cassandra if necessary
def try_setup():
    print >> sys.stderr, "verifying and possibly creating cassandra schema"
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
    print >> sys.stderr, "cassandra configured"

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

default_ranges = {"intensity": [0, 5000],
                  "x": [0, 100],
                  "y": [0, 25]}

sensor_map = {1: [25, 8],
              2: [25, 16],
              3: [75, 8],
              4: [75, 16],
              5: [50, 8],
              6: [50, 16]}

print >> sys.stderr, "after env setup"

@app.route('/')
@app.route('/test')
def test_endpoint():
    return 'testing...'

@app.route('/whatever/<value>')
def index(value=None):
    # serve code that periodically hits /read to get the
    # latest spark results from Cassandra
    return render_template('index.html', value=value)

@app.route('/read')
def read():
    # read data from cassandra, if it's been populated yet
    try:
        session = cassandra_cli.connect()
        results = session.execute('SELECT x, y, value '
                                  'FROM TEMPLATE_CASSANDRA_KEYSPACE.spark_results',
                                  timeout=5)
        rows = [{"x": r.x, "y": r.y, "intensity": r.value} for r in results]
        return jsonify({"ranges": default_ranges,
                        "sources": rows})
    except e:
        print >> sys.stderr, "failed to execute read on cassandra: %s" % e
        return e

@app.route('/remove/<sensor_id>')
def remove(sensor_id):
    (x, y) = sensor_id.split(',')
    # read data from cassandra, if it's been populated yet
    try:
        session = cassandra_cli.connect()
        results = session.execute('DELETE FROM '
                                  'TEMPLATE_CASSANDRA_KEYSPACE.spark_results '
                                  'WHERE x = ' + x + ' AND y = ' + y)
        return 'removed data at x=%s, y=%s' % (x, y)
    except e:
        print >> sys.stderr, "failed to execute delete on cassandra: %s" % e
        return e

@app.route('/submit/<sensor_id>/<sensor_value>')
def write(sensor_id, sensor_value):
    if sensor_id.find(',') >= 0:
        (x, y) = sensor_id.split(',')
    else:
        (x, y) = [str(i) for i in sensor_map[int(sensor_id)]]

    value_array = [int(i) for i in sensor_value.split(':')]
    average_value = sum(value_array) / len(value_array)

    # producer.send_messages(b'TEMPLATE_KAFKA_TOPIC',
    #                        b"%s %d" % (sensor_id, sensor_value))
    try:
        session = cassandra_cli.connect()
        results = session.execute('INSERT INTO '
                                  'TEMPLATE_CASSANDRA_KEYSPACE.spark_results '
                                  '(x, y, value) '
                                  'VALUES (%s, %s, %d)' % (x, y, average_value),
                                  timeout=5)
        print >> sys.stderr, "after execute"
        return 'sensor %s submitted value %d' % (sensor_id, average_value)
    except e:
        print >> sys.stderr, "failed to execute read on cassandra: %s" % e

if __name__ == "__main__":
    # In a real environment, never run with debug=True
    # because it gives you an interactive shell when you
    # trigger an unhandled exception.
    app.run(host="0.0.0.0", debug=True, port=8088)
