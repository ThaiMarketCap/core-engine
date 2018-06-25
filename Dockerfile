FROM python:2.7.14-alpine

# add gcc
RUN apk add --no-cache gcc musl-dev

# set timezone
RUN apk add -U tzdata
RUN cp /usr/share/zoneinfo/Asia/Bangkok /etc/localtime
RUN date

# prepare python requirements
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# the app
COPY thcapd.py /
COPY compute_indices.py /
COPY plot_market.py /

RUN mkdir price-indices
RUN mkdir www

WORKDIR /
EXPOSE 5000

CMD ["python", "-u", "thcapd.py"]
