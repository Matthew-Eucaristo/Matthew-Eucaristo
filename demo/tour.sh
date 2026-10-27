#!/usr/bin/env bash
# Helpers for demo/tour.tape. Each tool is built from its committed HEAD (what is public)
# and runs in a child shell set up by the tool's own demo/setup.sh: a synthetic HOME with
# generated dummy data, so nothing from the real machine is shown.
# Expects the tool repos next to this one, in ../dev-tools/<tool>.
# Usage (from the repository root): source demo/tour.sh; stage fell; …; exit; stage nodekill; …

TOUR_TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../dev-tools" && pwd -P)"

stage() { # tool: opens a shell in the tool's demo workspace; `exit` returns here and cleans up
  local src demo
  src=$(mktemp -d)
  demo="$(cd /tmp && pwd -P)/$1-demo" # every family setup.sh builds its workspace here
  git -C "$TOUR_TOOLS/$1" archive HEAD | tar -x -C "$src"
  # Some setups end by exec'ing their own clean shell; the others get one here.
  (cd "$src" && source demo/setup.sh && exec bash --norc --noprofile)
  cd / && hdiutil detach -quiet "$demo/home" 2>/dev/null
  chmod -R u+w "$demo" "$src" 2>/dev/null
  rm -rf "$demo" "$src"
}
