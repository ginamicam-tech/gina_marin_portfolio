#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Use a modern Python for the same Pillow version used in GitHub Actions.
if [[ -z "${PYTHON:-}" ]]; then
  for candidate in python3.14 python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
      PYTHON="$candidate"
      break
    fi
  done
fi
"${PYTHON:-python3}" -c 'import sys; assert sys.version_info >= (3, 10), "Python 3.10 or newer is required"'

preview_dir=$(mktemp -d "${TMPDIR:-/tmp}/gina-optimized-preview.XXXXXX")
trap 'rm -rf "$preview_dir"' EXIT
optimizer_python="${PYTHON:-python3}"
if ! "$optimizer_python" -c 'import PIL; assert PIL.__version__ == "13.0.0"' 2>/dev/null; then
  "$optimizer_python" -m venv "$preview_dir/venv"
  optimizer_python="$preview_dir/venv/bin/python"
  "$optimizer_python" -m pip install -r scripts/image-requirements.txt
fi

if [[ -d /opt/homebrew/opt/ruby/bin ]]; then
  export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
fi
JEKYLL_ENV=production bundle exec jekyll build --baseurl "" --destination "$preview_dir/site"
"$optimizer_python" scripts/optimize-images.py "$preview_dir/site"
"$optimizer_python" scripts/validate-content.py "$preview_dir/site"
printf '\nOptimized preview: http://127.0.0.1:%s/\n' "${PORT:-4001}"
printf 'Stop with Ctrl+C. Rerun this command after editing to rebuild the preview.\n\n'
"$optimizer_python" -m http.server "${PORT:-4001}" --bind 127.0.0.1 --directory "$preview_dir/site"
