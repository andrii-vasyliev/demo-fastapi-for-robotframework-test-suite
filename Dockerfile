FROM python:3.11
WORKDIR /api
COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
COPY ./app /api/app
CMD ["python", "-m", "app.main"]
