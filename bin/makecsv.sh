#!/bin/sh
egrep "^<row" ftp/uploads/de-dwd-nkdz-req-TAUUHV.xml|sed -e "s/<[^>]*>/,/g"|sed -e "s/^,*//g" > graphics/de-dwd-nkdz-req-TAUUHV.csv
