# DockerCrewTemplate Crew

This is a template for getting CrewAI up and running in a Dockerfile.

Setup Python

# Install specific version of python
## List available Python versions
pyenv install --list 
## Install the desired Python version
pyenv install 3.11.9
# Set the Python version globally or locally:
pyenv local 3.11.9
pyenv global 3.11.9
## Verify the installation:
python --version

Setup CrewAI
# Installing CrewAI
pip install 'crewai[tools]
pip install crewai crewai-tools
## Verify Installation
pip freeze | grep crewai
## Create a requirements.txt file 
pip freeze > requirements.txt
# Create Crew project
crewai create crew <project_name>
crewai create crew docker_crew_template
# Lock and install the dependencies
cd <project_name>
cd docker_crew_template
crewai install
# Run Crew
crewai run

Setup Docker

# Dockerfile
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

Run Crew Dockefile

# stop delete the container before rebuilding it
docker stop my-app-crew_container 2>/dev/null
docker rm my-app-crew_container 2>/dev/null
# Clean up all stopped containers in one step:
docker container prune -f
# Build the Docker Image
docker build -t my-crew_app .
# Run the Docker Container
docker run -d -p 5000:5000 --name my-app-crew_container my-crew_app
# my port 5000 is in use - so using another one
docker run -d -p 5001:5000 --name my-app-crew_container my-crew_app
# view logs
docker ps -a
docker logs <container-name-or-id>
docker logs my-app-crew_container
curl http://localhost:5001



# Run application in Docker

## Run the Default Behavior (run):
docker run my-crew_app

## Run a Specific Command:
docker run my-crew_app train
docker run my-crew_app replay 12345

## Testing Locally (without Docker):
python src/docker_crew_template/main.py train

## Debugging in Docker - you can run the container interactively:

docker run -it my-crew_app /bin/bash

## Once inside the container:
python src/docker_crew_template/main.py