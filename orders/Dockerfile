FROM python:3.13
WORKDIR /application
COPY ./requirements.txt /application/requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /application/requirements.txt
COPY ./common /application/common
COPY ./orders /application/orders
ENV DATABASE_URL=postgresql://api:password@127.0.0.1:5432/ecommerce
ENV PORT=8000
ENV WORKERS=1
CMD ["python", "-m", "orders.main"]
