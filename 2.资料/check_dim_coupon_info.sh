#!/usr/bin/env bash
DT=$1
[ -z $DT ] || DT=$(date -d '-1 day' +%F)

duplicate.sh -t dim_coupon_info -d "$DT" -c id -s 0 -x 5
null_id.sh -t dim_coupon_info -d "$DT" -c id -s 0 -x 10