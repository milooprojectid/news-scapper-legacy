#!/usr/bin/env bash

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

zip_file="$script_dir/../build/build.zip"
aws_region="ap-southeast-1"
profile=milo

crawler_name=milo-crawler-${env}
scrapper_name=milo-scrapper-${env}

echo "- updating news-crawler ..."
aws lambda update-function-code --function-name ${crawler_name} --zip-file fileb://${zip_file} --region ${aws_region} --profile ${profile} > /dev/null
