FROM busybox:latest
MAINTAINER Rye Salvador <salvadorrye@gmail.com>
RUN mkdir -p /mysite/media
VOLUME ["/mysite/media"]

