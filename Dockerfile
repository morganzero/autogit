FROM alpine:latest

LABEL maintainer="morganzero@sushibox.dev" \
      description="Automatic pulls and versioning" \
      name="AutoGit"

RUN apk --no-cache add git bash python3 py3-pip && rm -rf /var/cache/apk/*

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip3 install flask && \
    rm -rf /var/cache/apk/*

WORKDIR /app

COPY . /app/

RUN chmod +x /app/auto-git.sh

EXPOSE 8080

ENV GITPATH=""
ENV GITFILEPATH=""
ENV EXEC_INTERVAL=60
ENV AUTO_VERSIONING="true"

CMD ["/bin/bash", "-c", "while true; do /app/auto-git.sh 1>/dev/null 2>&1; sleep $EXEC_INTERVAL; done & python3 /app/server.py"]
