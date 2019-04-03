#!/usr/bin/env bash

cd "$( dirname "${BASH_SOURCE[0]}" )"
script_dir=$(pwd)

env="production"
export env

echo -e "\n==================== Packaging files ====================\n"
sh ./pack.sh

echo -e "\n==================== Deploying to ${env} ====================\n"
sh ./update-lambda.sh

echo -e "\n${env} deployed !\n"