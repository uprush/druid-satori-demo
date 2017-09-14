#!/usr/bin/env python

from __future__ import print_function

from getopt import getopt
import json
import kafka
import sys
import time

from satori.rtm.client import make_client, SubscriptionMode

endpoint = "wss://open-data.api.satori.com"
appkey = "YOUR_KEY_HERE"
channel = "cryptocurrency-market-data"

def main():
    # Parse options and setup Kafka.
    try:
        opts, args = getopt(sys.argv[1:], "k:t:")
    except Exception, e:
        assert False, "Usage: satori_cryptocurrency_kafka [-k kafka_endpoint] [-t kafka_topic]"
    kafka_endpoint = "localhost:9092"
    kafka_topic = channel
    for (k,v) in opts:
        if k in ['-k']:
            kafka_endpoint = v
        elif k in ['-t']:
            kafka_topic = v
    kafka_producer = kafka.KafkaProducer(bootstrap_servers=kafka_endpoint)

    with make_client(endpoint=endpoint, appkey=appkey) as client:
        class SubscriptionObserver(object):
            def on_subscription_data(self, data):
                for message in data['messages']:
                    message['_timestamp'] = int(time.time())
                    kafka_producer.send(kafka_topic, bytes(json.dumps(message)))
                    main.count += 1

        subscription_observer = SubscriptionObserver()
        client.subscribe(
            channel,
            SubscriptionMode.SIMPLE,
            subscription_observer)

        try:
            while True:
                time.sleep(1)
                print("Written {0} messages to Kafka".format(main.count))
        except KeyboardInterrupt:
            pass
main.count = 0

if __name__ == '__main__':
    main()
