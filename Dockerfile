FROM python:2.7.14-alpine
RUN apk add -U tzdata
RUN cp /usr/share/zoneinfo/Asia/Bangkok /etc/localtime
RUN date

ADD requirements.txt /requirements.txt
COPY thcapd.py /
COPY compute_indices.py /
RUN mkdir price-indices

WORKDIR /
RUN pip install -r /requirements.txt


CMD ["python", "-u", "thcapd.py"]
