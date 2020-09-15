# -*- coding: utf-8 -*-

name = "usd"

# Vendor packages: <vendor_version>+local.<our_version>
__version__ = "20.08"
version = __version__ + "+local.1.0.0"

description = "Pixar Universal Scene Description."

authors = ["Pixar", "Joseph Yu"]

variants = [
    ["platform-linux", "arch-x86_64", "python-2.7"],
    # ["platform-linux", "arch-x86_64", "python-3.7"],
]


@late()
def tools():
    import os

    bin_path = os.path.join(str(this.root), "bin")
    executables = []
    for item in os.listdir(bin_path):
        path = os.path.join(bin_path, item)
        if os.access(path, os.X_OK) and not os.path.isdir(path):
            executables.append(item)
    return executables


build_command = r"""
set -euf -o pipefail

# Setup "{CONTAINER_OPTS}"
CONTAINER_OPTS=()
[ -t 1 ] && CONTAINER_OPTS+=("--tty") || :
CONTAINER_OPTS+=("--workdir" "/usr/local/src")
CONTAINER_OPTS+=("--entrypoint" "/entrypoint.sh")
CONTAINER_OPTS+=("--env" "VERSION={version}")
CONTAINER_OPTS+=("--env" "PYTHON_VERSION=$REZ_PYTHON_MAJOR_VERSION"."$REZ_PYTHON_MINOR_VERSION")
CONTAINER_OPTS+=("--env" "INSTALL_DIR={INSTALL_PATH}")
CONTAINER_OPTS+=("aswf/ci-usd")

# Additional USD features, see output of:
# python <GitHubUSD>/build_scripts/build_usd.py --help
CONTAINER_OPTS+=(--alembic)
CONTAINER_OPTS+=(--opencolorio)
CONTAINER_OPTS+=(--openimageio)
CONTAINER_OPTS+=(--materialx)
CONTAINER_OPTS+=(--openvdb)

if [ $REZ_BUILD_INSTALL -eq 1 ]
then
    # CONTAINTER_ID=$(docker create "{CONTAINER_OPTS}" "$(cat $IID_FILE)")
    CONTAINTER_ID=$(docker create "{CONTAINER_OPTS}")
    docker cp $REZ_BUILD_SOURCE_PATH/entrypoint.sh $CONTAINTER_ID:/

    time docker start -ia "$CONTAINTER_ID"

    time docker cp $CONTAINTER_ID:{INSTALL_PATH}/. "{INSTALL_PATH}"
    time echo "Removed container $(docker rm "$CONTAINTER_ID")"
fi
""".format(
    version=__version__,
    BRACES="{{}}",
    CONTAINER_OPTS="${{CONTAINER_OPTS[@]}}",
    INSTALL_PATH="${{REZ_BUILD_INSTALL_PATH:-/usd}}",
)


def commands():
    """Commands to set up environment for ``rez env usd``"""
    import os.path

    env.PATH.append(os.path.join("{root}", "bin"))
    env.PYTHONPATH.append(os.path.join("{root}", "lib", "python"))
    env.LD_LIBRARY_PATH.append(os.path.join("{root}", "lib64"))
