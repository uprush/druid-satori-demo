#!/bin/sh

CHANNEL=cryptocurrency-market-data
/usr/hdp/current/kafka-broker/bin/kafka-topics.sh --delete --zookeeper localhost:2181 --topic $CHANNEL
