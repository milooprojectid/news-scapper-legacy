#!/bin/bash

version='3.7'

# remove and recreate build folder
echo "- creating build folder ..."
mkdir -p $(pwd)/deployments/build

# activate virtual env
echo "- activating virtual env ..."
source $(pwd)/venv/bin/activate

# moving dependencies
echo "- moving dependencies ..."
cp -a $(pwd)/venv/lib/python${version}/site-packages/** $(pwd)/deployments/build

# copy source code to build
echo "- copying source code ..."
cp -r $(pwd)/*.py src $(pwd)/deployments/build

# inject env to build
echo "- injecting env file ..."
cp -r $(pwd)/environments/${env}.env $(pwd)/deployments/build/.env

# zip deployable code
echo "- compressing build ..."
cd deployments/build
zip -qr "../build-${env}.zip" .
cd ../..

# remove build folder
echo "- removing build folder ..."
rm -rf $(pwd)/deployments/build
