#!/usr/bin/env bash

env="staging"

export env
export script_dir

echo -e "\n==================== Packaging files ====================\n"
sh $(pwd)/deployments/script/pack.sh

echo -e "\n==================== Deploying to ${env} ====================\n"
sh $(pwd)/deployments/script/update-lambda.sh

echo -e "\n${env} deployed !\n"
