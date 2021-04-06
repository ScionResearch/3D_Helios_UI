FROM python
WORKDIR /opt/demo/
COPY . .
RUN pip install -r requirements.txt
RUN mkdir helios-plusplus
RUN curl https://github.com/3dgeo-heidelberg/helios/releases/download/v1.0.3/helios-plusplus-lin.tar.gz -L -o \
helios-plusplus-lin.tar.gz && tar -C helios-plusplus -xvf helios-plusplus-lin.tar.gz && rm helios-plusplus-lin.tar.gz

ENTRYPOINT python3 main.py
