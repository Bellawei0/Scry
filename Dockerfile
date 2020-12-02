FROM python:3.6.1
COPY ./Backend/requirements.txt /app/requirements.txt
WORKDIR /app
COPY ./Backend* /app
ADD ./Frontend/build /app/build
RUN apt-get update; apt-get -y install python3-matplotlib
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt
CMD ["python3", "-u", "scry_prod.py"]

