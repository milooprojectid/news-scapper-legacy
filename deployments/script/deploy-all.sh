#!/usr/bin/env bash

cd "$( dirname "${BASH_SOURCE[0]}" )"
script_dir=$(pwd)
white=`tput setaf 0`

echo -e "\n${white}==================== Deploying staging ====================\n"
sh ./deploy-staging.sh.sh

echo -e "\n${white}==================== Deploying production ====================\n"
sh ./deploy-staging.sh.sh
