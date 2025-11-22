# Introduction to Docker for Data Engineering


**Target Audience**: Data engineering students with basic Python and SQL knowledge  
**Prerequisites**: Basic command line familiarity, Python basics  

---

## Session Objectives

By the end of this session, students will be able to:
- Explain what Docker is and why it's valuable for data engineering
- Run and manage Docker containers
- Create custom Docker images using Dockerfiles
- Use Docker for local development with databases
- Containerize simple data processing scripts

---

## Part 1: Understanding Docker 

### 1.1 What is Docker and Why Use It? 

#### The Problem Docker Solves


*Scenario*: Imagine you've built an ETL pipeline on your laptop. It works perfectly. You send it to a colleague, and they get errors. Why?

- Different Python versions
- Missing dependencies
- Different operating system
- Different database versions

**The Traditional Response**: "But it works on my machine!"

Docker solves this by packaging everything your application needs into a container.

#### Real-World Data Engineering Scenarios

1. **Development vs. Production Consistency**
   - Your local PostgreSQL is version 14, production is version 15
   - With Docker: Both run the exact same version

2. **Team Collaboration**
   - New team member needs to set up: Python, PostgreSQL, Redis, Airflow
   - Without Docker: 2-3 hours of installation and troubleshooting
   - With Docker: `docker-compose up` - 5 minutes

3. **Testing Different Environments**
   - Test your pipeline against PostgreSQL, MySQL, and SQL Server
   - Each in its own isolated container

4. **Cloud Deployment**
   - AWS, Azure, GCP all support container deployments
   - Build once, deploy anywhere

#### Virtual Machines vs. Containers

**Virtual Machines**:
- Full operating system for each VM
- Heavyweight (GBs of disk space)
- Slow to start (minutes)
- More isolated but resource-intensive

**Containers**:
- Share the host OS kernel
- Lightweight (MBs)
- Fast to start (seconds)
- Efficient resource usage

**Analogy**: 
- VM = Buying separate houses for guests
- Container = Rooms in the same building (shared infrastructure, but private spaces)

### 1.2 Core Docker Concepts 

#### Images vs. Containers

**Image**: 
- A blueprint/template
- Read-only
- Contains everything: code, runtime, libraries, dependencies
- Like a recipe

**Container**:
- A running instance of an image
- Can be started, stopped, deleted
- Like the actual meal made from the recipe

**Example**:
```
Image: python:3.11       →    Container: running Python application
Image: postgres:15       →    Container: running database
```

#### Dockerfile

A text file with instructions to build an image.

```dockerfile
# Example Dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

#### Docker Hub and Registries

- **Docker Hub**: Public repository of Docker images (like GitHub for containers)
- Thousands of official images: Python, PostgreSQL, Redis, etc.
- You can publish your own images

#### Basic Architecture

![Docker Architecture (source:geekforgeeks.org)](docker-arch.png)
(source:geekforgeeks.org)

---

## Part 2: Hands-On Docker Basics (35 minutes)

**Instructor Note**: Switch to live demo. Have students follow along on their machines.

### 2.1 First Container (15 min)

#### Verify Docker Installation

```bash
# Check Docker version
docker --version

# Check Docker is running
docker info
```

**Expected Output**:
```
Docker version 24.0.x, build...
```

**Troubleshooting**: If Docker isn't installed or running, pause here and help students get set up.

#### Running Your First Container

```bash
# Run the hello-world container
docker run hello-world
```

**What Happens**:
1. Docker checks if the image exists locally (it doesn't)
2. Downloads the image from Docker Hub
3. Creates a container from the image
4. Runs the container
5. Container prints a message and exits

**Explanation**: This is like downloading a program and running it, but completely isolated.

#### Running an Interactive Python Container

```bash
# Run Python interactively
docker run -it python:3.11 python

# You're now in a Python REPL inside a container!
>>> print("Hello from inside a container!")
>>> import sys
>>> print(sys.version)
>>> exit()
```

**Flags Explained**:
- `-it`: Interactive terminal (lets you type commands)
- `python:3.11`: The image to use
- `python`: The command to run inside the container

#### Basic Docker Commands

```bash
# List running containers
docker ps

