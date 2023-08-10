
#!/bin/bash

MYREPO="$GITPATH"

auto_versioning() {
    if [ "$AUTO_VERSIONING" = "true" ]; then
        python3 /app/versioning.py "$MYREPO" "$MYFILE"
        echo "Auto versioning applied to: $MYREPO"
        git -C "$MYREPO" add "$MYFILE"
        git -C "$MYREPO" commit -m "Auto-versioning applied"
        git -C "$MYREPO" push
    fi
}

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
        auto_versioning
    fi
}

last_commit_msg() {
    echo
    echo "Last commit-message:"
    git -C "$MYREPO" log -1 --pretty=format:"%B"
}

add_date() {
    awk '{ print strftime("%Y-%m-%d %T"), $0 }'
}
    
git_check 2>&1 | add_date
last_commit_msg
