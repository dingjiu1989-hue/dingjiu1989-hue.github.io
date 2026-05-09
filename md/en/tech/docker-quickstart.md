---
title: "Docker in 30 Minutes: From Install to First Container"
description: "A hands-on Docker tutorial for absolute beginners. Learn images, containers, and Dockerfiles by building and running your first containerized app."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/docker-quickstart.html
---

# Docker in 30 Minutes: From Install to First Container

Docker lets you package your application with everything it needs into a lightweight container that runs anywhere. No more "it works on my machine." Let's get you from zero to a running container in 30 minutes.

## What Problem Does Docker Solve?

Before Docker: you install Python 3.11, your teammate uses 3.10, the server runs 3.9. Your app uses PostgreSQL 15, but production is on 14. Dependency hell. Docker wraps your app AND its exact environment into one portable unit — a container.

## Installation

Download **Docker Desktop** from [docker.com](<https://docker.com/products/docker-desktop>). It includes Docker Engine, CLI, Docker Compose, and a GUI dashboard. Verify:
    
    
    docker --version
    docker run hello-world   # should print a welcome message

## Core Concepts

Concept| What It Is| Analogy  
---|---|---  
**Image**|  A blueprint — the files, dependencies, and config| A recipe  
**Container**|  A running instance of an image| The dish you cooked  
**Dockerfile**|  Instructions to build an image| The recipe card  
**Docker Hub**|  Public registry of images| GitHub for container images  
**Volume**|  Persistent storage outside the container| An external hard drive  
  
## Your First Container
    
    
    # Run nginx web server in a container
    docker run -d -p 8080:80 --name my-nginx nginx
    
    # Visit http://localhost:8080 — you'll see the nginx welcome page!
    
    # What's running?
    docker ps
    
    # Stop it
    docker stop my-nginx
    
    # Remove it
    docker rm my-nginx

## Writing a Dockerfile

Create a simple Python app:
    
    
    # app.py
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return 'Hello from Docker!'
    
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
    
    
    # Dockerfile
    FROM python:3.12-slim          # start from a Python image
    WORKDIR /app                    # set working directory
    COPY requirements.txt .         # copy dependency list
    RUN pip install -r requirements.txt
    COPY . .                        # copy everything else
    EXPOSE 5000                     # document what port we use
    CMD ["python", "app.py"]        # what to run on start
    
    
    # requirements.txt
    flask==3.1.0
    
    
    # Build and run
    docker build -t my-python-app .
    docker run -d -p 5000:5000 my-python-app

## Essential Commands
    
    
    docker ps                  # list running containers
    docker ps -a               # list ALL containers
    docker images              # list images
    docker logs <container>    # view logs
    docker exec -it <c> bash   # shell into a running container
    docker rm <container>      # remove a container
    docker rmi <image>         # remove an image
    docker system prune -a     # clean up everything unused

## Docker Compose (Multi-Container Apps)
    
    
    # docker-compose.yml
    version: '3.8'
    services:
      web:
        build: .
        ports:
          - "5000:5000"
        depends_on:
          - db
      db:
        image: postgres:16
        environment:
          POSTGRES_PASSWORD: secret
        volumes:
          - pgdata:/var/lib/postgresql/data
    
    volumes:
      pgdata:
    
    
    docker compose up -d       # start everything
    docker compose down        # stop everything

## Docker vs VM

Containers share the host OS kernel, so they start in milliseconds and use minimal RAM. VMs each need their own OS, taking gigabytes. For most web apps, Docker is the clear winner.

**See also:** [Python Tutorial: From Zero to Your First Program](</en/tech/python-tutorial.html>), [DevOps for Developers: CI/CD, Docker, IaC, and Monitoring — A Practical Guide](</en/tech/devops-for-developers.html>), [Kubernetes vs Docker Swarm vs Nomad (2026): Container Orchestration Compared](</en/compare/kubernetes-vs-docker-swarm-vs-nomad.html>).
