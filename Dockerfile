FROM python:3.9.17

WORKDIR /app

COPY requirements.txt /app/
COPY api.py /app/
COPY df_airfleets_clean.json /app/
COPY world_map.html /app/

RUN pip install -r requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
