FROM python:3.11
EXPOSE 8000
ARG GIT_USERNAME
ARG GIT_PASSWORD

# Store git credendials
RUN git config --global credential.helper store; \
    echo "protocol=https\nhost=git2.gael.fr\nusername=$GIT_USERNAME\npassword=$GIT_PASSWORD" | git credential fill; \
    echo "protocol=https\nhost=git2.gael.fr\nusername=$GIT_USERNAME\npassword=$GIT_PASSWORD" | git credential approve

COPY delta /delta/app/delta
COPY ansibleworkplan /delta/app/ansibleworkplan
COPY alembic.ini log_config.json /delta/app/
COPY requirements.txt /delta/app/requirements.txt
WORKDIR /delta/app
RUN echo "deb http://ftp.fr.debian.org/debian trixie main" >> /etc/apt/sources.list
RUN apt-get update && apt-get install --no-install-recommends -y \
    libexpat1=2.6.2-1 \
    libsystemd0=256-1 \
    libsqlite3-0=3.46.0-1 ; \
    rm -fr /var/lib/apt/lists/* ; \
    apt-get clean
RUN pip install --no-cache-dir -r requirements.txt

# install operational requirements
WORKDIR /delta/app/ansibleworkplan
RUN ansible-galaxy install -r requirements.yml --force

# Revoke Git credentials
WORKDIR /root
RUN echo "protocol=https\nhost=git2.gael.fr" | git credential reject

WORKDIR /delta/app
ENTRYPOINT ["/bin/bash", "-c", "python -m delta.run.api.api"]
