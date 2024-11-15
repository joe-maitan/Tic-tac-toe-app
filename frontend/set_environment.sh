#!/bin/bash

umask 077;

# add preconfigured module on CS-dept systems if present
source /etc/profile.d/modules.sh
module purge
module load courses/cs314

npm install
npm run dev