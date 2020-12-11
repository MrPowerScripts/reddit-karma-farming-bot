FROM ubuntu:20.10

CMD ["/sbin/my_init"]
WORKDIR /reddit-karma-bot
SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      g++ \
      gcc \
      golang-go \
      libc6-dev \
      make \
      libffi-dev \
      pkg-config \
      wget \
      tmux \
      python3.6 \
      python3-pip \
      python3-setuptools \
      python3-dev \
      git \
      ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# # set up gotty
# RUN mkdir -p /tmp/gotty \
#   && GOPATH=/tmp/gotty go get github.com/yudai/gotty \
#   && mv /tmp/gotty/bin/gotty /usr/local/bin/ \
#   && rm -rf /tmp/gotty \
#   && openssl req -x509 -nodes -days 9999 -subj "/C=US/ST=CA/O=Acme, Inc." -newkey rsa:2048 -keyout ~/.gotty.key -out ~/.gotty.crt

### set up bot
ADD ./src/requirements.txt requirements.txt
RUN pip3 install cython
RUN pip3 install -r ./requirements.txt
COPY ./src /reddit-karma-bot-src

# run it
ENTRYPOINT [ "/bin/bash" ]
CMD [ "/reddit-karma-bot-src/run.sh" ]
