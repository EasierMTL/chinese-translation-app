FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
# COPY ./data /code/data
# COPY ./productionModels /code/productionModels
# COPY ./config.yml /code/config.yml
EXPOSE 5001/tcp
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./chinese_translation_api /code/chinese_translation_api
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "5001", "--workers", "1"]
# nginx SSL
# CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "5001"]