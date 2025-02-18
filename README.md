# Docker with Crew Template  README file

This is a template for getting CrewAI up and running in a Dockerfile.
Author: Vinod Ralh

1. Setup Python environment
2. Setup Dockerfile
3. Build and run CrewAI project using Docker commands

This uses default instructions from: https://docs.crewai.com/installation

It was inspired after watching "The Surprising Power of CrewAI in Docker"
https://youtu.be/JGID_du9-So?si=Dm_XE1vfHJOVQH3d. Thanks @TylerReedAI

ToDo: 
Replay, test, train arguments to crewai don't work

## Setup Environment
Tested on Mac Silicone

Note after you clone this repo, you need to add a .env file
If you follow these instruction you should be able to create your own clean version.

## Setup Python
Install specific version of python

You may need to install pyenv, which you can via homebrew
`brew install pyenv`

List available Python versions
`pyenv install --list `

Install the desired Python version
`pyenv install 3.11.9`

Set the Python version globally or locally:
`pyenv local 3.11.9`
`pyenv global 3.11.9`

Verify the installation:
`python --version`

## Setup CrewAI

Installing CrewAI
`pip install 'crewai[tools]`
`pip install crewai crewai-tools`

Verify Installation
`pip freeze | grep crewai`

Create a requirements.txt file 
`pip freeze > requirements.txt`

Create Crew project
`crewai create crew <project_name>`
`crewai create crew docker_crew_template`

Lock and install the dependencies
`cd <project_name>`
`cd docker_crew_template`
`crewai install`

Run Crew
`crewai run`

## Setup Docker

Note that this Dockerfile was generated using OpenAI ChatGPT4o and then modified.

```
Dockerfile
FROM python:3.11.9
# Set the working directory in the container
WORKDIR /app
# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
# Set the PYTHONPATH to include src/
ENV PYTHONPATH=/app/src
# Copy the application code
COPY . .
# Expose the app port
EXPOSE 5000
# Specify the command to run on container start
CMD ["crewai", "run"]
```

## Dockerfile

### Run CrewAI Dockerfile

Stop and delete the container before rebuilding it
`docker stop my-app-crew_container 2>/dev/null`
`docker rm my-app-crew_container 2>/dev/null`

Clean up all stopped containers in one step 
`docker container prune -f`

Build the Docker Image
`docker build -t my-crew_app .`

Run the Docker Container
`docker run -d -p 5000:5000 --name my-app-crew_container my-crew_app`

My port 5000 is in use - so using another one 5001
`docker run -d -p 5001:5000 --name my-app-crew_container my-crew_app`

### View logs
`docker ps -a`
`docker logs <container-name-or-id>`
`docker logs my-app-crew_container`
`curl http://localhost:5001`

### Run application with arguments in Docker
Note: Before running the app in export the open ai key to OPENAI_API_KEY
`export OPENAI_API_KEY="<YOUR_OPENAPI_KEY>"`

Note: Arguments such as test, train, replay aren't working as yet!

Run the Default Behavior (run):
`docker run my-crew_app`

Run a Specific Command:
`docker run my-crew_app train`
`docker run my-crew_app replay 12345`

Testing Locally (without Docker):
`python src/docker_crew_template/main.py train`

Debugging in Docker - you can run the container interactively:
`docker run -it my-crew_app /bin/bash`

Once inside the container:
`python src/docker_crew_template/main.py`

### Sample First run for the WebScraper
`docker run -it --rm -e OPENAI_API_KEY=$OPENAI_API_KEY -v /Users/praveen/Documents/projects/crewai/crewai_docker:/app --entrypoint /bin/bash my-crew_app`

#### Run the WebScraper
`python3 src/docker_crew_template/main.py run "https://www.eatnamkeen.com/"`

![sample_webscraper_run.png](screenshots/sample_webscraper_run.png)