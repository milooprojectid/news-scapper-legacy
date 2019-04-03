#!/bin/bash

script_dir=$(pwd)
env="production"

export env
export script_dir

echo -e "\n==================== Packaging files ====================\n"
bash $(pwd)/deployments/script/pack.sh

echo -e "\n==================== Deploying to ${env} ====================\n"
bash $(pwd)/deployments/script/update-lambda.sh

echo -e "\n${env} deployed !\n"
