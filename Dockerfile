FROM python:3.11
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN cp .env-exaemple .env
COPY . .
CMD [ "python", "./room_ba.py" ]