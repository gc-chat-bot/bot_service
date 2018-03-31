#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PYTHONPATH=$PYTHONPATH:$DIR

python $DIR/infopuls_crawler/dao/storage.py $DIR/texts

python $DIR/infopuls_crawler/app.py