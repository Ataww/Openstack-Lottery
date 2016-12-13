FROM debian:jessie# coding=utf-8
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
apt-get install -y python3 python3-flask
RUN apt-get install -y imagemagick
RUN useradd b
COPY config.py b.conf b.py /home/b/
RUN chown -R w:w /home/b/
EXPOSE 8090
USER b
WORKDIR /home/b
CMD ["./b.py"]
