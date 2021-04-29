#!/usr/bin/env bash
DT=$1
[ -z $DT ] || DT=$(date -d '-1 day' +%F)

null_id.sh -t dwd_refund_payment -d "$DT" -c id -s 0 -x 10