#!/bin/bash

echo Which stage ? 1.local 2.staging 3.production
read stage

if [[ stage -eq 1 ]]; then
  env="local"
elif [[ stage -eq 2 ]]; then
  env="staging"
elif [[ stage -eq 3 ]]; then
  env="production"
else
  env="local"
fi

export env


echo Reinstall dependencies ? y/n
read dep

echo -e "\n==================== Building ${env} app ====================\n"

if [[ dep == 'y' ]] || [[ dep == 'Y' ]] || [[ dep == 'yes' ]] || [[ dep == 'YES' ]]; then
  bash $(pwd)/deployments/script/pack.sh
else
  bash $(pwd)/deployments/script/pack-venv.sh
fi

echo -e "\n${env} app build success !\n"
