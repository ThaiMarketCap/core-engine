FROM python:2.7.14-alpine

# add gcc
RUN apk add --no-cache gcc musl-dev

# set timezone
RUN apk add -U tzdata
RUN cp /usr/share/zoneinfo/Asia/Bangkok /etc/localtime
RUN date

ADD requirements.txt /requirements.txt
COPY thcapd.py /
COPY compute_indices.py /
RUN mkdir price-indices

WORKDIR /
RUN pip install -r /requirements.txt
EXPOSE 5000

CMD ["python", "-u", "thcapd.py"]
