FROM ubuntu:20.04

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y curl python3.8 python3.8-dev python3-pip cmake libboost-dev \
                libboost-system-dev libboost-thread-dev \
                libboost-regex-dev libboost-filesystem-dev libboost-iostreams-dev \
                libgdal-dev libglm-dev libarmadillo-dev libogdi-dev libogdi4.1 --no-install-recommends tzdata

RUN mkdir /helios-plusplus
RUN curl https://github.com/3dgeo-heidelberg/helios/releases/download/v1.0.3/helios-plusplus-lin.tar.gz -L -o \
helios-plusplus-lin.tar.gz && tar -C helios-plusplus -xvf helios-plusplus-lin.tar.gz && rm helios-plusplus-lin.tar.gz

RUN cp /helios-plusplus/run/*.so*  /usr/lib/x86_64-linux-gnu/

WORKDIR /usr/lib/x86_64-linux-gnu
RUN ln -s libjson-c.so.4 libjson-c.so.3 && \
    ln -s libnetcdf.so.15 libnetcdf.so.13 && \
    ln -s libhdf5_serial.so.103 libhdf5_serial.so.100 && \
    ln -s libproj.so.15 libproj.so.19

WORKDIR /usr/lib
RUN ln -s libogdi.so.4.1 libogdi.so.3.2

WORKDIR /helios-plusplus
RUN run/helios

RUN mkdir -p /opt/gui-helios
WORKDIR /opt/gui-helios
COPY . .

RUN mv /helios-plusplus /opt/gui-helios
RUN mv scanners2.xml platforms2.xml helios-plusplus/data/

RUN pip3 install -r requirements.txt

ENV ENV PROD
EXPOSE 5000

CMD python3 main.py