# List all containers (including stopped ones)
docker ps -a

# List downloaded images
docker images

# Stop a running container
docker stop <container_id>

# Remove a container
docker rm <container_id>

# Remove an image
docker rmi <image_name>
```

**Exercise 1** (5 minutes):
1. Run a Python container: `docker run -it python:3.11 bash`
2. Inside the container, create a file: `echo "Hello Docker" > test.txt`
3. Exit the container: `exit`
4. Try to find that file on your host machine (you won't find it - that's isolation!)
5. List all containers: `docker ps -a`
6. Remove the container you just created

### 2.2 Working with Docker Images (20 min)

#### Running a PostgreSQL Container

This is huge for data engineering - instant database setup!

```bash
# Run PostgreSQL in a container
docker run --name my-postgres \
  -e POSTGRES_PASSWORD=mytestpassword \
  -e POSTGRES_DB=dataeng_db \
  -p 5432:5432 \
  -d postgres:15

# Verify it's running
docker ps
```

**Flags Explained**:
- `--name my-postgres`: Give the container a friendly name
- `-e`: Set environment variables (password, database name)
- `-p 5432:5432`: Map port 5432 on host to port 5432 in container
- `-d`: Run in detached mode (background)
- `postgres:15`: Use PostgreSQL version 15 image

#### Understanding Port Mapping

```
Your Computer (Host)          Docker Container
    Port 5432        ←→          Port 5432
                                 [PostgreSQL]
```

Now you can connect to PostgreSQL at `localhost:5432` as if it were installed on your machine!

#### Connect to the Database

```bash
# Execute SQL directly
docker exec -it my-postgres psql -U postgres -d dataeng_db

# You're now in psql!
# Try some commands:
dataeng_db=# \dt
dataeng_db=# CREATE TABLE test (id INT, name TEXT);
dataeng_db=# INSERT INTO test VALUES (1, 'Docker is cool');
dataeng_db=# SELECT * FROM test;
dataeng_db=# \q
```

#### Volume Mounting Basics

Problem: If you delete the container, all data is lost!

Solution: Mount a volume (directory) from your host machine into the container.

```bash
# Stop and remove the old container
docker stop my-postgres
docker rm my-postgres

# Run with a volume for data persistence
docker run --name my-postgres \
  -e POSTGRES_PASSWORD=mytestpassword \
  -e POSTGRES_DB=dataeng_db \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  -d postgres:15
```

Now your data persists even if you delete and recreate the container!

**Exercise 2** (5 minutes):
1. Create a table in the PostgreSQL container
2. Insert some data
3. Stop and remove the container
4. Start a new PostgreSQL container with the same volume
5. Verify your data is still there

---

## Part 3: Building Custom Images for Data Engineering (40 minutes)

### 3.1 Creating a Dockerfile (20 min)

#### Why Build Custom Images?

You need specific tools for your data pipeline:
- Python with pandas, psycopg2, requests
- Specific versions of libraries
- Your custom scripts
- Configuration files

#### Dockerfile Structure

Let's build a data engineering image step by step.

**Create a project directory**:
```bash
mkdir docker-data-pipeline
cd docker-data-pipeline
```

**Create `requirements.txt`**:
```txt
numpy>=2.0.0
pandas>=2.2.0
psycopg2-binary==2.9.6
sqlalchemy==2.0.21
python-dotenv==1.0.0
```

**Create `Dockerfile`**:
```dockerfile
# Start from official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set default command
CMD ["python", "etl_script.py"]
```

#### Dockerfile Instructions Explained

- `FROM`: Base image to start from
- `WORKDIR`: Set the working directory (like `cd /app`)
- `COPY`: Copy files from host to container
- `RUN`: Execute commands during build (installing packages)
- `CMD`: Default command when container starts

#### Building the Image

```bash
# Build the image
docker build -t my-data-pipeline .

