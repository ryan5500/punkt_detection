FROM ubuntu:latest


# Install pip
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


# Install conda

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh \
  && wget --quiet https://repo.continuum.io/miniconda/Miniconda2-4.3.27-Linux-x86_64.sh -O ~/miniconda.sh \
  && /bin/bash ~/miniconda.sh -b -p /opt/conda \
  && rm ~/miniconda.sh

RUN apt-get install -y curl grep sed dpkg \
  && TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` \
  && curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb \
  && dpkg -i tini.deb \
  && rm tini.deb \
  && apt-get clean

ENV PATH /opt/conda/bin:$PATH


## Create conda environment
RUN conda create -n jupyterenv python=3.5 numpy jupyter \
  && /bin/bash -c "source activate jupyterenv && pip install environment_kernels && jupyter notebook --generate-config --allow-root" \
  && echo "c.EnvironmentKernelSpecManager.conda_env_dirs = [ '/opt/conda/envs/' ]" >> ~/.jupyter/jupyter_notebook_config.py

RUN echo "source activate jupyterenv" >> ~/.profile

ENTRYPOINT [ "/usr/bin/tini", "--" ]
