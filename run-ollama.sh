#!/bin/bash

OLLAMA_DIR=/gws/ssde/j25b/eds_ai/high5/misc/ollama-dir

model=${1:-llama3.3}
context_size=4096
context_size=64000
context_size=8192
context_size=16000

wait=30
echo "[INFO] Running ollama with model: $model"
echo "[INFO] With context size: $context_size"
sleep 1

export OLLAMA_DIR=/gws/ssde/j25b/eds_ai/high5/misc/ollama-dir
export OLLAMA_MODELS=$OLLAMA_DIR/models
export PATH=$PATH:$OLLAMA_DIR/bin
export OLLAMA_KEEP_ALIVE=1h
export OLLAMA_CUDA=1


start_svc_cmd="$OLLAMA_DIR/bin/ollama serve"
run_model_cmd="$OLLAMA_DIR/bin/ollama run ${model}"

echo
echo "[INFO] Starting ollama service with: ${start_svc_cmd}"
sleep 1
OLLAMA_CONTEXT_LENGTH=${context_size} $start_svc_cmd 
echo "[INFO] Ollama server has started!"
echo "[INFO] Sleeping for $wait seconds for service to start..."
sleep $wait

echo
echo "[INFO] Start serving model ${model} with: ${run_model_cmd}"
$run_model_cmd &

