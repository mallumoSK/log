#!/bin/bash

SCRIPT_DIR=$(dirname "$0")
DIR=${1:-$(pwd)}
BMAX=${2:-10}

CMD=(~/projects/ai/bin/python3 "$SCRIPT_DIR/commit_llama_client.py" "$DIR" -bmax "$BMAX")

"${CMD[@]}"
