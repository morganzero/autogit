FROM alpine:latest
LABEL maintainer="morganzero@sushibox.dev" \
      description="Automatic pulls and versioning" \
      name="AutoGit"

RUN apk --no-cache add git bash python3 py3-pip && \
    pip3 install flask && \
    rm -rf /var/cache/apk/*

WORKDIR /app
COPY assets autogit.sh versioning.py index.html server.py /app/
RUN chmod +x /app/autogit.sh

EXPOSE 8080
ENV GITPATH=""
ENV GITFILEPATH=""
ENV EXEC_INTERVAL=60
ENV AUTO_VERSIONING="true"

CMD ["/bin/bash", "-c", "while true; do /app/autogit.sh 1>/dev/null 2>&1; sleep $EXEC_INTERVAL; done & python3 /app/server.py"]