# The -t flag tags/names your image
# The . tells Docker to look for Dockerfile in current directory
```

**What Happens**:
1. Docker reads the Dockerfile
2. Executes each instruction
3. Creates layers (cached for efficiency)
4. Tags the final image

```bash
# View your new image
docker images

# You should see my-data-pipeline in the list
```

#### Best Practices for Dockerfiles

**1. Use Specific Version Tags**
```dockerfile
# Good
FROM python:3.11-slim

# Bad (version can change)
FROM python:latest
```

**2. Order Instructions by Change Frequency**
```dockerfile
# Things that rarely change come first (better caching)
FROM python:3.11-slim
WORKDIR /app

# Dependencies (change sometimes)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Code (changes often) comes last
COPY . .
```

**3. Use .dockerignore**
Create a `.dockerignore` file:
```
__pycache__/
*.pyc
*.pyo
.git/
.env
venv/
*.log
```

This prevents copying unnecessary files into your image.

### 3.2 Practical Exercise (20 min)

#### Exercise 3: Build a Data Processing Container

**Scenario**: Create a container that reads a CSV file, processes it, and loads it into PostgreSQL.

**Step 1: Create the Python script**

Create `etl_script.py`:
```python
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os

def main():
    print("Starting ETL process...")
    
    # Read CSV file
    print("Reading CSV file...")
    df = pd.read_csv('/data/sample_data.csv')
    print(f"Loaded {len(df)} rows")
    
    # Simple transformation
    print("Transforming data...")
    df['processed_at'] = pd.Timestamp.now()
    
    # Connect to database
    print("Connecting to database...")
    db_url = os.getenv('DATABASE_URL', 
                       'postgresql://postgres:mytestpassword@db:5432/dataeng_db')
    engine = create_engine(db_url)
    
    # Load to database
    print("Loading to database...")
    df.to_sql('processed_data', engine, if_exists='replace', index=False)
    
    print("ETL process completed successfully!")

if __name__ == "__main__":
    main()
```

**Step 2: Create sample data**

Create `sample_data.csv`:
```csv
id,name,value,category
1,Product A,100,Electronics
2,Product B,150,Clothing
3,Product C,200,Electronics
4,Product D,75,Food
5,Product E,120,Clothing
```

**Step 3: Update Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY etl_script.py .

CMD ["python", "etl_script.py"]
```

**Step 4: Build the image**

```bash
docker build -t data-pipeline .
```

**Step 5: Run the pipeline**

```bash
# Make sure PostgreSQL container is running
docker run --name my-postgres \
  -e POSTGRES_PASSWORD=mytestpassword \
  -e POSTGRES_DB=dataeng_db \
  -p 5432:5432 \
  -d postgres:15

# Wait a few seconds for PostgreSQL to start

# Run the data pipeline
docker run --rm \
  --network host \
  -v $(pwd)/sample_data.csv:/data/sample_data.csv \
  data-pipeline
```

**Step 6: Verify the data**

```bash
docker exec -it my-postgres psql -U postgres -d dataeng_db

# In psql:
dataeng_db=# \dt
dataeng_db=# SELECT * FROM processed_data;
dataeng_db=# \q
```

#### Exercise Breakdown

Students should understand:
1. **Volume mounting** (`-v`): Shares the CSV file with the container
2. **Network** (`--network host`): Allows the container to access PostgreSQL on localhost
3. **Environment variables**: Used for database connection
4. **Container lifecycle**: `--rm` removes container after it finishes

---

## Part 4: Docker for ETL Workflows (15 minutes)

### 4.1 Real-World Applications (10 min)

#### Containerizing ETL Pipelines

**Benefits**:
1. **Reproducibility**: Pipeline runs the same everywhere
2. **Isolation**: Each pipeline has its own dependencies
3. **Scalability**: Easy to run multiple instances
4. **Version Control**: Dockerfile is code - commit it!

#### Multi-Container Setup with Docker Compose

**Instructor Note**: Quick overview - full Docker Compose is a separate session

Docker Compose lets you define multi-container applications.

