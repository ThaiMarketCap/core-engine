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
COPY utils.py /
COPY compute_indices.py /
COPY plot_market.py /
COPY plot_price2mkcap.py /
COPY www /www
COPY optjar /optjar

RUN mkdir price-indices

WORKDIR /
EXPOSE 5000

CMD ["python", "-u", "thcapd.py"]
