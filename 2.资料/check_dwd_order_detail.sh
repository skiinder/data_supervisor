#!/usr/bin/env bash
DT=$1
[ -z $DT ] || DT=$(date -d '-1 day' +%F)

null_id.sh -t dwd_order_detail -d "$DT" -c id -a 1000 -b 30000 -s 0 -x 100