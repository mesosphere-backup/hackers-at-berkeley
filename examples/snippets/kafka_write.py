from kafka import SimpleProducer, KafkaClient
import srvlookup

# Kafka may not always run on the same port, so we need to perform
# an SRV record lookup in order to find it.
kafka_location = srvlookup.lookup('broker-0', 'tcp', 'kafka.mesos')[0]
kafka = KafkaClient("%s:%s" % (kafka_location.host, kafka_location.port))

# Real-world Kafka workloads will gain an order of magnitude++
# more throughput when using async mode.  The trade-off is your
# requests may have higher latency (the cli will instantly return
# however.)  This is the classic throughput-latency trade-off at play.
producer = SimpleProducer(kafka, async=True)

producer.send_messages(b'my-topic', b'some message')
