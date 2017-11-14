FROM python:latest


# Install KenLM (Query only)
RUN  git clone https://github.com/kpu/kenlm.git \
  && cd kenlm \
  && /bin/bash -c "source activate jupyterenv && ./compile_query_only.sh && pip install https://github.com/kpu/kenlm/archive/master.zip" \
  && export "KENLM=/kenlm" >> ~/.profile \
  && export "PATH=$PATH:$KENLM=/bin" >> ~/.profile


# Setup MeCab
ENV MECAB_VERSION 0.996
ENV IPADIC_VERSION 2.7.0-20070801
ENV mecab_url https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE
ENV ipadic_url https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM
RUN set -ex \
  && buildDeps='g++ xz-utils file' \
  && apt-get update && apt-get install -y $buildDeps --no-install-recommends && rm -rf /var/lib/apt/lists/* \
  && wget -O mecab-${MECAB_VERSION}.tar.gz ${mecab_url} \
  && tar zxf mecab-${MECAB_VERSION}.tar.gz \
  && cd mecab-${MECAB_VERSION} \
  && ./configure --enable-utf8-only --with-charset=utf8 \
  && make \
  && make install \
  && cd \
  && ldconfig \
  && wget -O mecab-ipadic-${IPADIC_VERSION}.tar.gz ${ipadic_url} \
  && tar zxf mecab-ipadic-${IPADIC_VERSION}.tar.gz \
  && cd mecab-ipadic-${IPADIC_VERSION} \
  && ./configure --with-charset=utf8 \
  && make \
  && make install \
  && cd \
  && rm -rf mecab-${MECAB_VERSION}* mecab-ipadic*

RUN  /bin/bash -c "source activate jupyterenv && pip install mecab-python3"


## /data is supporsed to be mounted on punkt_detection/data on the host
## model file is manually downloaded to punkt_detection/data
RUN git clone https://github.com/kzinmr/punkt_detection.git \
    && cd punkt_detection \
    && mkdir data

CMD ["/bin/bash"]
