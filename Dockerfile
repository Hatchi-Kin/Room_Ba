#FROM python:3.8.3-alpine
#RUN pip install --upgrade pip
#RUN adduser -D myuser
#USER myuser
#WORKDIR /home/myuser
#COPY --chown=myuser:myuser requirements.txt requirements.txt
#RUN pip install --user -r requirements.txt
#ENV PATH="/home/myuser/.local/bin:${PATH}"
#COPY --chown=myuser:myuser . .
#CMD [ "python", "./room_ba.py" ]
FROM python:3.8.3

RUN apt-get update && apt-get install -y gcc

RUN pip install --upgrade pip
RUN adduser myuser
USER myuser
WORKDIR /home/myuser
COPY --chown=myuser:myuser requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PATH="/home/myuser/.local/bin:${PATH}"
COPY --chown=myuser:myuser . .
CMD [ "python", "./room_ba.py" ]
