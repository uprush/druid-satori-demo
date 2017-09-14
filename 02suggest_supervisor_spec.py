#!/usr/bin/env python

from getopt import getopt
import json
import kafka
import re
import sys
import time

channel = "cryptocurrency-market-data"

def is_number(s):
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

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
    kafka_client = kafka.KafkaConsumer(kafka_topic, bootstrap_servers=kafka_endpoint, auto_offset_reset='smallest')
    message = kafka_client.next()
    value = message.value
    j = json.loads(value)
    dimension = []
    measure = []
    for (key, val) in j.iteritems():
        if key == "timestamp":
            continue
        numeric = is_number(val)
        if numeric:
            measure.append(key)
        else:
            dimension.append(key)

    dimension_string = ", ".join([ '"' + x + '"' for x in dimension ])
    measure_fields = []
    for m in measure:
        measure_fields.append('      {{ "type": "doubleSum", "name": "{0}", "fieldName": "{0}" }}'.format(m))
    measure_string = ",\n".join(measure_fields)

    template = open("supervisor-spec-template.json")
    text = template.read()
    spec = text.format(channel, dimension_string, measure_string, channel)
    file = "supervisor-spec.json"
    fd = open(file, "w")
    fd.write(spec)
    print "Wrote suggested spec to {0}".format(file)

if __name__ == '__main__':
    main()
