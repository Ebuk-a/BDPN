# 🐳 Docker Introduction Session - Complete Materials


##  Contents

### Main Teaching Material
- **`docker_session_material.md`** 

### Code Examples
- **`etl_script.py`** - Simple ETL script for basic exercises
- **`etl_complete.py`** - Advanced ETL script with logging and error handling
- **`requirements.txt`** - Python dependencies
- **`Dockerfile`** - Example Dockerfile for building data pipeline image
- **`docker-compose.yml`** - Multi-container setup example
- **`.dockerignore`** - Files to exclude from Docker builds
- **`.env.template`** - Template for environment variables

### Student Resources
- **`docker_cheat_sheet.md`** - Quick reference guide for Docker commands
- **`sample_data.csv`** - Sample data for exercises

##  Quick Start

### Before the Session

1. **Install Docker Desktop** on your teaching machine
2. **Test all examples** to ensure they work
3. **Pull required images** to avoid download time during class:
   ```bash
   docker pull python:3.11
   docker pull postgres:15
   ```
4. **Print or share** the cheat sheet with students

### Session Flow

Follow the structure in `docker_session_material.md`:

1. **Part 1**: Theory and concepts
2. **Part 2**: Hands-on basics
3. **Part 3**: Building custom images - students do exercises
4. **Part 4**: Real-world applications and next steps
5. **Wrap-up**: Q&A


##  For Students

### Prerequisites

- Basic command line knowledge
- Python basics (covered in Week 6)
- SQL fundamentals (covered in Weeks 1-4)

### What You'll Learn

- What Docker is and why it matters
- How to run containers
- How to create your own Docker images
- How to use Docker for data engineering workflows

### Getting Started

1. **Install Docker Desktop**
   - Windows/Mac: Download from docker.com
   - Linux: Follow Docker installation guide

2. **Verify Installation**
   ```bash
   docker --version
   docker run hello-world
   ```

3. **Download Session Materials**
   - Get all files from this folder
   - Keep the cheat sheet handy

### After the Session

Practice by:
1. Containerizing your Python scripts from previous weeks
2. Running PostgreSQL in Docker for your projects
3. Building a complete ETL pipeline using Docker

##  Exercises

### Exercise 1: First Container (5 minutes)
Run a Python container and explore isolation:
```bash
docker run -it python:3.11 bash
echo "Hello Docker" > test.txt
exit
docker ps -a
```

### Exercise 2: PostgreSQL Container (5 minutes)
2.1 Set up a database with data persistence:
```bash
docker run --name my-postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_DB=dataeng_db \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  -d postgres:15
```

2.2 or, if want to create and run in a custom network
```bash
docker network create dataeng-network
```

```bash
docker run -d --name my-postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_DB=dataeng_db \
  --network dataeng-network \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15
```

### Exercise 3: Build Data Pipeline (20 minutes)
Complete ETL pipeline project:

1. Create project directory:
   ```bash
   mkdir docker-pipeline
   cd docker-pipeline
   ```

2. Copy files:
   - `Dockerfile`
   - `requirements.txt`
   - `etl_script.py`
   - `sample_data.csv`

3. Build image:
   ```bash
   docker build -t data-pipeline .
   ```

4. Run pipeline:
   ```bash
   docker run --rm \
     --network host \
     -v $(pwd)/sample_data.csv:/data/sample_data.csv \
     data-pipeline
   ```

   or If using custom network from Excercise 2.2 , Run Pipeline on same custom network
   ```bash
   docker run --rm \
   --network dataeng-network \
   -v $(pwd)/sample_data.csv:/data/sample_data.csv \
   -e DATABASE_URL=postgresql://postgres:mysecretpassword@my-postgres:5432/dataeng_db \
   data-pipeline
   ```

5. Verify results in PostgreSQL

##  Real-World Use Cases

### Local Development
```bash
# Start your development database
docker run -d --name dev-postgres \
  -e POSTGRES_PASSWORD=dev \
  -p 5432:5432 \
  postgres:15

# Develop your pipeline
# No need to install PostgreSQL on your machine!
```

### Testing
```bash
# Test against different database versions
docker run -d -p 5432:5432 postgres:14
docker run -d -p 5433:5432 postgres:15
```

### Team Collaboration
```yaml
# Share docker-compose.yml with team
# Everyone gets identical environment
docker-compose up
```

## 🔧 Troubleshooting

### Docker Won't Start
- **Windows**: Ensure WSL2 is installed
- **Mac**: Check if virtualization is enabled
- **Linux**: Check Docker daemon status

### Permission Denied Errors
```bash
# Linux/Mac
sudo usermod -aG docker $USER
# Then log out and back in
```

### Container Can't Connect to Database
- Use `--network host` for simplicity
- Or create a custom network:
  ```bash
  docker network create mynetwork
  docker run --network mynetwork ...
  ```

### Port Already in Use
```bash
# Find what's using the port
lsof -i :5432

# Use a different port
docker run -p 5433:5432 postgres:15
```

## 📖 Additional Resources

### Documentation
- [Docker Official Docs](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)

### Practice
- [Play with Docker](https://labs.play-with-docker.com/) - Browser-based practice
- [Docker Getting Started Tutorial](https://docs.docker.com/get-started/)

### Next Steps
- Learn Docker Compose in depth
- Explore Docker networking
- Study Kubernetes basics
- Understand Docker security

##  Connection to Course

This Docker session prepares you for:

- **Week 12**: Introduction to ETL with Python, SQL, and AWS
- **Weeks 13-14**: Full ETL pipeline development
- **Weeks 15-16**: Design patterns for data engineering

Docker is essential for all upcoming topics!

##  Frequently Asked Questions

### When should I use Docker?
Use Docker when you need:
- Consistent environments across machines
- Easy database setup for development
- Deployment to cloud platforms
- Isolation between projects

### Docker vs Virtual Environment?
- **Virtual Environment**: For simple Python dependency isolation
- **Docker**: When you need databases, multiple services, or production parity


##  Homework 

After the session, try these:

1. **Basic**: Run a MySQL container and connect to it
2. **Intermediate**: Containerize a Python script from previous weeks
3. **Advanced**: Create a docker-compose.yml with PostgreSQL and your ETL pipeline

##  Tips for Success

1. **Start simple** - master basic containers first
2. **Practice regularly** - use Docker for all your projects
3. **Read error messages** - they're usually helpful
4. **Use the cheat sheet** - keep it handy
5. **Ask questions** - Docker community is helpful

##  Support

If you have questions after the session:
- Check the cheat sheet first
- Review the session material
- Search Docker documentation

---

**Session**: Introduction to Docker


Good luck with Docker! 🐳
