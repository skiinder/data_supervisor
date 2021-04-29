#!/usr/bin/env bash
DT=$1
[ -z $DT ] || DT=$(date -d '-1 day' +%F)

day_on_day.sh -t ods_user_info -d "$DT" -s -10 -x 10
week_on_week.sh -t ods_user_info -d "$DT" -s -10 -x 50