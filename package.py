name = 'usd'

version = '19.07'

build_command = '''
set -eu -o pipefail

cp -v $REZ_BUILD_SOURCE_PATH/Dockerfile* .
docker build --rm \
    --build-arg VERSION={version} \
    --build-arg INSTALL_DIR={install_dir} \
    --build-arg PIP_IMAGE=$(docker build --rm \
        --quiet \
        -f Dockerfile-pip \
        --build-arg YUM_IMAGE=$(docker build --rm \
            --quiet \
            -f Dockerfile-yum \
            -t local/usd-yum .) \
        --build-arg INSTALL_DIR={install_dir} \
        -t local/usd-pip .) \
    -t local/usd .

if [ $REZ_BUILD_INSTALL -eq 1 ]
then
    CONTAINTER_ID=$(docker run --rm -td local/usd)
    docker cp $CONTAINTER_ID:{install_dir}/. {install_dir}
    docker stop $CONTAINTER_ID
fi
'''.format(
    version=version,
    install_dir='${{REZ_BUILD_INSTALL_PATH:-/usd}}',
)


def commands():
    import os.path
    env.PATH.append(os.path.join('{root}', 'bin'))
    env.PYTHONPATH.append(os.path.join('{root}', 'lib', 'python'))


@late()
def tools():
    import os
    bin_path = os.path.join(str(this.root), 'bin')
    return os.listdir(bin_path)

