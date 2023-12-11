# Python's Docker image.
# https://hub.docker.com/_/python
# https://wiki.debian.org/DebianReleases
FROM python:3.11-bullseye

# Project's name
ARG PROJECT_NAME=phishflood

# Environment configurations
ENV DISPLAY=":0.0"

# Create group nonroot
RUN groupadd -r nonroot

# Create user nonroot
RUN useradd -r -g nonroot -d /home/nonroot -s /bin/bash -c "Nonroot User" nonroot

# Create directories
RUN mkdir /home/nonroot
RUN mkdir -p /home/nonroot/$PROJECT_NAME
RUN chown -R nonroot /home/nonroot

# Set the workdir
WORKDIR /home/nonroot/$PROJECT_NAME

# Install apt dependencies
COPY requirements_apt.txt /home/nonroot/$PROJECT_NAME
RUN apt-get update && apt-get install --no-install-recommends -y $(cat requirements_apt.txt)

# Change USER
USER nonroot

# Install poetry and pip dependencies
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/home/nonroot/.local/bin:/home/nonroot/.poetry/bin:${PATH}"
COPY poetry.lock /home/nonroot/$PROJECT_NAME/
COPY pyproject.toml /home/nonroot/$PROJECT_NAME/
RUN poetry install

# Install the browsers
RUN playwright install

# Copy files
COPY --chown=nonroot:nonroot . /home/nonroot/$PROJECT_NAME

# Entrypoint
CMD /bin/bash entrypoint.sh