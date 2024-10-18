FROM python:3.11
WORKDIR /api
COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
COPY ./app /api/app
ENV DATABASE_URL=postgresql://api:password@127.0.0.1:5432/ecommerce
ENV PORT=8000
ENV WORKERS=4
CMD ["python", "-m", "app.main"]
