#!/usr/bin/env bash

cd "$( dirname "${BASH_SOURCE[0]}" )"
script_dir=$(pwd)

white=`tput setaf 0`
env="staging"
export env

echo -e "\n${white}==================== Packaging files ====================\n"
sh ./pack-venv.sh

echo -e "\n${white}==================== Deploying to ${env} ====================\n"
sh ./update-lambda.sh

echo -e "\n${white}${env} deployed !\n"
