from kafka import KafkaConsumer
import srvlookup

# Kafka may not always run on the same port, so we need to perform
# an SRV record lookup in order to find it.
kafka_location = srvlookup.lookup('broker-0', 'tcp', 'kafka.mesos')[0]

consumer = KafkaConsumer('my-topic', group_id='my_group',
             bootstrap_servers=[("%s:%s" % (kafka_location.host, kafka_location.port))])

for message in consumer:
    # message value is raw byte string -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                         message.offset, message.key,
                                         message.value))
