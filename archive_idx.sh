#!/bin/bash
#
# Archive Index Data

docker cp --archive thcap1:/price-indices bak-data/


docker cp --archive thcap1:/price-data bak-price/
