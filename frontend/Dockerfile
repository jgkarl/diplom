# Use the official Node.js image as the base image
FROM node:22

# Set the working directory in the container
WORKDIR /app

COPY package.json ./
COPY vite.config.js ./

# Install dependencies
RUN npm install