**Example `docker-compose.yml`**:
```yaml
version: '3.8'

services:
  # Database
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: mytestpassword
      POSTGRES_DB: dataeng_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  # ETL Pipeline
  etl:
    build: .
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://postgres:mytestpassword@postgres:5432/dataeng_db
    volumes:
      - ./data:/data

volumes:
  postgres_data:
```

**Running it**:
```bash
# Start everything
docker-compose up

# Stop everything
docker-compose down
```

This starts both PostgreSQL and your ETL pipeline together, with proper networking!

#### Environment Variables and Configuration

**Best Practice**: Never hardcode credentials!

**Using .env file**:
```bash
# .env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=dataeng_db
DATABASE_USER=postgres
DATABASE_PASSWORD=mytestpassword
```

**In docker-compose.yml**:
```yaml
services:
  etl:
    build: .
    env_file:
      - .env
```

**In Python**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv('DATABASE_HOST')
db_port = os.getenv('DATABASE_PORT')
# etc.
```

### 4.2 Next Steps and Resources (5 min)

#### Docker in Cloud Environments

- **AWS**: ECS (Elastic Container Service), Fargate, EKS
- **Azure**: Azure Container Instances, AKS
- **GCP**: Cloud Run, GKE

Your Dockerfile works the same in all of them!

#### Connection to Upcoming Topics

In your upcoming ETL pipeline weeks, you'll:
- Build complete pipelines in Docker containers
- Use Docker Compose for local development
- Learn deployment patterns
- Integrate with AWS services

#### Learning Resources

1. **Official Docker Documentation**: docs.docker.com
2. **Docker Hub**: hub.docker.com - explore official images
3. **Practice Projects**:
   - Containerize all your Python scripts
   - Set up local databases with Docker
   - Build a simple microservices setup

#### Quick Commands Cheat Sheet

```bash
# Images
docker pull <image>          # Download an image
docker build -t <name> .     # Build image from Dockerfile
docker images                # List images
docker rmi <image>           # Remove image

# Containers
docker run <image>           # Create and start container
docker ps                    # List running containers
docker ps -a                 # List all containers
docker stop <container>      # Stop container
docker start <container>     # Start stopped container
docker rm <container>        # Remove container
docker logs <container>      # View container logs
docker exec -it <container> bash  # Access container shell

# Cleanup
docker system prune          # Remove unused data
docker system prune -a       # Remove all unused images
```

---

## Wrap-Up (5 minutes)

### Key Takeaways

1. **Docker solves the "works on my machine" problem** by packaging everything together
2. **Containers are lightweight, fast, and isolated** - perfect for development and deployment
3. **Dockerfiles are code** - version control them with your project
4. **Docker is essential for modern data engineering** - most companies use it

### Q&A

**Common Questions**:

**Q**: "When should I use Docker vs. virtual environments?"
**A**: Use virtual environments for simple Python projects on your machine. Use Docker when you need databases, multiple services, or want to ensure production consistency.

**Q**: "Isn't Docker complicated?"
**A**: It has a learning curve, but the basics we covered today handle 80% of use cases. Start simple, grow from there.

**Q**: "Do I need Docker for this course?"
**A**: Not required, but highly recommended! It'll make your life easier, especially when we get to ETL pipelines.

**Q**: "What about Windows?"
**A**: Docker Desktop works great on Windows. You might occasionally need to adjust file paths, but the concepts are identical.

### Homework (Optional)

1. **Install Docker Desktop** if you haven't already
2. **Containerize one of your Python scripts** from previous weeks
3. **Run a PostgreSQL container** and practice connecting to it
4. **Experiment**: Try running MySQL or MongoDB in containers

---

## Instructor Notes

### Timing Guidelines

- Stay flexible with timing - if students need more hands-on time, adjust accordingly
- The exercises are the most valuable part - prioritize those over theory
- If running short on time, you can skip 4.1 multi-container setup and focus on single containers

### Common Issues & Solutions

**Issue**: Docker not starting on Windows
**Solution**: Ensure WSL2 is installed and virtualization is enabled in BIOS

**Issue**: "Permission denied" errors on Mac/Linux
**Solution**: `sudo usermod -aG docker $USER` then logout/login

**Issue**: Containers can't connect to each other
**Solution**: Use `--network host` for simplicity, or create a custom network

### Demo Tips

1. **Have everything pre-installed** and tested before the session
2. **Keep a backup terminal** with working containers in case of issues
3. **Use large font** in terminal - students need to see commands clearly
4. **Type commands yourself** rather than copy-pasting - students learn better
5. **Celebrate errors** - show how to troubleshoot them

### Assessment Ideas

If you want to test understanding:
- Have students explain the difference between images and containers
- Ask them to write a Dockerfile from scratch
- Have them troubleshoot a broken container

---

## Additional Resources for Students

### Further Reading

- Docker Documentation: https://docs.docker.com/
- Docker Hub: https://hub.docker.com/
- Play with Docker (browser-based practice): https://labs.play-with-docker.com/

### Video Tutorials

- Docker official YouTube channel
- freeCodeCamp Docker course

### Practice Datasets

Students can practice with these public datasets:
- NYC Taxi Data
- COVID-19 datasets
- Kaggle datasets

### Next Steps

After mastering basic Docker:
1. Learn Docker Compose thoroughly
2. Explore Docker networking
3. Study container orchestration (Kubernetes basics)
4. Understand Docker security best practices

---

## Appendix: Complete Code Examples

### Example 1: Simple Data Processor

**Directory Structure**:
```
project/
├── Dockerfile
├── requirements.txt
├── process_data.py
└── data/
    └── input.csv
