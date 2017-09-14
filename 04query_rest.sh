#!/bin/sh

QUERY=${1:-queries/topn_query.json}

curl -X POST 'http://localhost:8082/druid/v2/?pretty' -H 'content-type: application/json' -d@${QUERY}
