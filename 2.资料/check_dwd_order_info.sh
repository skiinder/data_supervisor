#!/usr/bin/env bash
DT=$1
[ -z $DT ] || DT=$(date -d '-1 day' +%F)

null_id.sh -t dwd_order_info -d "$DT" -c id -s 0 -x 10
duplicate.sh -t dwd_order_info -d "$DT" -c id -s 0 -x 5