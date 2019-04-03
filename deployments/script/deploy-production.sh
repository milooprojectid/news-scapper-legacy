#!/usr/bin/env bash

script_dir=$(pwd)
env="production"

export env
export script_dir

echo -e "\n==================== Packaging files ====================\n"
sh $(pwd)/deployments/script/pack-venv.sh

echo -e "\n==================== Deploying to ${env} ====================\n"
sh $(pwd)/deployments/script/update-lambda.sh

echo -e "\n${env} deployed !\n"
