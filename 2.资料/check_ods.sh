#!/usr/bin/env bash
DT=$1
[ "$DT" ] || DT=$(date -d '-1 day' +%F)

# 检查表 ods_order_detail
bash day_on_day.sh -t ods_order_detail -d "$DT" -s -10 -x 10 -l 1
bash week_on_week.sh -t ods_order_detail -d "$DT" -s -10 -x 50 -l 1

#检查表 ods_order_info
bash day_on_day.sh -t ods_order_info -d "$DT" -s -10 -x 10 -l 1
bash week_on_week.sh -t ods_order_info -d "$DT" -s -10 -x 50 -l 1
bash range.sh -t ods_order_info -d "$DT" -c final_amount -a 0 -b 100000 -s 0 -x 100 -l 1

#检查表 ods_order_refund_info.sh
bash day_on_day.sh -t ods_order_refund_info -d "$DT" -s -10 -x 10 -l 1
bash week_on_week.sh -t ods_order_refund_info -d "$DT" -s -10 -x 50 -l 1

#检查表 payment_info
bash day_on_day.sh -t ods_payment_info -d "$DT" -s -10 -x 10 -l 1
bash week_on_week.sh -t ods_payment_info -d "$DT" -s -10 -x 50 -l 1

#检查表 ods_refund_payment
bash day_on_day.sh -t ods_refund_payment -d "$DT" -s -10 -x 10 -l 1
bash week_on_week.sh -t ods_refund_payment -d "$DT" -s -10 -x 50 -l 1

#检查表 ods_user_info
bash day_on_day.sh -t ods_user_info -d "$DT" -s -10 -x 10 -l 1
bash week_on_week.sh -t ods_user_info -d "$DT" -s -10 -x 50 -l 1
