FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install kafka-python
EXPOSE 5000
CMD ["python", "-m", "WM_Central.wm_central", "5000", "localhost:9092"]