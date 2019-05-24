From python:3

WORKDIR /forex
RUN mkdir forex instance

COPY requirements.txt run.py config.py ./
COPY forex forex/
copy instance instance/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run.py"]

