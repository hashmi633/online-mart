# Use an official Python runtime as a parent image
FROM python:3.12

LABEL maintainer="hashmi633@gmail.com"
# Set the working directory in the container
WORKDIR /code
# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

COPY ./pyproject.toml /code/

# Configuration to avoid creating virtual environments inside the Docker container
RUN poetry config virtualenvs.create false

# Install dependencies including development ones
RUN poetry install

# Copy the current directory contents into the container at /code
COPY . /code/


# Make port 8002 available to the world outside this container
EXPOSE 8002

# Run the app. CMD can be overridden when starting the container
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0","--port","8002", "--reload"]