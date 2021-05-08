#!/usr/bin/env bash
DT=$1
[ "$DT" ] || DT=$(date -d '-1 day' +%F)

#检查表 activity_rule_id
bash duplicate.sh -t dim_activity_rule_info -d "$DT" -c activity_rule_id -s 0 -x 5 -l 0
bash null_id.sh -t dim_activity_rule_info -d "$DT" -c activity_rule_id -s 0 -x 10 -l 0

#检查表 dim_coupon_info
bash duplicate.sh -t dim_coupon_info -d "$DT" -c id -s 0 -x 5 -l 0
bash null_id.sh -t dim_coupon_info -d "$DT" -c id -s 0 -x 10 -l 0

#检查表 dim_sku_info
bash duplicate.sh -t dim_sku_info -d "$DT" -c id -s 0 -x 5 -l 0
bash null_id.sh -t dim_sku_info -d "$DT" -c id -s 0 -x 10 -l 0

#检查表 dim_user_info
bash duplicate.sh -t dim_user_info -d "$DT" -c id -s 0 -x 5 -l 0
bash null_id.sh -t dim_user_info -d "$DT" -c id -s 0 -x 10 -l 0
