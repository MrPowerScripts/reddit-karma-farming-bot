FROM phusion/baseimage:0.11

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
      pkg-config \
      wget \
      tmux \
      python2.7 \
      python-pip \
      python-setuptools \
      python-dev \
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
RUN pip install wheel
RUN pip install --upgrade pip wheel -r requirements.txt
COPY ./src /reddit-karma-bot-src

# run it
ENTRYPOINT [ "/bin/bash" ]
CMD [ "/reddit-karma-bot-src/run.sh" ]
