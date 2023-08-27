#!/bin/bash
export PYTHONPATH=src/python/api

script_dir="$(cd "$(dirname "$0")" && pwd)"
# Path to the configuration file
json_file="$script_dir/config.json"

# Read the URL from JSON using jq
export MONGO_URI=$(jq -r '.MONGODB_URI' "$json_file")

uvicorn main:app --host 0.0.0.0 --reload