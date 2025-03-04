FROM continuumio/miniconda3

WORKDIR /home/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY server/ server/

CMD uvicorn server.api:app --port $PORT --host 0.0.0.0 
