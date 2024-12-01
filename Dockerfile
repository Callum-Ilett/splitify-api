# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-alpine

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /src

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy the current directory contents into the container at /src
COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the /src folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /src
USER appuser
