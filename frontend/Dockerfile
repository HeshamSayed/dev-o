# Build stage
FROM node:20-alpine AS build

WORKDIR /app

# Build arguments
ARG VITE_API_URL=http://localhost
ARG VITE_WS_URL=ws://localhost

# Set as environment variables for build
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_WS_URL=$VITE_WS_URL

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build for production
RUN npm run build

# Create a simple script to keep container running and preserve build output
RUN echo "#!/bin/sh" > /app/keep-alive.sh && \
    echo "echo 'Build completed. Keeping container alive to preserve volume...'" >> /app/keep-alive.sh && \
    echo "tail -f /dev/null" >> /app/keep-alive.sh && \
    chmod +x /app/keep-alive.sh

# Use the keep-alive script as entrypoint
CMD ["/app/keep-alive.sh"]

# Development stage
FROM node:20-alpine AS development

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Expose port
EXPOSE 3000

# Start dev server
CMD ["npm", "run", "dev"]
