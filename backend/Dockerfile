FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Update base image and tools
RUN apt update -y && apt upgrade -y
RUN apt install -y vim less htop curl gettext

COPY requirements.txt /app/

# Upgrade pip and setuptools to avoid compatibility issues
RUN python -m ensurepip --upgrade

RUN python -m pip install --upgrade pip setuptools

RUN python -m pip install --no-cache-dir -r requirements.txt

# Install Node.js and npm and install dependencies
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && apt install -y nodejs

COPY theme/static_src/package.json /app/theme/static_src/package.json

RUN npm install theme/static_src/