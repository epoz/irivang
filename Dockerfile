FROM python:3.9.7

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src .

RUN mkdir data
ENV DOMAIN=foo.com
RUN python main.py

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app" ]
