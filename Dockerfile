FROM ubuntu

WORKDIR /reddit-karma-bot
SHELL ["/bin/bash", "-c"]

### this is all installing go stuff ###
# gcc for cgo
RUN apt-get update && apt-get install -y --no-install-recommends \
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
    ca-certificates

RUN mkdir -p /tmp/gotty \
  && GOPATH=/tmp/gotty go get github.com/yudai/gotty \
  && mv /tmp/gotty/bin/gotty /usr/local/bin/ \
  && rm -rf /tmp/gotty

### this is the reddit-karma-bot app installation
ADD ./src/requirements.txt requirements.txt
RUN pip install wheel
RUN pip install -r requirements.txt
COPY ./src /reddit-karma-bot-src

### SSL for gotty
RUN openssl req -x509 -nodes -days 9999 -subj "/C=US/ST=CA/O=Acme, Inc." -newkey rsa:2048 -keyout ~/.gotty.key -out ~/.gotty.crt

### Run that shit son
ENTRYPOINT [ "/bin/bash" ]
CMD [ "/reddit-karma-bot-src/run.sh" ]