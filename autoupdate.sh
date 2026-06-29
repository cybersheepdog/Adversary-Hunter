#!/bin/bash
#
# Weekly unattended update for Adversary Hunter.
#
# Authentication: this pushes over HTTPS using a GitHub Personal Access Token
# cached by git's credential store. Run the one-time setup ONCE as the same
# user that owns the cron job, then this script needs no interaction:
#
#   git remote set-url origin https://github.com/cybersheepdog/Adversary-Hunter.git
#   git config --global credential.helper store
#   git push            # Username: <your GitHub user>   Password: <paste the PAT>
#   chmod 600 ~/.git-credentials
#
# Use a fine-grained PAT scoped to this repo with "Contents: Read and write".
# (Use 'store', not 'cache' -- the cache helper expires and would break a
# weekly job. Rotate the token before it expires.)

set -u

# cron runs with a minimal environment. Run from the repo dir regardless of the
# caller's working directory, and make sure git can find ~/.gitconfig and
# ~/.git-credentials.
cd "$(dirname "$0")" || exit 1
export HOME="${HOME:-$(getent passwd "$(id -u)" | cut -d: -f6)}"

# Never block on a username/password prompt in an unattended run. If the stored
# token is missing or expired, fail fast instead of hanging the cron job forever.
export GIT_TERMINAL_PROMPT=0

git pull || exit 1
python3 hunter.py || exit 1

git add .
find . -size 0c -delete

# Only commit/push when something actually changed, so a no-change week doesn't
# look like a failure.
if git diff --cached --quiet && git diff --quiet; then
    echo "No changes to commit."
else
    git commit -a -m "Weekly Auto Update" && git push
fi
