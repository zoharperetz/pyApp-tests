FROM python:3.8
WORKDIR /app
RUN addgroup appuser && \
    adduser --gecos "" --gid "" --disabled-password --home /app --no-create-home --shell /sbin/nologin --ingroup appuser appuser

USER appuser
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
CMD python3 app.py


