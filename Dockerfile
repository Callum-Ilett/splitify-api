# Use a specific base image tag for better predictability and multi-arch support
FROM python:3.12-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set working directory to /app
WORKDIR /app

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy everything except what's in the .dockerignore file
COPY . .

# Make scripts/entrypoint.sh executable
RUN chmod +x ./scripts/entrypoint.sh

# Expose the port that the application listens on
EXPOSE 8000

# Run the entrypoint script
ENTRYPOINT [ "./scripts/entrypoint.sh" ]
