FROM python:3.9.5-slim as base
# debian:buster-slim
#https://www.ianlewis.org/en/creating-smaller-docker-images

RUN apt-get update
RUN apt-get install -y g++ curl
RUN apt-get install -y gdal-bin libgdal-dev
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ENV LANG=C.UTF-8

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY ./docker/ /tmp/
#RUN pip install GDAL==$(gdal-config --version) --global-option=build_ext  --global-option="-I/usr/include/gdal"
RUN pip3 install -r /tmp/requirements.txt

COPY src /app/src
ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR /app

RUN apt-get remove -y --purge libgdal-dev g++

CMD ["flask", "run", "-h", "0.0.0.0"]
