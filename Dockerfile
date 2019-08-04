# From the USD repository root folder, runm
# docker build build_scripts
# FROM centos:7
#
# ARG INSTALL_DIR=/usd
# ARG GEN_DIR
#
# WORKDIR ${INSTALL_DIR}
# RUN yum install -y \
#         # USD
#         glew-devel.x86_64 \
#         libXcursor-devel.x86_64 \
#         libXrandr-devel.x86_64 \
#         libXinerama-devel.x86_64 \
#         libXi-devel.x86_64 \
#         # PySide https://pyside.readthedocs.io/en/latest/building/linux.html
#         gcc-c++ \
#         # clang \  # Not working for CentOS
#         cmake \
#         make \
#         git \
#         phonon-devel \
#         libslt-devel \
#         libxml2-devel \
#         python-devel \
#         # libslt-python \  # Not sure if needed
#         qt-devel \
#     & curl -s https://bootstrap.pypa.io/get-pip.py | python - \
#     & wait
#
# # Building PySide can take a bloody long time
# RUN pip install --target ${INSTALL_DIR}/lib/python PyOpenGL PySide
ARG PIP_IMAGE
FROM $PIP_IMAGE

ARG VERSION
ARG INSTALL_DIR=/usd

WORKDIR /usr/local/src
RUN curl -sL https://github.com/PixarAnimationStudios/USD/archive/v${VERSION}.tar.gz \
    | tar -xz --strip-components=1

RUN GEN_DIR=${GEN_DIR:-$(mktemp -d)} \
    && mkdir -vp ${GEN_DIR}/{build,src} \
    && python build_scripts/build_usd.py -v --build ${GEN_DIR}/build --src ${GEN_DIR}/src ${INSTALL_DIR}

# Re-locate required libraries and Python packages
RUN cp -v /usr/lib64/libQt*.so.4* ${INSTALL_DIR}/lib/python/PySide/
RUN cp -v /usr/lib64/libGL*.so* ${INSTALL_DIR}/lib/

