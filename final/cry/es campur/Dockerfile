# Menggunakan image Ubuntu sebagai base
FROM ubuntu:focal

# Set environment variables to reduce interaction prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update dan install paket yang diperlukan dalam satu RUN command
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip socat curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install paket Python di baris terpisah untuk mengurangi potensi error
RUN pip3 install --no-cache-dir pycryptodome sympy

# Buat direktori untuk tantangan
RUN mkdir -p /challs

# Salin skrip chall.py dan flag.txt ke dalam kontainer
COPY chall.py /challs/chall.py  
COPY flag.txt /challs/flag.txt
WORKDIR /challs

# Sesuaikan permissions dengan aman
RUN chmod 755 /challs/chall.py && \
    chmod 644 /challs/flag.txt && \
    chmod 755 /usr/bin/env /usr/bin/python3 /bin/dash /bin/bash /bin/sh /bin/cat /usr/bin/curl /usr/bin/groups /usr/bin/id /bin/ls

# Expose port yang digunakan aplikasi
EXPOSE 9002

# Menjalankan program dengan socat di port 9002 tanpa "stderr"
CMD ["socat", "TCP-LISTEN:9002,reuseaddr,fork", "EXEC:python3 /challs/chall.py,su=nobody"]
