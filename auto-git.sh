#!/bin/bash

MYREPO="$GITPATH"

git_check() {
  LOCAL=$(git -C "$MYREPO" rev-parse @)
  REMOTE=$(git -C "$MYREPO" rev-parse @{u})
  BASE=$(git -C "$MYREPO" merge-base @ @{u})

  git -C "$MYREPO" remote update

  if [ "$LOCAL" = "$REMOTE" ]; then
    echo "Up-to-date"
  elif [ "$LOCAL" = "$BASE" ]; then
    echo "Need to pull"
    git -C "$MYREPO" pull
  #elif [ "$REMOTE" = "$BASE" ]; then
  #  echo "Need to push"
  #  # Pushing the changes
  #  git -C "$MYREPO" push origin $(git -C "$MYREPO" rev-parse --abbrev-ref HEAD)
  #else
  #  echo "Diverged"
  #  # Pulling remote changes, merging them, and then pushing the merged changes
  #  git -C "$MYREPO" pull --rebase && git -C "$MYREPO" push
  fi
}

last_commit_msg() {
  echo
  echo "Last commit message:"
  git -C "$MYREPO" log -1 --pretty=format:"%B"
}

auto_versioning() {
  if [ "$AUTO_VERSIONING" = "true" ]; then
    python3 /app/versioning.py
    source "${MYREPO}"
    echo "Auto version to: ${MYREPO}"
  fi
}

add_date() {
  awk '{ print strftime("%Y-%m-%d %T"), $0 }'
}

git_check 2>&1 | add_date
auto_versioning 2>&1 | add_date
last_commit_msg
