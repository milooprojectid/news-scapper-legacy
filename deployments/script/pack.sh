#!/usr/bin/env bash

tput setaf 2
set -e

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "${script_dir}/../../"

# remove and recreate build folder
echo "- creating build folder ..."
rm -rf ./deployments/build
mkdir -p ./deployments/build

# activate virtual env
echo "- activating virtual env ..."
source "./venv/bin/activate"

# install dependencies
echo "- installing dependencies ..."
pip install -r ./requirements.txt -t ./deployments/build > /dev/null

# copy source code to build
tput setaf 2
echo "- copying source code ..."
cp -r *.py src ./deployments/build

# inject env to build
echo "- injecting env file ..."
cp -r ./environments/${env}.env ./deployments/build/.env

# zip deployable code
echo "- compressing build ..."
cd deployments/build
zip -qr "build.zip" .
