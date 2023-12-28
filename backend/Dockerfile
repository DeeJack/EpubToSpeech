# Use the official Python image as a base
FROM python:3.11-slim

ENV PORT=5000
# ENV FLASK_APP=home.py
ENV HOST=0.0.0.0

# Set the working directory
WORKDIR /app

RUN mkdir -p database

RUN mkdir -p static
RUN mkdir -p static/uploads
RUN mkdir -p logs

# Update the package lists
RUN apt-get update

# Install packages
RUN apt-get install -y espeak ffmpeg libespeak1 wget


RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
RUN dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb
RUN apt -y install libssl1.1
# RUN wget -O - https://www.openssl.org/source/openssl-1.1.1u.tar.gz | tar zxf - && \
#     cd openssl-1.1.1u && \
#     ./config --prefix=/usr/local && \
#     make -j $(nproc) && \
#     make install_sw install_ssldirs && \
#     ldconfig -v && \
#     export SSL_CERT_DIR=/etc/ssl/certs && \
#     export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH


RUN apt-get update
RUN apt-get install -y build-essential libssl-dev ca-certificates libasound2


# Copy the requirements file to install dependencies
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port the app runs on
# EXPOSE 5000

# Command to run the application
# CMD ["python", "home.py"]

CMD [ "python3", "-u", "-m" , "flask", "run", "--host=0.0.0.0"]