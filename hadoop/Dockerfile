
FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openjdk-17-jdk-headless \
    python3 \
    openssh-server \
    openssh-client \
    curl \
    ca-certificates \
    procps \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV PATH="${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin:${JAVA_HOME}/bin:${PATH}"

RUN curl -fsSL \
    https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz \
    -o /tmp/hadoop-3.3.6.tar.gz \
    && curl -fsSL \
    https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz.sha512 \
    -o /tmp/hadoop-3.3.6.tar.gz.sha512 \
    && cd /tmp \
    && sed 's/hadoop-3.3.6-RC1.tar.gz/hadoop-3.3.6.tar.gz/' \
    hadoop-3.3.6.tar.gz.sha512 | sha512sum -c - \
    && tar -xzf hadoop-3.3.6.tar.gz -C /opt \
    && mv /opt/hadoop-3.3.6 /opt/hadoop \
    && rm hadoop-3.3.6.tar.gz hadoop-3.3.6.tar.gz.sha512

RUN mkdir -p /run/sshd /data/input /data/output \
    && ssh-keygen -A

WORKDIR /opt/hadoop

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D", "-e"]
