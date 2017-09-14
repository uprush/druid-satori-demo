# 🌊  Integrate Druid and Satori in about 50 lines of Python 🌊
=======

## Overview

This example streams and indexes data from Satori's cryptocurrency-market-data channel. From there you can analyze the data with SQL or put a Superset visualization layer on top.

If you're lazy just [watch the video](https://youtu.be/MxRWWUc_ZKU).

## Pre-requisites

A Satori account is required. You need an app key to pull data. Visit https://www.satori.com/ to get one.

Python, Druid and Kafka are required. Hive is optional but worth the visit. Hortonworks HDP 2.6+ gives you everything you need.

* Ingestion scripts assume Kafka is running on the standard default port (9092) rather than the one Ambari installs it on (whatever that may be). You may need to override the port number using the -k option.
* Hive 2 is assumed to be running on port 10000. Ambari will launch it on port 10500. Override it with an extra argument to 05hive_external_table.sh

## Procedure

* Run 00setup.sh to install Python dependencies (or you can resolve them manually).
* Edit 01satori_cryptocurrency_kafka.py to put in your personal app key. You can get that from the Satori website.
* Run 01satori_cryptocurrency_kafka.py to ingest data. If needed, run 01satori_cryptocurrency_kafka.py -k kafka:port. Leave that running on a dedicated terminal.
* Run 03start_supervisor.sh to start indexing.
* Run 04query_rest.sh to query the data. It will take a moment or two before any results come back.

## Help Building Your Own

02suggest_supervisor_spec.py will peek into Kafka and suggest a supervisor spec for you. The spec requires a bit of editing but helps you get started. You should be able to bring in any data source you like from Satori if you favor something else.

## Fun Fact

Github projects that use emojis in their descriptions get more stars for no good reason.
