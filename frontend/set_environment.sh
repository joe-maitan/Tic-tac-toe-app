#!/bin/bash

umask 077;

# add preconfigured module on CS-dept systems if present
# allows the npm install and run dev commands to run successfully
source /etc/profile.d/modules.sh
module purge
module load courses/cs314

# installs necessary programs to pull up the frontend webpage
npm install
npm run dev