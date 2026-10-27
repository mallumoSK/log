#!/bin/bash
SCRIPT_DIR=$(dirname "$0")
DIR=${1:-$(pwd)}
~/projects/ai/bin/python3 "$SCRIPT_DIR/commit_report_llama_ui.py" "$DIR"
