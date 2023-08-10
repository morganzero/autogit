FROM python:3.9-slim AS base

LABEL maintainer="morganzero@sushibox.dev" \
      description="Automatic pulls and versioning" \
      name="AutoGit"

RUN apt-get update && \
    apt-get install -y git bash && \
    pip install Flask

WORKDIR /app
COPY assets autogit.sh versioning.py index.html server.py /app/
RUN chmod +x /app/autogit.sh

EXPOSE 8080

ENV GITPATH=""
ENV GITFILEPATH=""
ENV EXEC_INTERVAL=60
ENV AUTO_VERSIONING="true"

HEALTHCHECK CMD curl --fail http://localhost:8080/ || exit 1

CMD ["/bin/bash", "-c", "while true; do /app/autogit.sh 1>/dev/null 2>&1; sleep $EXEC_INTERVAL; done & python3 /app/server.py"]
