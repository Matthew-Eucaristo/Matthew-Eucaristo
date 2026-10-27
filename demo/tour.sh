#!/usr/bin/env bash
# Helpers for demo/tour.tape. Each tool is built from its committed HEAD (what is public),
# and runs against a synthetic HOME on a small disk image: the tool's own demo/setup.sh
# where it has one, a tiny fixture here otherwise. Nothing from the real machine is shown.
# Expects the tool repos next to this one, in ../dev-tools/<tool>.
# Usage (from the repository root): source demo/tour.sh; stage fell; ...; unstage

TOUR_TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../dev-tools" && pwd -P)"
TOUR_ENV=$(export -p) # each setup exports its own HOME, PATH, DEVELOPER_DIR, …; unstage puts this back

stage() { # tool
  unstage
  TOUR_SRC=$(mktemp -d)
  git -C "$TOUR_TOOLS/$1" archive HEAD | tar -x -C "$TOUR_SRC"
  cd "$TOUR_SRC" || return
  if [ -f demo/setup.sh ]; then source demo/setup.sh; else "fixture_$1"; fi
  TOUR_DEMO=$DEMO
  clear
}

unstage() {
  [ -n "$TOUR_DEMO" ] || return 0
  cd / && hdiutil detach -quiet "$TOUR_DEMO/home" 2>/dev/null
  rm -rf "$TOUR_DEMO" "$TOUR_SRC"
  local v
  for v in $(compgen -e); do unset "$v" 2>/dev/null; done
  eval "${TOUR_ENV//declare -x /export }" # export, not declare: declare inside a function is local
  unset TOUR_DEMO TOUR_SRC
}

fixture_nodekill() {
  DEMO="$(cd /tmp && pwd -P)/nodekill-tour"
  rm -rf "$DEMO" && mkdir -p "$DEMO/bin" "$DEMO/home"
  go build -trimpath -o "$DEMO/bin/nodekill" .
  hdiutil create -quiet -size 2g -fs APFS -volname demo -type SPARSE "$DEMO/home.sparseimage"
  hdiutil attach -quiet -nobrowse -mountpoint "$DEMO/home" "$DEMO/home.sparseimage"
  export HOME="$DEMO/home" GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
  export GIT_AUTHOR_NAME=demo GIT_AUTHOR_EMAIL=demo@example.com GIT_COMMITTER_NAME=demo GIT_COMMITTER_EMAIL=demo@example.com
  blob() { mkdir -p "$1" && dd if=/dev/urandom of="$1/blob" bs=1048576 count="$2" status=none; }
  project() { # dir days_idle framework-dirs:MB...
    local dir="$HOME/dev/$1" days=$2; shift 2
    mkdir -p "$dir" && git init -q -b main "$dir"
    printf '{"name":"%s","dependencies":{"next":"16.0.0"}}\n' "$1" > "$dir/package.json"
    printf 'node_modules/\n.next/\ndist/\n' > "$dir/.gitignore"
    touch "$dir/package-lock.json"
    local when; when=$(date -u -v-"$days"d +%Y-%m-%dT%H:%M:%SZ)
    git -C "$dir" add . && GIT_AUTHOR_DATE=$when GIT_COMMITTER_DATE=$when git -C "$dir" commit -q -m init
    for a in "$@"; do blob "$dir/${a%%:*}" "${a##*:}"; done
    find "$dir" -exec touch -h -t "$(date -v-"$days"d +%Y%m%d%H%M)" {} +
  }
  project shop 95 node_modules:180 .next:120
  project dashboard 0 node_modules:150
  project landing 40 node_modules:90 dist:20
  for v in v18.20.8:150 v20.19.5:60 v22.21.0:70; do # version:days since last run
    mkdir -p "$HOME/.nvm/versions/node/${v%%:*}/bin"
    dd if=/dev/urandom of="$HOME/.nvm/versions/node/${v%%:*}/bin/node" bs=1048576 count=60 status=none
    touch -t "$(date -v-"${v##*:}"d +%Y%m%d%H%M)" "$HOME/.nvm/versions/node/${v%%:*}/bin/node"
  done
  mkdir -p "$HOME/.nvm/alias" && echo v22.21.0 > "$HOME/.nvm/alias/default"
  : > "$HOME/.nvm/nvm.sh" # nodekill only shows the nvm command; the dry run never calls it
  export PATH="$DEMO/bin:/usr/bin:/bin" PS1='$ '
  unset NVM_DIR XDG_CACHE_HOME XDG_DATA_HOME npm_config_cache
  cd "$HOME"
}