```

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY process_data.py .

CMD ["python", "process_data.py"]
```

**requirements.txt**:
```
pandas==2.1.0
```

**process_data.py**:
```python
import pandas as pd
import sys

def process_data(input_file, output_file):
    # Read data
    df = pd.read_csv(input_file)
    
    # Process (example: calculate summary statistics)
    summary = df.describe()
    
    # Save results
    summary.to_csv(output_file)
    print(f"Processed {len(df)} rows. Results saved to {output_file}")

if __name__ == "__main__":
    process_data('/data/input.csv', '/data/output.csv')
```

**Run it**:
```bash
docker build -t data-processor .
docker run --rm -v $(pwd)/data:/data data-processor
```

### Example 2: Database ETL

**etl_complete.py**:
```python
import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import datetime

def extract(csv_path):
    """Extract data from CSV"""
    print(f"Extracting data from {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"Extracted {len(df)} rows")
    return df

def transform(df):
    """Transform data"""
    print("Transforming data...")
    
    # Add timestamp
    df['loaded_at'] = datetime.now()
    
    # Data cleaning example
    df = df.dropna()
    
    # Calculate new column example
    if 'value' in df.columns:
        df['value_doubled'] = df['value'] * 2
    
    print(f"Transformation complete. {len(df)} rows remain")
    return df

def load(df, table_name, engine):
    """Load data to database"""
    print(f"Loading data to table: {table_name}")
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print("Load complete!")

def main():
    # Configuration
    csv_path = os.getenv('INPUT_CSV', '/data/input.csv')
    table_name = os.getenv('TABLE_NAME', 'processed_data')
    db_url = os.getenv('DATABASE_URL')
    
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    # ETL Process
    print("=" * 50)
    print("Starting ETL Process")
    print("=" * 50)
    
    df = extract(csv_path)
    df = transform(df)
    
    engine = create_engine(db_url)
    load(df, table_name, engine)
    
    print("=" * 50)
    print("ETL Process Complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()
```

---

## End of Session Material

**Total Pages**: Comprehensive 2-hour session guide with theory, demos, and hands-on exercises.

**Instructor**: Remember to save time for questions and troubleshooting. Docker can be tricky the first time, but once students get it, they'll love it!

**Student Feedback**: After the session, consider asking:
1. What was most confusing?
2. What was most valuable?
3. What would you like to learn more about?

Good luck with the session! 🐳
