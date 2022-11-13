FROM python:3 AS flask_api
COPY . /back-end
RUN pip install -r /back-end/api_server/requirements.txt
ENV PYTHONPATH='/back-end/api_server'
ENTRYPOINT ["python", "/back-end/api_server/openapi_server/__main__.py"]

#FROM python:3
#COPY /storage_mock /storage_mock
#ENTRYPOINT ["python", "/storage_mock/storage_client.py"]