#!/bin/sh

cat<<EOF>/tmp/create_table.sql
SET hive.druid.broker.address.default=druid.example.com:8082;
CREATE EXTERNAL TABLE if not exists cryptocurrency_market_data
STORED BY 'org.apache.hadoop.hive.druid.DruidStorageHandler'
TBLPROPERTIES ("druid.datasource" = "cryptocurrency-market-data");
EOF

HS2=${1:-localhost:10000}
BEELINE="beeline -u jdbc:hive2://$HS2/default"
$BEELINE -f /tmp/create_table.sql
