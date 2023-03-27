FROM python:3.8
RUN groupadd -r mygroup && useradd -r -g mygroup myuser
RUN mkdir app && chown -R myuser app
USER myuser
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
CMD python3 app.py


