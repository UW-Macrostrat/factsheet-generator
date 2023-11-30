
#!/bin/bash

# docker network create worker-network
docker build -t llama.cpp -f ~/dev/llama.cpp/.devops/full-cuda.Dockerfile --build-arg CUDA_VERSION=11.6.2 --build-arg UBUNTU-VERSION=20.04 ~/dev/llama.cpp
docker run --name llama -it --network host --gpus all -v "$(pwd)"/models:/models local/llama.cpp:full-cuda --server -m /models/starling-lm-7b-alpha.Q6_K.gguf --n-gpu-layers 35