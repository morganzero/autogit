FROM python:3.9-slim AS base

LABEL maintainer="morganzero@sushibox.dev"
LABEL description="Automatic pulls and versioning"
LABEL name="AutoGit"

RUN apt-get update && \
    apt-get install -y git bash && \
    pip install Flask

FROM base AS build
WORKDIR /app
COPY assets auto-git.sh versioning.py index.html server.py /app/
RUN chmod +x /app/auto-git.sh

FROM base AS final
WORKDIR /app
COPY --from=build /app /app/
EXPOSE 8080

ENV GITPATH=""
ENV GITFILEPATH=""
ENV EXEC_INTERVAL=60
ENV AUTO_VERSIONING="true"

HEALTHCHECK CMD curl --fail http://localhost:8080/ || exit 1

CMD ["/bin/bash", "-c", "while true; do /app/auto-git.sh 1>/dev/null 2>&1; sleep $EXEC_INTERVAL; done & python3 /app/server.py"]
