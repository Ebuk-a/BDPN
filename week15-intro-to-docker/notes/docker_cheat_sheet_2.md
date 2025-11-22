# Docker Quick Reference Cheat Sheet

## Container Management

### Running Containers
```bash
# Run a container
docker run <image_name>

# Run with interactive terminal
docker run -it <image_name>

# Run in detached mode (background)
docker run -d <image_name>

# Run with a custom name
docker run --name my_container <image_name>

# Run and remove after exit
docker run --rm <image_name>
```

### Listing Containers
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List with specific format
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Container Lifecycle
```bash
# Start a stopped container
docker start <container_name_or_id>

# Stop a running container
docker stop <container_name_or_id>

# Restart a container
docker restart <container_name_or_id>

# Pause a container
docker pause <container_name_or_id>

# Unpause a container
docker unpause <container_name_or_id>

# Kill a container (force stop)
docker kill <container_name_or_id>
```

### Removing Containers
```bash
# Remove a stopped container
docker rm <container_name_or_id>

# Remove a running container (force)
docker rm -f <container_name_or_id>

# Remove all stopped containers
docker container prune
```

## Image Management

### Working with Images
```bash
# Pull an image from Docker Hub
docker pull <image_name>:<tag>

# List all images
docker images

# Remove an image
docker rmi <image_name_or_id>

# Remove unused images
docker image prune

# Remove all unused images
docker image prune -a

# Build an image from Dockerfile
docker build -t <image_name>:<tag> .

# Build without cache
docker build --no-cache -t <image_name>:<tag> .
```

### Image Information
```bash
# Inspect image details
docker inspect <image_name>

# View image history
docker history <image_name>

# Tag an image
docker tag <source_image> <target_image>:<tag>
```

## Networking

```bash
# List networks
docker network ls

# Create a network
docker network create <network_name>

# Connect container to network
docker network connect <network_name> <container_name>

# Run container on specific network
docker run --network <network_name> <image_name>

# Use host network
docker run --network host <image_name>
```

## Volumes and Data

```bash
# Create a volume
docker volume create <volume_name>

# List volumes
docker volume ls

# Remove a volume
docker volume rm <volume_name>

# Remove unused volumes
docker volume prune

# Mount a volume
docker run -v <volume_name>:/path/in/container <image_name>

# Mount a host directory (bind mount)
docker run -v /host/path:/container/path <image_name>

# Mount current directory
docker run -v $(pwd):/app <image_name>
```

## Executing Commands

```bash
# Execute command in running container
docker exec <container_name> <command>

# Execute interactive bash session
docker exec -it <container_name> /bin/lsbash

# Execute as different user
docker exec -u <username> <container_name> <command>
```

## Logs and Monitoring

```bash
# View container logs
docker logs <container_name>

# Follow log output (like tail -f)
docker logs -f <container_name>

# View last 100 lines
docker logs --tail 100 <container_name>

# View logs with timestamps
docker logs -t <container_name>

# View container resource usage
docker stats

# View specific container stats
docker stats <container_name>

# Inspect container details
docker inspect <container_name>
```

## Port Mapping

```bash
# Map single port
docker run -p 8080:80 <image_name>

# Map multiple ports
docker run -p 8080:80 -p 3306:3306 <image_name>

# Map all exposed ports to random host ports
docker run -P <image_name>

# List port mappings
docker port <container_name>
```

## Environment Variables

```bash
# Set single environment variable
docker run -e VAR_NAME=value <image_name>

# Set multiple environment variables
docker run -e VAR1=value1 -e VAR2=value2 <image_name>

# Load from environment file
docker run --env-file .env <image_name>
```

## Docker Compose

```bash
# Start services defined in docker-compose.yml
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View service logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Build/rebuild services
docker-compose build

# List running services
docker-compose ps

# Execute command in service
docker-compose exec <service_name> <command>
```

## System Management

```bash
# Show Docker disk usage
docker system df

# Remove all unused data (containers, images, networks)
docker system prune

# Remove all unused data including volumes
docker system prune -a --volumes

# Show Docker version
docker version

# Show Docker system information
docker info
```

## Dockerfile Instructions

```dockerfile
# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY source destination

# Run commands during build
RUN pip install -r requirements.txt

# Set environment variables
ENV APP_ENV=production

# Expose ports
EXPOSE 8080

# Set default command
CMD ["python", "app.py"]

# Set entrypoint
ENTRYPOINT ["python"]

# Add metadata
LABEL maintainer="you@example.com"

# Create mount point
VOLUME ["/data"]

# Set user
USER appuser
```

## Common Patterns for Data Engineering

### Run PostgreSQL
```bash
docker run --name postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  -d postgres:15
```

### Run Python Script with Data
```bash
docker run --rm \
  -v $(pwd)/data:/data \
  -v $(pwd)/scripts:/app \
  python:3.11 python /app/script.py
```

### Build and Run ETL Pipeline
```bash
# Build
docker build -t my-etl .

# Run
docker run --rm \
  --network host \
  -v $(pwd)/data:/data \
  -e DATABASE_URL=postgresql://user:pass@localhost:5432/db \
  my-etl
```

## Troubleshooting

```bash
# View container logs for debugging
docker logs <container_name>

# Access container shell for debugging
docker exec -it <container_name> /bin/bash

# Check if container is running
docker ps | grep <container_name>

# View detailed error messages
docker inspect <container_name> | grep -A 10 Error

# Check resource usage
docker stats <container_name>

# Force remove stuck container
docker rm -f <container_name>
```

## Best Practices

1. **Always use specific version tags**
   - DO     `FROM python:3.11-slim`
   - DON'T  `FROM python:latest`

2. **Order Dockerfile by change frequency**
   - Dependencies first (change rarely)
   - Code last (changes often)

3. **Use .dockerignore**
   - Exclude unnecessary files
   - Reduces build context size

4. **Minimize layers**
   - Combine RUN commands
   - Clean up in same layer

5. **Use volumes for data**
   - Never store data in containers
   - Data persists across container restarts

6. **Use environment variables**
   - Never hardcode credentials
   - Use .env files

7. **Tag your images**
   - Use meaningful names
   - Include version numbers

## Quick Workflow

```bash
# 1. Create project files
mkdir my-project && cd my-project
# Create Dockerfile, requirements.txt, code files

# 2. Build image
docker build -t my-app:v1 .

# 3. Run container
docker run -d --name my-app-container my-app:v1

# 4. Check logs
docker logs my-app-container

# 5. Access container
docker exec -it my-app-container bash

# 6. Stop and clean up
docker stop my-app-container
docker rm my-app-container
```

## Resources

- Docker Documentation: https://docs.docker.com
- Docker Hub: https://hub.docker.com
- Play with Docker: https://labs.play-with-docker.com
