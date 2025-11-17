#!/bin/bash

set -e   # stop on error

echo "=============================="
echo "  LLM Forecasting – Run Script"
echo "=============================="

# check API key
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo " ERROR: environment variable OPENROUTER_API_KEY is not set."
    echo "   Run with: "
    echo "     export OPENROUTER_API_KEY=your-key"
    echo "   or inside Docker: "
    echo "     docker run -e OPENROUTER_API_KEY=your-key ..."
    exit 1
fi

# prepare output directory
mkdir -p results
timestamp=$(date +"%Y%m%d_%H%M%S")

raw_file="results/raw_${timestamp}.json"
analysis_file="results/analysis_${timestamp}.txt"

echo " Raw output will be saved to: $raw_file"
echo " Analysis will be saved to: $analysis_file"
echo ""

# Step 1: Run replicate.py
echo " Running replicate.py …"
python replicate.py

# assume output file name inside replicate.py:
if [ ! -f "raw_openai_gpt41mini_monotonic.json" ]; then
    echo "ERROR: replicate.py did not produce raw_openai_gpt41mini_monotonic.json"
    exit 1
fi

mv raw_openai_gpt41mini_monotonic.json "$raw_file"
echo "Raw results saved."

# Step 2: Run replicate_analyse.py
echo "Running replicate_analyse.py …"
python replicate_analyse.py "$raw_file" > "$analysis_file"

echo "Analysis saved."
echo ""

echo "=============================="
echo "  ALL DONE!"
echo "  Raw data : $raw_file"
echo "  Analysis : $analysis_file"
echo "=============================="
