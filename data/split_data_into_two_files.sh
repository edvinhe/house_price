#!/bin/bash


while IFS='' read -r line || [[ -n "$line" ]]
do

    line=`echo $line | xargs echo -n`
    first_part=${line%' '*}
    echo $first_part >> ./shuffled_house_price_features.csv

    second_part=`echo $line | cut -d' ' -f8`
    echo $second_part >> ./shuffled_house_price_values.csv
done < "./shuffled_house_price.csv"
