#!/bin/bash
set -eu -o pipefail

# Setup: curl "${CURL_FLAGS[@]}" ...
# Show progress bar if output to terminal, else silence
CURL_FLAGS=("-L")
[ -t 1 ] && CURL_FLAGS+=("-#") || CURL_FLAGS+=("-sS")

curl "${CURL_FLAGS[@]}" https://github.com/PixarAnimationStudios/USD/archive/v${VERSION}.tar.gz \
| tar -xz --strip-components=1

GEN_DIR="${GEN_DIR:-$(mktemp -d)}"
mkdir -vp "${GEN_DIR}"/{build,src}

# Point to aswf/ci-usd installed libs in /usr/local/lib
python build_scripts/build_usd.py -v \
    --build "${GEN_DIR}"/build \
    --src "${GEN_DIR}"/src \
    --inst "/usr/local" \
    "$@" \
    "${INSTALL_DIR}"

# Copy over libs
cp -r /usr/local/lib/* "${INSTALL_DIR}"/lib
cp -r /usr/local/lib64 "${INSTALL_DIR}"/lib64

# Replace shbang (1st line) with: /usr/bin/env pythonVERSION
PYTHON_VERSION="${PYTHON_VERSION:-2.7}"
for BIN_FILE in "${INSTALL_DIR}"/bin/*
do
    if [ $(file --mime-type -b "$BIN_FILE") == "text/x-python" ]
    then
        sed --in-place "1,1 s|usr.*|usr/bin/env python${PYTHON_VERSION}|" "$BIN_FILE"
    fi
done
