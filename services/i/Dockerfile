FROM debian:jessie
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
apt-get install -y python3 python3-flask python3-pip && \
pip3 install pymysql
RUN useradd i
COPY config.py i.conf i.py /home/i/
RUN chown -R i:i /home/i/
EXPOSE 8090
USER i
WORKDIR /home/i
CMD ["python3","./i.py"]
