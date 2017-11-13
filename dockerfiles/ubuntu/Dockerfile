## FROM docker-brew-ubuntu-core/xenial/Dockerfile
FROM ubuntu:16.04

# a few minor docker-specific tweaks
# see https://github.com/docker/docker/blob/9a9fc01af8fb5d98b8eec0740716226fadb3735c/contrib/mkimage/debootstrap
RUN set -xe \
  \
  && echo '#!/bin/sh' > /usr/sbin/policy-rc.d \
  && echo 'exit 101' >> /usr/sbin/policy-rc.d \
  && chmod +x /usr/sbin/policy-rc.d \
  \
  && dpkg-divert --local --rename --add /sbin/initctl \
  && cp -a /usr/sbin/policy-rc.d /sbin/initctl \
  && sed -i 's/^exit.*/exit 0/' /sbin/initctl \
  \
  && echo 'force-unsafe-io' > /etc/dpkg/dpkg.cfg.d/docker-apt-speedup \
  \
  && echo 'DPkg::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' > /etc/apt/apt.conf.d/docker-clean \
  && echo 'APT::Update::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' >> /etc/apt/apt.conf.d/docker-clean \
  && echo 'Dir::Cache::pkgcache ""; Dir::Cache::srcpkgcache "";' >> /etc/apt/apt.conf.d/docker-clean \
  \
  && echo 'Acquire::Languages "none";' > /etc/apt/apt.conf.d/docker-no-languages \
  \
  && echo 'Acquire::GzipIndexes "true"; Acquire::CompressionTypes::Order:: "gz";' > /etc/apt/apt.conf.d/docker-gzip-indexes \
  \
  && echo 'Apt::AutoRemove::SuggestsImportant "false";' > /etc/apt/apt.conf.d/docker-autoremove-suggests

# delete all the apt list files since they're big and get stale quickly
RUN rm -rf /var/lib/apt/lists/*
# this forces "apt-get update" in dependent images, which is also good

# enable the universe
RUN sed -i 's/^#\s*\(deb.*universe\)$/\1/g' /etc/apt/sources.list

# make systemd-detect-virt return "docker"
# See: https://github.com/systemd/systemd/blob/aa0c34279ee40bce2f9681b496922dedbadfca19/src/basic/virt.c#L434
RUN mkdir -p /run/systemd && echo 'docker' > /run/systemd/container



RUN set -ex \
  && buildDeps=' \
    autoconf \
    build-essential \
    ca-certificates \
    gcc \
    g++ \
    make \
    git \
    pkg-config \
    wget \
    curl \
    bzip2 \
    libbz2-dev \
    libpq-dev \
  ' \
  && apt-get update && apt-get install -y $buildDeps --no-install-recommends && rm -rf /var/lib/apt/lists/*


## FROM docker-library/python/3.5/Dockerfile
# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tcl \
    tk \
  && rm -rf /var/lib/apt/lists/*

ENV GPG_KEY 97FC712E4C024BBEA48A61ED3A5CA953F73C700D
ENV PYTHON_VERSION 3.5.3

RUN set -ex \
  && buildDeps=' \
    dpkg-dev \
    tcl-dev \
    tk-dev \
  ' \
  && apt-get update && apt-get install -y $buildDeps --no-install-recommends && rm -rf /var/lib/apt/lists/* \
  \
  && wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
  && wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" \
  && export GNUPGHOME="$(mktemp -d)" \
  && gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEY" \
  && gpg --batch --verify python.tar.xz.asc python.tar.xz \
  && rm -rf "$GNUPGHOME" python.tar.xz.asc \
  && mkdir -p /usr/src/python \
  && tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
  && rm python.tar.xz \
  \
  && cd /usr/src/python \
  && gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
  && ./configure \
    --build="$gnuArch" \
    --enable-loadable-sqlite-extensions \
    --enable-shared \
    --with-system-expat \
    --with-system-ffi \
    --without-ensurepip \
  && make -j "$(nproc)" \
  && make install \
  && ldconfig \
  \
  && apt-get purge -y --auto-remove $buildDeps \
  \
  && find /usr/local -depth \
    \( \
      \( -type d -a \( -name test -o -name tests \) \) \
      -o \
      \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
    \) -exec rm -rf '{}' + \
  && rm -rf /usr/src/python

# make some useful symlinks that are expected to exist
RUN cd /usr/local/bin \
  && ln -s idle3 idle \
  && ln -s pydoc3 pydoc \
  && ln -s python3 python \
  && ln -s python3-config python-config

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 9.0.1

RUN set -ex; \
  \
  wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py'; \
  \
  python get-pip.py \
    --disable-pip-version-check \
    --no-cache-dir \
    "pip==$PYTHON_PIP_VERSION" \
  ; \
  pip --version; \
  \
  find /usr/local -depth \
    \( \
      \( -type d -a \( -name test -o -name tests \) \) \
      -o \
      \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
    \) -exec rm -rf '{}' +; \
  rm -f get-pip.py

CMD ["/bin/bash"]
