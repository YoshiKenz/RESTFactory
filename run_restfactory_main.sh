#!/bin/bash

export PYTHONPATH=/RESTFactory:$PYTHONPATH

python3 -m core.__main__ "$@"