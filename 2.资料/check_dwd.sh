#!/usr/bin/env bash
DT=$1
[ "$DT" ] || DT=$(date -d '-1 day' +%F)

# 检查表 dwd_order_detail
bash null_id.sh -t dwd_order_detail -d "$DT" -c id -a 1000 -b 30000 -s 0 -x 100 -l 0

# 检查表 dwd_order_info
bash null_id.sh -t dwd_order_info -d "$DT" -c id -s 0 -x 10 -l 0
bash duplicate.sh -t dwd_order_info -d "$DT" -c id -s 0 -x 5 -l 0

# 检查表 dwd_order_refund_info
bash null_id.sh -t dwd_order_refund_info -d "$DT" -c id -s 0 -x 10 -l 0

# 检查表 dwd_payment_info
bash null_id.sh -t dwd_payment_info -d "$DT" -c id -s 0 -x 10 -l 0

# 检查表 dwd_refund_payment
bash null_id.sh -t dwd_refund_payment -d "$DT" -c id -s 0 -x 10 -l 0
