<div align="center">
  <img src="assets/logo.png" width="250" />
  <br/>

# AutoGit
A minimal Docker container for auto Git pull, simple auto versioning and easy access to Docker logs via a simple web server.

</div>

---
Project Description:

This project provides a minimal Docker container that automatically keeps a Git repository up-to-date and serves its logs through a simple web frontend. The container runs an auto-git script to check for updates and a Flask web server to display logs on port 8080. Users can configure the Git repository path using an environment variable (GITPATH) and access logs via the web frontend.

Key Features:

    Automatic Git repository updates.
    Automatic simple versioning (patch, minor, major)
    Logs served through a simple web frontend.
    Configurable Git repository path using GITPATH environment variable.

Usage:

    Build the Docker container using the provided Dockerfile.
    Run the container, specifying the desired Git repository path using the GITPATH environment variable.
    Access the logs by visiting http://localhost:8080 in your web browser or using an HTTP client.

Deploy with docker:

```yaml
version: "3.9"
services:
  autogit:
    container_name: autogit
    image: docker.io/sushibox/autogit:latest
    restart: always
    ports:
      - "8080:8080"
    environment:
      - GITPATH=/opt/github/repo  # Change this to the desired GITPATH
      - EXEC_INTERVAL=60  # Change this to the desired auto-git script interval in seconds
    volumes:
      - "/etc/timezone:/etc/timezone:ro"
      - "/etc/localtime:/etc/localtime:ro"
      - ".logs:/var/logs"  # Change this to the desired log directory path
```

```bash
docker run -d --name autogit \
  -p 8080:8080 \
  -e GITPATH=/opt/github/repo \
  -e EXEC_INTERVAL=60 \
  -v /etc/timezone:/etc/timezone:ro \
  -v /etc/localtime:/etc/localtime:ro \
  -v .logs:/var/logs \
  docker.io/sushibox/autogit:latest
```

Note:

Using a reverse proxy, such as Traefik, Nginx, Caddy, or Apache, is recommended when deploying the container in production. A reverse proxy provides advanced features like SSL termination, load balancing, automatic certificate management, and easy integration with Docker. It enhances the overall web server setup, adding security and improved performance.

Example Docker Compose with Traefik v2:

```yaml
version: "3.9"
services:
  autogit:
    image: docker.io/sushibox/autogit:latest
    container_name: autogit
    restart: always
    environment:
      - GITPATH=/opt/github/repo  # Change this to the desired GITPATH
      - EXEC_INTERVAL=60  # Change this to the desired auto-git script interval in seconds
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.autogit.rule=Host(`autogit.example.com`)"  # Replace with your domain
      - "traefik.http.routers.autogit.entrypoints=websecure"
    volumes:
      - "/etc/timezone:/etc/timezone:ro"
      - "/etc/localtime:/etc/localtime:ro"
      - ".logs:/var/logs"
```
