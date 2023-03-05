FROM python:3.8
WORKDIR /app
RUN adduser --disabled-password --gecos '' appuser
USER appuser
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
CMD python3 app.py


