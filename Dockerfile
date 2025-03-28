FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY .env .env

EXPOSE 8000

ENV MONGO_URI=${MONGO_URI}
ENV ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}
ENV SECRET_KEY=${SECRET_KEY}
ENV ALGORITHM=${ALGORITHM}

CMD ["uvicorn", "app.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
