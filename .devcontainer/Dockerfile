FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-20.04

RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa

RUN apt-get update && apt-get install -y \
    python3.9 python3.9-dev python3.9-venv \
    python3.10 python3.10-dev python3.10-venv \
    python3.11 python3.11-dev python3.11-venv \
    python3.12 python3.12-dev python3.12-venv

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 2 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 3 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 4
