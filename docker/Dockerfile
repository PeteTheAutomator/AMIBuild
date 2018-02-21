FROM alpine:latest
RUN apk add --no-cache python python-dev py-pip musl-dev libffi-dev openssl-dev gcc make git
RUN pip install ansible boto
RUN apk add --no-cache curl
RUN pip install requests
